#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import os
import sys

import numba
import numpy as np
import time
from array import array
from datetime import datetime


from scipy.interpolate import interp1d
from pathlib import Path
from matplotlib import pyplot as plt
from scipy import stats

from stix.spice import stix_datetime
from stix.core import stix_datatypes as sdt
from stix.core import mongo_db as db
import pickle
mdb = db.MongoDB()

#


# 2.3 ADC/keV
# Estimated energy conversion factor
from matplotlib.backends.backend_pdf import PdfPages
#import numba
SPECTRUM_MODEL_DATA_FILES=Path(__file__).parent.parent/ 'data' / 'ExpSpecModel.npz'


def interp(xvals, yvals, xnew):
    # x y define orignal points
    # xnew interpolated data points
    f2 = interp1d(xvals, yvals, bounds_error=False, fill_value=0)
    y = f2(xnew)
    return y

def chi2test(obs_y:np.ndarray,exp_y:np.ndarray):
    """
        Do chisquare test between to spectra
    Arguments
    obs_y: numpy.ndarray
        observed energy spectrum
    exp_y: numpy.ndarray
        expected energy spectrum
    Returns
        chisquare: float
            chiquare
        dof:
            dof: dregress of freedom
    """
    #exp_y: expected spectrum
    #obs_y: observed spectra
    norm_factor=np.sum(obs_y)/np.sum(exp_y)
    exp_y[exp_y==0]=1e-12
    dof=obs_y.size -1
    return np.sum((obs_y-exp_y*norm_factor)**2/exp_y),dof
    #stats.chisquare is too slow
    #return stats.chisquare(f_obs=obs_y, f_exp=exp_y)

class Calibration(object):
    """
    Fit calibration spectra using  spectrum models loaded from npy file

    """
    FIT_RANGE_KEV = (28, 85) #20 keV - 90 keV
    SPECTRUM_SEL_ADC_RANGE=(252, 448)
    #used to check if do fitting for a subspectrum
    OFFSETS_LIMITS = (210, 235)  #default range, load from ELUT by default
    MIN_COUNTS = 100
    DEFAULT_OUTPUT_DIR = '/data/calibration/'
    STEPS=10000  #number of data points generated for each interation
    MAX_DEPTH=1  #random grid recursive search depth
    SCALE_FACTOR=10  #shrink search region after each interation
    PEAK_MIN_COUNTS = 50  # spectrum with little counts ignored
    MEAN_GAIN=2.31

    ELUT_ENERGIES = [
        4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 25, 28, 32, 36,
        40, 45, 50, 56, 63, 70, 76, 84, 100, 120, 150
    ]
    SUM_SPECTRUM_STEPS=10000
    PIXEL_EBINS = np.linspace(0, 100, SUM_SPECTRUM_STEPS)

    def __init__(self):
        self.pixel_fspec_models, self.default_slopes, self.default_offsets = \
            self.load_spectrum_models(SPECTRUM_MODEL_DATA_FILES)

    def load_spectrum_models(self, npy_filename):
        data= np.load(npy_filename)
        spec=data['arr_0']
        slope=data['arr_1']
        offset=data['arr_2']
        res = []
        for detector in range(32):
            for pixel in range(12):
                res.append(
                    interp1d(Calibration.PIXEL_EBINS, spec[detector][pixel], bounds_error=False, fill_value=0)
                )
        return res, slope, offset

    def compute_elut(self,offset, slope):
        elut = []
        for det in range(0, 32):
            for pix in range(0, 12):
                p0 = offset[det][pix]
                p1 = slope[det][pix]
                # print(det, pix, p0, p1)
                if p0 > 0 and p1 > 0:
                    row = [det, pix, p0, p1]
                    elut_e_low= [int(4 * (p0 + p1 * x)) for x in Calibration.ELUT_ENERGIES]
                    row.extend(elut_e_low)
                    elut.append(row)
        return elut

    def get_subspec(self,spectrum, start_ch, bin_width, only_fit_range=True):
        """
        reconstruct subspectrum
        Args
        spectrum: List of counts
        start_ch: start ADC channel
        bin_width:  number of summed ADC channels per bin
        xmin, xmax:  limits to slice the spectrum
        Returns
        x: a numpy array indicates ADC channels
        y: a numpy array indicates counts of spectrum
        """
        spec_len = len(spectrum)

        spectrum = np.array(spectrum)
        _x = np.arange(spec_len) * bin_width + 0.5 * bin_width + start_ch
        max_count = np.max(spectrum)
        peak_x = _x[spectrum == max_count][0]
        min_adc=peak_x-(31-Calibration.FIT_RANGE_KEV[0])*Calibration.MEAN_GAIN
        max_adc=peak_x+(-31+Calibration.FIT_RANGE_KEV[1])*Calibration.MEAN_GAIN

        if only_fit_range:
            clip = (_x >min_adc) & (_x < max_adc)
            return _x[clip], spectrum[clip]
        return _x, spectrum

    def get_intensity_from_model(self, detector:int, pixel:int, offset:float, slope:float, spec_adcs:np.ndarray) -> object:
        """
        convert adc channels to keV
        Args
            offset: float
                offset
            slope: float
                gain
        returns
            an array having the same length as adc spectrum
        """
        energies=(spec_adcs-offset)/slope
        return energies, self.pixel_fspec_models[detector*12+pixel](energies)

    def correlate(self, detector, pixel, offset, slope, spec_x:np.ndarray,  spec_y:np.ndarray):
        """
        calculate correlation of two spectra
        Parameters
        spec_x: numpy.ndarray
           energies of experimetal spectrum
        spec_y: numpy.ndarray
            counts spectrum
        pred_spec: numpy.ndarray
          predicted spectrum

        Returns
         chi2:  chisquare
         dof: dof
        """
        energies, pred_spec = self.get_intensity_from_model(detector,pixel, offset, slope, spec_x)
        chi, dof=chi2test(spec_y, pred_spec)
        return chi,dof
    def quick_random_search(self, detector,pixel, offsets_1d, slopes_1d, spec_x,spec_y,  max_delta=1e-3, depth=0):
        """
         Parameter search recursively
         finner search for higher depth
        """
        best_fit = {'slope': 0, 'offset': 0}
        min_chi2=np.inf

        for offset, slope in zip(offsets_1d, slopes_1d):
            chi2, dof= self.correlate(detector,pixel, offset, slope, spec_x, spec_y)
            if chi2< min_chi2:
                best_fit = {'slope': slope, 'offset': offset, 'chi2':chi2, 'dof':dof}
                min_chi2= chi2
        #delta=(best_cor_factor-min(factors))/best_cor_factor
        #print('depth:', depth, delta)
        return best_fit
        '''
        if delta<max_delta or depth>Calibration.MAX_DEPTH:
            #no need to search further
            #print(best_fit)
            return best_fit
        #next search
        #print('depth:', depth, delta)
        offset_next_range=(np.max(offsets_1d)-np.min(offsets_1d))/Calibration.SCALE_FACTOR
        slope_next_range=(np.max(slopes_1d)-np.min(slopes_1d))/Calibration.SCALE_FACTOR
        #steps=len(offsets_1d)
        #print("Range:",offset_next_range, slope_next_range)
        offsets_1d=np.random.uniform(best_fit['offset']-offset_next_range,
                                     best_fit['offset']+offset_next_range, len(offsets_1d))
        slopes_1d = np.random.uniform(best_fit['slope'] - slope_next_range,
                                      best_fit['slope'] + slope_next_range,len(slopes_1d))
        
        return self.quick_random_search(detector, pixel, offsets_1d, slopes_1d, spec_x,
                                        spec_y,  max_delta, depth+1)
                                        '''



    def find_solution(self, detector, pixel, sbspec_id,spectrum, start_ch, bin_width,
                      pdf=None):
        """
        Fit spectrum using a spectrum model
        Arguments
        spec: spectrum counts
        start_ch: start channel
        bin_width: number of summed ADC bins
        model:
          An 2d array indicate x, y of the theoretical spectrum. Use ECC model if it is None
        """
        spec_x, spec_y = self.get_subspec(spectrum, start_ch, bin_width) #real spectra
        #peak1_y = np.max(spec_y)
        #peak1_x = spec_x[spec_y==peak1_y][0]
        # find the peak with highest counts in the predefined range
        #x_shift = Calibration.MEAN_GAIN * (81 - 31)
        #peak3_peak_range = np.array([peak1_x + 0.9 * x_shift, peak1_x + 1.1 * x_shift])
        #peak3_x_range=(spec_x>peak3_peak_range[0]) & (spec_x<peak3_peak_range[1])
        #peak3_y_clip=spec_y[peak3_x_range]
        #peak3_max_counts=np.max(peak3_y_clip)#80 keV max counts
        #peak3_x_clip=spec_x[peak3_x_range]
        #peak3_x=peak3_x_clip[peak3_y_clip==peak3_max_counts][0]
        #rough estimation of ranges
        #print("PEAK",peak1_x, peak3_x, peak3_peak_range, peak3_max_counts)
        #slope_rough = (peak3_x - peak1_x) / (81 - 31)
        #offset_rough=peak1_x-31*slope_rough
        slope_rough=self.default_slopes[detector][pixel]
        offset_rough=self.default_offsets[detector][pixel]
        offset_limits=[offset_rough-5, offset_rough+5]
        slope_limits = [slope_rough - 2*bin_width/(81-31), slope_rough + 2*bin_width/(81-31)]
        print("Limits", offset_limits, slope_limits)

        offsets_1d, slopes_1d=np.random.uniform(offset_limits[0],offset_limits[1],Calibration.STEPS), \
                              np.random.uniform(slope_limits[0],slope_limits[1], Calibration.STEPS)


        best_fit=self.quick_random_search(detector,pixel, offsets_1d, slopes_1d, spec_x, spec_y)

        #print(best_fit)
        energies, pred_spec = self.get_intensity_from_model(detector,pixel,best_fit['offset'], best_fit['slope'], spec_x)
        #fout.write(f'{detector},{pixel},{best_fit["offset"]},{best_fit["slope"]}\n')
        if pdf:
            fig=plt.figure()
            norm_spec=pred_spec *np.sum(spec_y)/np.sum(pred_spec)
            plt.plot(energies, norm_spec,label='Model')
            plt.errorbar(energies,spec_y,yerr=np.sqrt(spec_y), label='exp')
            ax=plt.gca()
            plt.text(0.6, 0.7,
                 f'p0 = {best_fit["offset"]:.3f}, p1={best_fit["slope"]:.3f}',
                 horizontalalignment='center', verticalalignment='center',
                 transform=ax.transAxes)
            plt.xlabel('Energy (keV)')
            plt.ylabel('Normalized counts')
            plt.title(f'Detector {detector},pixel {pixel}, subspec {sbspec_id} ')
            plt.legend()
            pdf.savefig(fig)
            plt.close()
        return best_fit
    def create_sum_spectra(self, calibration_id, spectra, slope:np.ndarray,offset:np.ndarray):
        # do calibration
        sum_spectra = {}#sum spectrum for all detectors
        # cc = TCanvas()

        pixel_sum_spectra = np.zeros((32, 12, Calibration.SUM_SPECTRUM_STEPS))  # pixel sum spectrum, 100 energy bins

        xvals = []
        for spec in spectra:

            detector, pixel, sbspec_id, start, bin_width, spectrum = spec
            num_points = len(spectrum)
            spectrum=np.array(spectrum)
            if np.sum(spectrum) < Calibration.PEAK_MIN_COUNTS:
                continue


            end = start + bin_width * num_points  # end ADC

            if slope[detector][pixel] > 0 and offset[detector][pixel] > 0:
                #energies = (np.linspace(start, end - bin_width, num_points) - offset[detector][pixel]) / \
                #           slope[detector][pixel]
                spec_x, spec_y = self.get_subspec(spectrum, start, bin_width, False)
                energies=(spec_x-offset[detector][pixel])/slope[detector][pixel]
                if sbspec_id not in sum_spectra:
                    #first occurent of the spectrum, any detector
                    min_energy,max_energy=np.min(energies)*0.8,np.max(energies)*1.2
                    xvals = np.linspace(min_energy, max_energy,
                                        int((num_points + 1) * 1.4))
                    sum_spectra[sbspec_id] = [xvals, np.zeros_like(xvals)]  # sum spectrum x vs. y
                yvals = interp(energies, spectrum / bin_width, xvals)
                sum_spectra[sbspec_id][1] += yvals
                amps = interp(energies, spectrum / bin_width, Calibration.PIXEL_EBINS)
                pixel_sum_spectra[detector][pixel]+=amps
        sub_sum_spec = {}
        points = 1150*2
        energy_range = np.linspace(-10, 450, points)
        sbspec_sum = np.zeros(points)
        for key, val in sum_spectra.items():  # mongodb doesn't support array
            sub_sum_spec[f'sbspec - {key}'] = [
                v.tolist() for v in sum_spectra[key]
            ]
            sbspec_sum += interp(sum_spectra[key][0], sum_spectra[key][1],
                                 energy_range)

        sub_sum_spec['sbspec sum'] = [energy_range.tolist(), sbspec_sum.tolist()]
        return sub_sum_spec, pixel_sum_spectra

    def process_one_run(self, calibration_id, create_pdf=True):
        docs = mdb.get_calibration_run_data(calibration_id)
        if not docs:
            print("Calibration run {} data doesn't exist".format(calibration_id))
            return
        data = docs[0]
        spectra = data['spectra']
        pdf, pdf_filename=None, None


        if create_pdf:
            pdf_filename = os.path.abspath(
                os.path.join(Calibration.DEFAULT_OUTPUT_DIR, f'calibration_{calibration_id}_chisquare.pdf'))
            pdf = PdfPages(pdf_filename)
        slope = np.zeros((32, 12))
        offset = np.zeros((32, 12))
        chi2= np.zeros((32, 12))
        slope_error = np.zeros((32, 12))
        offset_error = np.zeros((32, 12))
        report = {}
        report['fit_parameters'] = []
        print(f'Processing calibration run {calibration_id} ...')

        for spec in spectra:
            # iterate over sub spectra
            detector, pixel, sbspec_id, start, bin_width, spectrum = spec
            print(detector,pixel,sbspec_id)
            spectrum = np.array(spectrum)
            if np.sum(spectrum) < Calibration.PEAK_MIN_COUNTS:
                # total counts less than the limit
                continue

            end = start + bin_width * len(spectrum)
            if start > Calibration.SPECTRUM_SEL_ADC_RANGE[0] or end < Calibration.SPECTRUM_SEL_ADC_RANGE[1]:
                #ignore those spectra
                continue
            best_fit=self.find_solution(detector, pixel, sbspec_id, spectrum,start, bin_width,
                                               pdf)

            #jjdetector>0:
            #   break

            slope[detector][pixel] = best_fit['slope']
            offset[detector][pixel] = best_fit['offset']
            chi2[detector][pixel]=best_fit['chi2']
            slope_error[detector][pixel] = 0.5*bin_width/(81-30)
            offset_error[detector][pixel] = 0.5*bin_width
        if create_pdf:
            pdf.close()
            report['pdf']=pdf_filename
        report['elut'] = self.compute_elut(offset, slope)

        sub_sum_spec, pixel_sum_spectra=self.create_sum_spectra(calibration_id,spectra, slope, offset)

        calibration_result_filename=os.path.join(Calibration.DEFAULT_OUTPUT_DIR,
                                                f'calibration_results_{calibration_id}.npz')
        print(f'calibration_results saved to: {calibration_result_filename}')

        np.savez(calibration_result_filename, pixel_sum_spectra, slope, offset)

        report['calibration_results']=calibration_result_filename
        report['slope'] = slope.reshape(-1).tolist()
        report['offset'] = offset.reshape(-1).tolist()
        report['slope_error'] = slope_error.reshape(-1).tolist()
        report['offset_error'] = offset_error.reshape(-1).tolist()
        report['sum_spectra'] = sub_sum_spec
        report['chi2'] = chi2.reshape(-1).tolist()
        # calibrated sum spectra

        mdb.update_calibration_analysis_report(calibration_id, report)
        #fout = open('/home/xiaohl/run_1301_chisquare_sum_spec.csv', 'w')
        #fout.close()

if __name__ == '__main__':
    #output_dir = DEFAULT_OUTPUT_DIR
    # output_dir='./'
    if len(sys.argv) == 1:
        print('Usage ./calibration_ecc <calibration_run_id> [<end id>]')
    elif len(sys.argv) >= 2:
        cal=Calibration()
        start_id = int(sys.argv[1])
        end_id = start_id
        if len(sys.argv) >= 3:
            end_id = int(sys.argv[2])
        for i in range(start_id, end_id + 1):
            cal.process_one_run(i)
