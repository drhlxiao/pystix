#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context structure definition
Created on Thu Aug 29 15:54:01 2019

@author: Hualin Xiao

@TODO: 

    """

CONTEXT_REGISTER_DESC = {
    'REG01': 'Register 1	ICOMP',
    'REG02': 'Register 2	IREQ',
    'REG03_TH_1': 'ASIC channel 1 threshold',
    'REG03_TH_2': 'ASIC channel 2 threshold',
    'REG03_TH_3': 'ASIC channel 3 threshold',
    'REG03_TH_4': 'ASIC channel 4 threshold',
    'REG03_TH_5': 'ASIC channel 5 threshold',
    'REG03_TH_6': 'ASIC channel 6 threshold',
    'REG03_TH_7': 'ASIC channel 7 threshold',
    'REG03_TH_8': 'ASIC channel 8 threshold',
    'REG03_TH_9': 'ASIC channel 9 threshold',
    'REG03_TH_10': 'ASIC channel 10 threshold',
    'REG03_TH_11': 'ASIC channel 11 threshold',
    'REG03_TH_12': 'ASIC channel 12 threshold',
    'REG03_TH_13': 'ASIC channel 13 threshold',
    'REG03_TH_14': 'ASIC channel 14 threshold',
    'REG03_TH_15': 'ASIC channel 15 threshold',
    'REG03_TH_16': 'ASIC channel 16 threshold',
    'REG03_TH_17': 'ASIC channel 17 threshold',
    'REG03_TH_18': 'ASIC channel 18 threshold',
    'REG03_TH_19': 'ASIC channel 19 threshold',
    'REG03_TH_20': 'ASIC channel 20 threshold',
    'REG03_TH_21': 'ASIC channel 21 threshold',
    'REG03_TH_22': 'ASIC channel 22 threshold',
    'REG03_TH_23': 'ASIC channel 23 threshold',
    'REG03_TH_24': 'ASIC channel 24 threshold',
    'REG03_TH_25': 'ASIC channel 25 threshold',
    'REG03_TH_26': 'ASIC channel 26 threshold',
    'REG03_TH_27': 'ASIC channel 27 threshold',
    'REG03_TH_28': 'ASIC channel 28 threshold',
    'REG03_TH_29': 'ASIC channel 29 threshold',
    'REG03_TH_30': 'ASIC channel 30 threshold',
    'REG03_TH_31': 'ASIC channel 31 threshold',
    'REG03_TH_32': 'ASIC channel 32 threshold',
    'REG04': 'Register 4	SEL_TEST',
    'REG05': 'Register 5	TPEAK',
    'REG06': 'Register 6	I0',
    'REG07': 'Register 7	RDELAY',
    'REG08': 'Register 8	GAIN',
    'REG09': 'Register 9	SPY',
    'REG10': 'Register 10	VREFF2P',
    'REG11': 'Register 11	TNUE',
    'REG12': 'Register 12	ALIMON'
}

CONTEXT_REGISTER_BIT_SIZE = [('REG01', 2), ('REG02', 3), ('REG03_TH_1', 6),
                             ('REG03_TH_2', 6), ('REG03_TH_3', 6),
                             ('REG03_TH_4', 6), ('REG03_TH_5', 6),
                             ('REG03_TH_6', 6), ('REG03_TH_7', 6),
                             ('REG03_TH_8', 6), ('REG03_TH_9', 6),
                             ('REG03_TH_10', 6), ('REG03_TH_11', 6),
                             ('REG03_TH_12', 6), ('REG03_TH_13', 6),
                             ('REG03_TH_14', 6), ('REG03_TH_15', 6),
                             ('REG03_TH_16', 6), ('REG03_TH_17', 6),
                             ('REG03_TH_18', 6), ('REG03_TH_19', 6),
                             ('REG03_TH_20', 6), ('REG03_TH_21', 6),
                             ('REG03_TH_22', 6), ('REG03_TH_23', 6),
                             ('REG03_TH_24', 6), ('REG03_TH_25', 6),
                             ('REG03_TH_26', 6), ('REG03_TH_27', 6),
                             ('REG03_TH_28', 6), ('REG03_TH_29', 6),
                             ('REG03_TH_30', 6), ('REG03_TH_31', 6),
                             ('REG03_TH_32', 6), ('REG04', 32), ('REG05', 4),
                             ('REG06', 2), ('REG07', 5), ('REG08', 2),
                             ('REG09', 2), ('REG10', 3), ('REG11', 3),
                             ('REG12', 32)]

CONTEXT_PARAMETER_BIT_SIZE = [
    ('ContextMgmt_param_fdir_sw_1v5c_min', 12),
    ('ContextMgmt_param_fdir_sw_1v5c_max', 12),
    ('ContextMgmt_param_fdir_hw_1v5c', 12),
    ('ContextMgmt_param_fdir_sw_2v5c_min', 12),
    ('ContextMgmt_param_fdir_sw_2v5c_max', 12),
    ('ContextMgmt_param_fdir_hw_2v5c', 12),
    ('ContextMgmt_param_fdir_sw_3v3c_min', 12),
    ('ContextMgmt_param_fdir_sw_3v3c_max', 12),
    ('ContextMgmt_param_fdir_hw_3v3c', 12),
    ('ContextMgmt_param_fdir_sw_spw0c_min', 12),
    ('ContextMgmt_param_fdir_sw_spw0c_max', 12),
    ('ContextMgmt_param_fdir_sw_spw1c_min', 12),
    ('ContextMgmt_param_fdir_sw_spw1c_max', 12),
    ('ContextMgmt_param_fdir_sw_spw2c_min', 12),
    ('ContextMgmt_param_fdir_sw_spw2c_max', 12),
    ('ContextMgmt_param_fdir_hw_spwc', 12),
    ('ContextMgmt_param_fdir_sw_det0c_min', 12),
    ('ContextMgmt_param_fdir_sw_det0c_max', 12),
    ('ContextMgmt_param_fdir_sw_det1c_min', 12),
    ('ContextMgmt_param_fdir_sw_det1c_max', 12),
    ('ContextMgmt_param_fdir_sw_det2c_min', 12),
    ('ContextMgmt_param_fdir_sw_det2c_max', 12),
    ('ContextMgmt_param_fdir_sw_det3c_min', 12),
    ('ContextMgmt_param_fdir_sw_det3c_max', 12),
    ('ContextMgmt_param_fdir_sw_det4c_min', 12),
    ('ContextMgmt_param_fdir_sw_det4c_max', 12),
    ('ContextMgmt_param_fdir_hw_detc', 12),
    ('ContextMgmt_param_fdir_sw_att0c_min', 12),
    ('ContextMgmt_param_fdir_sw_att0c_max', 12),
    ('ContextMgmt_param_fdir_sw_att1c_min', 12),
    ('ContextMgmt_param_fdir_sw_att1c_max', 12),
    ('ContextMgmt_param_fdir_sw_att2c_min', 12),
    ('ContextMgmt_param_fdir_sw_att2c_max', 12),
    ('ContextMgmt_param_fdir_hw_attc', 12),
    ('ContextMgmt_param_fdir_sw_attv_min', 12),
    ('ContextMgmt_param_fdir_sw_attv_max', 12),
    ('ContextMgmt_param_fdir_hw_attv', 12),
    ('ContextMgmt_param_fdir_sw_hw01_min', 12),
    ('ContextMgmt_param_fdir_sw_hw01_max', 12),
    ('ContextMgmt_param_fdir_hw_hw01', 12),
    ('ContextMgmt_param_fdir_sw_hw02_min', 12),
    ('ContextMgmt_param_fdir_sw_hw02_max', 12),
    ('ContextMgmt_param_fdir_hw_hw02', 12),
    ('ContextMgmt_param_fdir_sw_2v9v_min', 12),
    ('ContextMgmt_param_fdir_sw_2v9v_max', 12),
    ('ContextMgmt_param_fdir_sw_2v5v_min', 12),
    ('ContextMgmt_param_fdir_sw_2v5v_max', 12),
    ('ContextMgmt_param_fdir_sw_1v5v_min', 12),
    ('ContextMgmt_param_fdir_sw_1v5v_max', 12),
    ('ContextMgmt_param_fdir_sw_spw0v_min', 12),
    ('ContextMgmt_param_fdir_sw_spw0v_max', 12),
    ('ContextMgmt_param_fdir_sw_spw1v_min', 12),
    ('ContextMgmt_param_fdir_sw_spw1v_max', 12),
    ('ContextMgmt_param_fdir_sw_asp_vsensa_min', 12),
    ('ContextMgmt_param_fdir_sw_asp_vsensa_max', 12),
    ('ContextMgmt_param_fdir_sw_asp_vsensb_min', 12),
    ('ContextMgmt_param_fdir_sw_asp_vsensb_max', 12),
    ('ContextMgmt_param_fdir_sw_asp_refa_min', 12),
    ('ContextMgmt_param_fdir_sw_asp_refa_max', 12),
    ('ContextMgmt_param_fdir_sw_asp_refb_min', 12),
    ('ContextMgmt_param_fdir_sw_asp_refb_max', 12),
    ('ContextMgmt_param_fdir_sw_asp_photoA0_min', 12),
    ('ContextMgmt_param_fdir_sw_asp_photoA0_max', 12),
    ('ContextMgmt_param_fdir_sw_asp_photoA1_min', 12),
    ('ContextMgmt_param_fdir_sw_asp_photoA1_max', 12),
    ('ContextMgmt_param_fdir_sw_asp_photoB0_min', 12),
    ('ContextMgmt_param_fdir_sw_asp_photoB0_max', 12),
    ('ContextMgmt_param_fdir_sw_asp_photoB1_min', 12),
    ('ContextMgmt_param_fdir_sw_asp_photoB1_max', 12),
    ('ContextMgmt_param_fdir_sw_fpgat_min', 12),
    ('ContextMgmt_param_fdir_sw_fpgat_max', 12),
    ('ContextMgmt_param_fdir_sw_pcbt_min', 12),
    ('ContextMgmt_param_fdir_sw_pcbt_max', 12),
    ('ContextMgmt_param_fdir_sw_tim01t_min', 12),
    ('ContextMgmt_param_fdir_sw_tim01t_max', 12),
    ('ContextMgmt_param_fdir_sw_tim02t_min', 12),
    ('ContextMgmt_param_fdir_sw_tim02t_max', 12),
    ('ContextMgmt_param_fdir_sw_tim03t_min', 12),
    ('ContextMgmt_param_fdir_sw_tim03t_max', 12),
    ('ContextMgmt_param_fdir_sw_tim04t_min', 12),
    ('ContextMgmt_param_fdir_sw_tim04t_max', 12),
    ('ContextMgmt_param_fdir_sw_tim05t_min', 12),
    ('ContextMgmt_param_fdir_sw_tim05t_max', 12),
    ('ContextMgmt_param_fdir_sw_tim06t_min', 12),
    ('ContextMgmt_param_fdir_sw_tim06t_max', 12),
    ('ContextMgmt_param_fdir_sw_tim07t_min', 12),
    ('ContextMgmt_param_fdir_sw_tim07t_max', 12),
    ('ContextMgmt_param_fdir_sw_tim08t_min', 12),
    ('ContextMgmt_param_fdir_sw_tim08t_max', 12),
    ('ContextMgmt_param_fdir_sw_det01t_min', 12),
    ('ContextMgmt_param_fdir_sw_det01t_max', 12),
    ('ContextMgmt_param_fdir_sw_det02t_min', 12),
    ('ContextMgmt_param_fdir_sw_det02t_max', 12),
    ('ContextMgmt_param_fdir_sw_det03t_min', 12),
    ('ContextMgmt_param_fdir_sw_det03t_max', 12),
    ('ContextMgmt_param_fdir_sw_det04t_min', 12),
    ('ContextMgmt_param_fdir_sw_det04t_max', 12),
    ('ContextMgmt_param_fdir_sw_attt_min', 12),
    ('ContextMgmt_param_fdir_sw_attt_max', 12),
    ('ContextMgmt_param_fdir_meas_trig_psut', 8),
    ('ContextMgmt_param_fdir_meas_trig_pcbt', 8),
    ('ContextMgmt_param_fdir_meas_trig_fpgat', 8),
    ('ContextMgmt_param_fdir_meas_trig_3v3c', 8),
    ('ContextMgmt_param_fdir_meas_trig_2v5c', 8),
    ('ContextMgmt_param_fdir_meas_trig_1v5c', 8),
    ('ContextMgmt_param_fdir_meas_trig_spwc', 8),
    ('ContextMgmt_param_fdir_meas_trig_spw0v', 8),
    ('ContextMgmt_param_fdir_meas_trig_spw1v', 8),
    ('ContextMgmt_param_fdir_meas_trig_1v5v', 8),
    ('ContextMgmt_param_fdir_meas_trig_2v5v', 8),
    ('ContextMgmt_param_fdir_meas_trig_2v9v', 8),
    ('ContextMgmt_param_fdir_meas_trig_attv', 8),
    ('ContextMgmt_param_fdir_meas_trig_attc', 8),
    ('ContextMgmt_param_fdir_meas_trig_attt', 8),
    ('ContextMgmt_param_fdir_meas_trig_hv01', 8),
    ('ContextMgmt_param_fdir_meas_trig_hv02', 8),
    ('ContextMgmt_param_fdir_meas_trig_detc', 8),
    ('ContextMgmt_param_fdir_meas_trig_detq1t', 8),
    ('ContextMgmt_param_fdir_meas_trig_detq2t', 8),
    ('ContextMgmt_param_fdir_meas_trig_detq3t', 8),
    ('ContextMgmt_param_fdir_meas_trig_detq4t', 8),
    ('ContextMgmt_param_fdir_meas_trig_asp_refa', 8),
    ('ContextMgmt_param_fdir_meas_trig_asp_refb', 8),
    ('ContextMgmt_param_fdir_meas_trig_tim01t', 8),
    ('ContextMgmt_param_fdir_meas_trig_tim02t', 8),
    ('ContextMgmt_param_fdir_meas_trig_tim03t', 8),
    ('ContextMgmt_param_fdir_meas_trig_tim04t', 8),
    ('ContextMgmt_param_fdir_meas_trig_tim05t', 8),
    ('ContextMgmt_param_fdir_meas_trig_tim06t', 8),
    ('ContextMgmt_param_fdir_meas_trig_tim07t', 8),
    ('ContextMgmt_param_fdir_meas_trig_tim08t', 8),
    ('ContextMgmt_param_fdir_meas_trig_asp_vsensa', 8),
    ('ContextMgmt_param_fdir_meas_trig_asp_vsensb', 8),
    ('ContextMgmt_param_fdir_meas_trig_asp_photoa0', 8),
    ('ContextMgmt_param_fdir_meas_trig_asp_photoa1', 8),
    ('ContextMgmt_param_fdir_meas_trig_asp_photob0', 8),
    ('ContextMgmt_param_fdir_meas_trig_asp_photob1', 8),
    ('ContextMgmt_param_fdir_seu_ignore_flag', 4),
    ('ContextMgmt_param_fdir_enabled_dete_quarter', 4),
    ('ContextMgmt_param_fdir_att_number_moves', 32),
    ('ContextMgmt_param_fdir_att_N1', 8), ('ContextMgmt_param_fdir_att_T1', 8),
    ('ContextMgmt_param_fdir_att_N2', 8), ('ContextMgmt_param_fdir_att_T2',
                                           12),
    ('ContextMgmt_param_fdir_asic_verif_disabled_dete_mask', 32),
    ('ContextMgmt_param_fdir_asic_verif_period', 16),
    ('ContextMgmt_param_fdir_hv01_depolarisation_period', 16),
    ('ContextMgmt_param_fdir_hv02_depolarisation_period', 16),
    ('ContextMgmt_param_fdir_hv01_depolarisation_duration', 16),
    ('ContextMgmt_param_fdir_hv02_depolarisation_duration', 16),
    ('ContextMgmt_param_fdir_enabled_function_mask', 32),
    ('ContextMgmt_param_fdir_enabled_current_function_checks', 8),
    ('ContextMgmt_param_fdir_enabled_voltage_function_checks', 16),
    ('ContextMgmt_param_fdir_enabled_temperature_function_checks', 16),
    ('ContextMgmt_param_config_hv01_line_enabled', 1),
    ('ContextMgmt_param_config_hv02_line_enabled', 1),
    ('ContextMgmt_param_config_hv01_value', 8),
    ('ContextMgmt_param_config_hv02_value', 8),
    ('ContextMgmt_param_config_spw_ocp_state', 1),
    ('ContextMgmt_param_config_det_ocp_state', 1),
    ('ContextMgmt_param_config_att_ocp_state', 1),
    ('ContextMgmt_param_config_1v5_ocp_state', 1),
    ('ContextMgmt_param_config_2v5_ocp_state', 1),
    ('ContextMgmt_param_config_3v3_ocp_state', 1),
    ('ContextMgmt_param_config_att_ovp_state', 1),
    ('ContextMgmt_param_config_hv1_ovp_state', 1),
    ('ContextMgmt_param_config_hv2_ovp_state', 1),
    ('ContextMgmt_param_config_asp_fpga_readout_per_sum', 3),
    ('ContextMgmt_param_config_att_max_pwm', 8),
    ('ContextMgmt_param_config_att_nom_pwm', 8),
    ('ContextMgmt_param_config_fsw_s20_reaction_state', 1),
    ('ContextMgmt_param_config_fsw_enable_tm51', 1),
    ('ContextMgmt_param_config_sdram_prescaler', 16),
    ('ContextMgmt_param_config_rotb_prescaler', 16),
    ('ContextMgmt_param_config_spw_transient_duration', 32),
    ('ContextMgmt_param_calib_cyclic_state', 1),
    ('ContextMgmt_param_calib_tq',
     16), ('ContextMgmt_param_calib_detemask', 32),
    ('ContextMgmt_param_calib_ta', 16),
    ('ContextMgmt_param_calib_formatting_subspectra_mask', 8),
    ('ContextMgmt_param_calib_formatting_subspectrum_1', 30),
    ('ContextMgmt_param_calib_formatting_subspectrum_2', 30),
    ('ContextMgmt_param_calib_formatting_subspectrum_3', 30),
    ('ContextMgmt_param_calib_formatting_subspectrum_4', 30),
    ('ContextMgmt_param_calib_formatting_subspectrum_5', 30),
    ('ContextMgmt_param_calib_formatting_subspectrum_6', 30),
    ('ContextMgmt_param_calib_formatting_subspectrum_7', 30),
    ('ContextMgmt_param_calib_formatting_subspectrum_8', 30),
    ('ContextMgmt_param_calib_formatting_detemask', 32),
    ('ContextMgmt_param_calib_formatting_bit_reduction_flag', 1),
    ('ContextMgmt_param_calib_formatting_pixelmask', 16),
    ('ContextMgmt_param_ql_nominal_period', 16),
    ('ContextMgmt_param_qlbg_enabled', 1),
    ('ContextMgmt_param_qlbg_enabled_tm', 1),
    ('ContextMgmt_param_qlbg_default_value_range_1', 32),
    ('ContextMgmt_param_qlbg_default_value_range_2', 32),
    ('ContextMgmt_param_qlbg_default_value_range_3', 32),
    ('ContextMgmt_param_qlbg_default_value_range_4', 32),
    ('ContextMgmt_param_qlbg_default_value_range_5', 32),
    ('ContextMgmt_param_qlbg_default_value_range_6', 32),
    ('ContextMgmt_param_qlbg_default_value_range_7', 32),
    ('ContextMgmt_param_qlbg_default_value_range_8', 32),
    ('ContextMgmt_param_qlbg_ql_integration_per_datum', 8),
    ('ContextMgmt_param_qlbg_compression_scheme_counts', 7),
    ('ContextMgmt_param_qlbg_compression_scheme_triggers', 7),
    ('ContextMgmt_param_qlbg_energy_bin_edge_mask_upper_bit', 1),
    ('ContextMgmt_param_qlbg_energy_bin_edge_mask_lower_bits', 32),
    ('ContextMgmt_param_qllc_energy_bin_edge_mask_upper_bit', 1),
    ('ContextMgmt_param_qllc_energy_bin_edge_mask_lower_bits', 32),
    ('ContextMgmt_param_qllc_enable_tm', 1),
    ('ContextMgmt_param_qllc_ql_integration_per_datum', 8),
    ('ContextMgmt_param_qllc_compression_scheme_counts', 7),
    ('ContextMgmt_param_qllc_compression_scheme_triggers', 7),
    ('ContextMgmt_param_qllc_detemask', 32),
    ('ContextMgmt_param_qllc_pixemask', 12),
    ('ContextMgmt_param_qlfdet_pixemask', 12),
    ('ContextMgmt_param_qlfdet_thermal_energy_mask', 32),
    ('ContextMgmt_param_qlfdet_nonthermal_energy_mask', 32),
    ('ContextMgmt_param_qlfdet_kb', 32),
    ('ContextMgmt_param_qlfdet_thermal_factor_rcr1', 32),
    ('ContextMgmt_param_qlfdet_thermal_factor_rcr2', 32),
    ('ContextMgmt_param_qlfdet_thermal_factor_rcr3', 32),
    ('ContextMgmt_param_qlfdet_thermal_factor_rcr4', 32),
    ('ContextMgmt_param_qlfdet_thermal_factor_rcr5', 32),
    ('ContextMgmt_param_qlfdet_thermal_factor_rcr6', 32),
    ('ContextMgmt_param_qlfdet_thermal_factor_rcr7', 32),
    ('ContextMgmt_param_qlfdet_thermal_factor_rcr8', 32),
    ('ContextMgmt_param_qlfdet_nonthermal_factor_rcr1', 32),
    ('ContextMgmt_param_qlfdet_nonthermal_factor_rcr2', 32),
    ('ContextMgmt_param_qlfdet_nonthermal_factor_rcr3', 32),
    ('ContextMgmt_param_qlfdet_nonthermal_factor_rcr4', 32),
    ('ContextMgmt_param_qlfdet_nonthermal_factor_rcr5', 32),
    ('ContextMgmt_param_qlfdet_nonthermal_factor_rcr6', 32),
    ('ContextMgmt_param_qlfdet_nonthermal_factor_rcr7', 32),
    ('ContextMgmt_param_qlfdet_nonthermal_factor_rcr8', 32),
    ('ContextMgmt_param_qlfdet_k', 32), ('ContextMgmt_param_qlfdet_kp', 32),
    ('ContextMgmt_param_qlfdet_kpp', 32),
    ('ContextMgmt_param_qlfdet_timescale_short', 16),
    ('ContextMgmt_param_qlfdet_timescale_long', 16),
    ('ContextMgmt_param_qlfdet_init_thermal_cbc', 32),
    ('ContextMgmt_param_qlfdet_init_nonthermal_cbc', 32),
    ('ContextMgmt_param_qlfdet_cfmin', 32),
    ('ContextMgmt_param_qlfdet_threshold_thermal_B1', 32),
    ('ContextMgmt_param_qlfdet_threshold_thermal_C1', 32),
    ('ContextMgmt_param_qlfdet_threshold_thermal_M1', 32),
    ('ContextMgmt_param_qlfdet_threshold_thermal_X1', 32),
    ('ContextMgmt_param_qlfdet_threshold_nonthermal_weak', 32),
    ('ContextMgmt_param_qlfdet_threshold_nonthermal_significant', 32),
    ('ContextMgmt_param_qlfdetfloc_enable_tm', 1),
    ('ContextMgmt_param_qlfdet_ql_integration_per_datum', 8),
    ('ContextMgmt_param_qlffloc_ql_integration_per_datum', 8),
    ('ContextMgmt_param_qlfloc_dete_mask', 32),
    ('ContextMgmt_param_qlfloc_energy_mask', 32),
    ('ContextMgmt_param_qlfloc_sky_table_id', 16),
    ('ContextMgmt_param_qlfloc_L1', 32), ('ContextMgmt_param_qlfloc_L2', 32),
    ('ContextMgmt_param_qlfloc_k', 8), ('ContextMgmt_param_qlfloc_kp', 8),
    ('ContextMgmt_param_qlfloc_kpp', 16), ('ContextMgmt_param_qlfloc_kppp', 8),
    ('ContextMgmt_param_qlfloc_k0', 8), ('ContextMgmt_param_qlfloc_k1', 8),
    ('ContextMgmt_param_qlfloc_k2', 8), ('ContextMgmt_param_qlfloc_dx', 3),
    ('ContextMgmt_param_qlfloc_dy', 3),
    ('ContextMgmt_param_qldmon_active_detector_mask', 32),
    ('ContextMgmt_param_qldmon_energy_mask', 32),
    ('ContextMgmt_param_qldmon_ql_integration_per_datum', 8),
    ('ContextMgmt_param_qldmon_kbad', 8), ('ContextMgmt_param_qldmon_rbad',
                                           32),
    ('ContextMgmt_param_qldmon_nbad', 4), ('ContextMgmt_param_qldmon_nrep', 4),
    ('ContextMgmt_param_qlsp_detemask', 32),
    ('ContextMgmt_param_qlsp_pixemask', 32),
    ('ContextMgmt_param_qlsp_ql_integrations_per_datum', 8),
    ('ContextMgmt_param_qlsp_enable_tm', 1),
    ('ContextMgmt_param_qlsp_compression_scheme_counts', 7),
    ('ContextMgmt_param_qlsp_compression_scheme_triggers', 7),
    ('ContextMgmt_param_qlvar_detemask', 32),
    ('ContextMgmt_param_qlvar_enemask', 32),
    ('ContextMgmt_param_qlvar_pixemask', 12),
    ('ContextMgmt_param_qlvar_enable_tm', 1),
    ('ContextMgmt_param_qlvar_compression_scheme_counts', 7),
    ('ContextMgmt_param_qlrcr_enabled', 1),
    ('ContextMgmt_param_qlrcr_group_mask', 16),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr0', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr1', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr2_north', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr2_south', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr3_north_1', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr3_north_2', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr3_south_1', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr3_south_2', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr4_north_1', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr4_north_2', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr4_north_3', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr4_north_4', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr4_south_1', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr4_south_2', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr4_south_3', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr4_south_4', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr5', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr6_1', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr6_2', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr7_1', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr7_2', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr7_3', 13),
    ('ContextMgmt_param_qlrcr_pixelmask_rcr7_4', 13),
    ('ContextMgmt_param_qlrcr_regime2state_lut', 24),
    ('ContextMgmt_param_qlrcr_bckg_pixel_mask_rcr0', 13),
    ('ContextMgmt_param_qlrcr_bckg_pixel_mask_rcr1', 13),
    ('ContextMgmt_param_qlrcr_bckg_pixel_mask_rcr2', 13),
    ('ContextMgmt_param_qlrcr_bckg_pixel_mask_rcr3', 13),
    ('ContextMgmt_param_qlrcr_bckg_pixel_mask_rcr4', 13),
    ('ContextMgmt_param_qlrcr_bckg_pixel_mask_rcr5', 13),
    ('ContextMgmt_param_qlrcr_bckg_pixel_mask_rcr6', 13),
    ('ContextMgmt_param_qlrcr_bckg_pixel_mask_rcr7', 13),
    ('ContextMgmt_param_qlrcr_L0', 32), ('ContextMgmt_param_qlrcr_L1', 32),
    ('ContextMgmt_param_qlrcr_L2', 32), ('ContextMgmt_param_qlrcr_L3', 32),
    ('ContextMgmt_param_accum_max_duration', 16),
    ('ContextMgmt_param_accum_min_duration', 16),
    ('ContextMgmt_param_accum_max_counts', 32),
    ('ContextMgmt_param_accum_sum_e_mask', 32),
    ('ContextMgmt_param_accum_sum_d_mask', 32),
    ('ContextMgmt_param_data_level', 3),
    ('ContextMgmt_param_data_l0_dete_mask', 32),
    ('ContextMgmt_param_data_l0_pixe_mask', 12),
    ('ContextMgmt_param_data_l1_rcr1_pixe_mask', 12),
    ('ContextMgmt_param_data_l1_rcr2_pixe_mask', 12),
    ('ContextMgmt_param_data_l1_rcr3_pixe_mask', 12),
    ('ContextMgmt_param_data_l1_rcr4_pixe_mask', 12),
    ('ContextMgmt_param_data_l1_rcr5_pixe_mask', 12),
    ('ContextMgmt_param_data_l1_rcr6_pixe_mask', 12),
    ('ContextMgmt_param_data_l1_rcr7_pixe_mask', 12),
    ('ContextMgmt_param_data_l1_rcr8_pixe_mask', 12),
    ('ContextMgmt_param_data_l2_rcr1_pixe_mask1', 12),
    ('ContextMgmt_param_data_l2_rcr1_pixe_mask2', 12),
    ('ContextMgmt_param_data_l2_rcr1_pixe_mask3', 12),
    ('ContextMgmt_param_data_l2_rcr1_pixe_mask4', 12),
    ('ContextMgmt_param_data_l2_rcr1_pixe_mask5', 12),
    ('ContextMgmt_param_data_l2_rcr2_pixe_mask1', 12),
    ('ContextMgmt_param_data_l2_rcr2_pixe_mask2', 12),
    ('ContextMgmt_param_data_l2_rcr2_pixe_mask3', 12),
    ('ContextMgmt_param_data_l2_rcr2_pixe_mask4', 12),
    ('ContextMgmt_param_data_l2_rcr2_pixe_mask5', 12),
    ('ContextMgmt_param_data_l2_rcr3_pixe_mask1', 12),
    ('ContextMgmt_param_data_l2_rcr3_pixe_mask2', 12),
    ('ContextMgmt_param_data_l2_rcr3_pixe_mask3', 12),
    ('ContextMgmt_param_data_l2_rcr3_pixe_mask4', 12),
    ('ContextMgmt_param_data_l2_rcr3_pixe_mask5', 12),
    ('ContextMgmt_param_data_l2_rcr4_pixe_mask1', 12),
    ('ContextMgmt_param_data_l2_rcr4_pixe_mask2', 12),
    ('ContextMgmt_param_data_l2_rcr4_pixe_mask3', 12),
    ('ContextMgmt_param_data_l2_rcr4_pixe_mask4', 12),
    ('ContextMgmt_param_data_l2_rcr4_pixe_mask5', 12),
    ('ContextMgmt_param_data_l2_rcr5_pixe_mask1', 12),
    ('ContextMgmt_param_data_l2_rcr5_pixe_mask2', 12),
    ('ContextMgmt_param_data_l2_rcr5_pixe_mask3', 12),
    ('ContextMgmt_param_data_l2_rcr5_pixe_mask4', 12),
    ('ContextMgmt_param_data_l2_rcr5_pixe_mask5', 12),
    ('ContextMgmt_param_data_l2_rcr6_pixe_mask1', 12),
    ('ContextMgmt_param_data_l2_rcr6_pixe_mask2', 12),
    ('ContextMgmt_param_data_l2_rcr6_pixe_mask3', 12),
    ('ContextMgmt_param_data_l2_rcr6_pixe_mask4', 12),
    ('ContextMgmt_param_data_l2_rcr6_pixe_mask5', 12),
    ('ContextMgmt_param_data_l2_rcr7_pixe_mask1', 12),
    ('ContextMgmt_param_data_l2_rcr7_pixe_mask2', 12),
    ('ContextMgmt_param_data_l2_rcr7_pixe_mask3', 12),
    ('ContextMgmt_param_data_l2_rcr7_pixe_mask4', 12),
    ('ContextMgmt_param_data_l2_rcr7_pixe_mask5', 12),
    ('ContextMgmt_param_data_l2_rcr8_pixe_mask1', 12),
    ('ContextMgmt_param_data_l2_rcr8_pixe_mask2', 12),
    ('ContextMgmt_param_data_l2_rcr8_pixe_mask3', 12),
    ('ContextMgmt_param_data_l2_rcr8_pixe_mask4', 12),
    ('ContextMgmt_param_data_l2_rcr8_pixe_mask5', 12),
    ('ContextMgmt_param_data_l3_rcr1_pixe_mask1', 12),
    ('ContextMgmt_param_data_l3_rcr1_pixe_mask2', 12),
    ('ContextMgmt_param_data_l3_rcr1_pixe_mask3', 12),
    ('ContextMgmt_param_data_l3_rcr1_pixe_mask4', 12),
    ('ContextMgmt_param_data_l3_rcr1_pixe_mask5', 12),
    ('ContextMgmt_param_data_l3_rcr2_pixe_mask1', 12),
    ('ContextMgmt_param_data_l3_rcr2_pixe_mask2', 12),
    ('ContextMgmt_param_data_l3_rcr2_pixe_mask3', 12),
    ('ContextMgmt_param_data_l3_rcr2_pixe_mask4', 12),
    ('ContextMgmt_param_data_l3_rcr2_pixe_mask5', 12),
    ('ContextMgmt_param_data_l3_rcr3_pixe_mask1', 12),
    ('ContextMgmt_param_data_l3_rcr3_pixe_mask2', 12),
    ('ContextMgmt_param_data_l3_rcr3_pixe_mask3', 12),
    ('ContextMgmt_param_data_l3_rcr3_pixe_mask4', 12),
    ('ContextMgmt_param_data_l3_rcr3_pixe_mask5', 12),
    ('ContextMgmt_param_data_l3_rcr4_pixe_mask1', 12),
    ('ContextMgmt_param_data_l3_rcr4_pixe_mask2', 12),
    ('ContextMgmt_param_data_l3_rcr4_pixe_mask3', 12),
    ('ContextMgmt_param_data_l3_rcr4_pixe_mask4', 12),
    ('ContextMgmt_param_data_l3_rcr4_pixe_mask5', 12),
    ('ContextMgmt_param_data_l3_rcr5_pixe_mask1', 12),
    ('ContextMgmt_param_data_l3_rcr5_pixe_mask2', 12),
    ('ContextMgmt_param_data_l3_rcr5_pixe_mask3', 12),
    ('ContextMgmt_param_data_l3_rcr5_pixe_mask4', 12),
    ('ContextMgmt_param_data_l3_rcr5_pixe_mask5', 12),
    ('ContextMgmt_param_data_l3_rcr6_pixe_mask1', 12),
    ('ContextMgmt_param_data_l3_rcr6_pixe_mask2', 12),
    ('ContextMgmt_param_data_l3_rcr6_pixe_mask3', 12),
    ('ContextMgmt_param_data_l3_rcr6_pixe_mask4', 12),
    ('ContextMgmt_param_data_l3_rcr6_pixe_mask5', 12),
    ('ContextMgmt_param_data_l3_rcr7_pixe_mask1', 12),
    ('ContextMgmt_param_data_l3_rcr7_pixe_mask2', 12),
    ('ContextMgmt_param_data_l3_rcr7_pixe_mask3', 12),
    ('ContextMgmt_param_data_l3_rcr7_pixe_mask4', 12),
    ('ContextMgmt_param_data_l3_rcr7_pixe_mask5', 12),
    ('ContextMgmt_param_data_l3_rcr8_pixe_mask1', 12),
    ('ContextMgmt_param_data_l3_rcr8_pixe_mask2', 12),
    ('ContextMgmt_param_data_l3_rcr8_pixe_mask3', 12),
    ('ContextMgmt_param_data_l3_rcr8_pixe_mask4', 12),
    ('ContextMgmt_param_data_l3_rcr8_pixe_mask5', 12),
    ('ContextMgmt_param_data_enable_bckg_dete_formatting', 1),
    ('ContextMgmt_param_data_enable_cfl_dete_formatting', 1),
    ('ContextMgmt_param_imaging_dete_mask', 32),
    ('ContextMgmt_param_imaging_trim_N', 8),
    ('ContextMgmt_param_imaging_trim_F', 8),
    ('ContextMgmt_param_imaging_bckg_determination', 1),
    ('ContextMgmt_param_spectro_dete_mask', 32),
    ('ContextMgmt_param_spectro_pixe_mask', 12),
    ('ContextMgmt_param_spectro_bckg_determination', 1),
    ('ContextMgmt_param_xray01_registers', 282),
    ('ContextMgmt_param_xray02_registers', 282),
    ('ContextMgmt_param_xray03_registers', 282),
    ('ContextMgmt_param_xray04_registers', 282),
    ('ContextMgmt_param_xray05_registers', 282),
    ('ContextMgmt_param_xray06_registers', 282),
    ('ContextMgmt_param_xray07_registers', 282),
    ('ContextMgmt_param_xray08_registers', 282),
    ('ContextMgmt_param_xray09_registers', 282),
    ('ContextMgmt_param_xray10_registers', 282),
    ('ContextMgmt_param_xray11_registers', 282),
    ('ContextMgmt_param_xray12_registers', 282),
    ('ContextMgmt_param_xray13_registers', 282),
    ('ContextMgmt_param_xray14_registers', 282),
    ('ContextMgmt_param_xray15_registers', 282),
    ('ContextMgmt_param_xray16_registers', 282),
    ('ContextMgmt_param_xray17_registers', 282),
    ('ContextMgmt_param_xray18_registers', 282),
    ('ContextMgmt_param_xray19_registers', 282),
    ('ContextMgmt_param_xray20_registers', 282),
    ('ContextMgmt_param_xray21_registers', 282),
    ('ContextMgmt_param_xray22_registers', 282),
    ('ContextMgmt_param_xray23_registers', 282),
    ('ContextMgmt_param_xray24_registers', 282),
    ('ContextMgmt_param_xray25_registers', 282),
    ('ContextMgmt_param_xray26_registers', 282),
    ('ContextMgmt_param_xray27_registers', 282),
    ('ContextMgmt_param_xray28_registers', 282),
    ('ContextMgmt_param_xray29_registers', 282),
    ('ContextMgmt_param_xray30_registers', 282),
    ('ContextMgmt_param_xray31_registers', 282),
    ('ContextMgmt_param_xray32_registers', 282),
    ('ContextMgmt_param_hk_period_sid2', 16),
    ('ContextMgmt_param_hk_period_sid4', 16),
    ('ContextMgmt_param_enabled_science_data_transfer', 32),
    ('ContextMgmt_param_elut_lut', 16), ('ContextMgmt_param_tlut1_lut', 16),
    ('ContextMgmt_param_tlut2_lut', 16),
    ('ContextMgmt_param_tlut_dete_quarter_mask', 4),
    ('ContextMgmt_param_tlut_number_of_temperatures_for_average', 8),
    ('ContextMgmt_param_compression_l1l2_counts', 7),
    ('ContextMgmt_param_compression_l1l2l3_triggers', 7),
    ('ContextMgmt_param_compression_l3_counts', 7),
    ('ContextMgmt_param_compression_spectro_counts', 7),
    ('ContextMgmt_param_tmmgmt_publishing_interval', 32),
    ('ContextMgmt_param_tmmgmt_corridor_t1', 32),
    ('ContextMgmt_param_tmmgmt_corridor_t2', 32),
    ('ContextMgmt_param_tmmgmt_corridor_m1', 32),
    ('ContextMgmt_param_tmmgmt_corridor_m2', 32),
    ('ContextMgmt_param_aspect_halves_power', 16),
    ('ContextMgmt_param_att_openned_motor', 2),
    ('ContextMgmt_param_calib_compression_schema', 7),
    ('ContextMgmt_param_calib_formatting_enabled', 1),
    ('ContextMgmt_param_calib_pixel_mask', 16),
    ('ContextMgmt_param_config_adc_enable_mask', 16),
    ('ContextMgmt_param_config_adc_mode_mask', 16),
    ('ContextMgmt_param_config_enabled_edac', 4),
    ('ContextMgmt_param_config_scrub_cache', 2),
    ('ContextMgmt_param_config_scrub_sdram', 2),
    ('ContextMgmt_param_config_spw_state', 2),
    ('ContextMgmt_param_detector_mask_l1', 32),
    ('ContextMgmt_param_detector_mask_l2', 32),
    ('ContextMgmt_param_detector_mask_l3', 32),
    ('ContextMgmt_param_detector_mask_l4', 32),
    ('ContextMgmt_param_edac_scrub_algo_cache_threshold_high', 32),
    ('ContextMgmt_param_edac_scrub_algo_cache_threshold_nom', 32),
    ('ContextMgmt_param_edac_scrub_algo_sdram_threshold_high', 32),
    ('ContextMgmt_param_edac_scrub_algo_sdram_threshold_nom', 32),
    ('ContextMgmt_param_edac_seu_report_period_s', 16),
    ('ContextMgmt_param_fdir_irq_counter_max_dataflash', 32),
    ('ContextMgmt_param_fdir_irq_counter_max_detector', 32),
    ('ContextMgmt_param_fdir_irq_counter_max_detector_ql', 32),
    ('ContextMgmt_param_fdir_irq_counter_max_spw', 32),
    ('ContextMgmt_param_flare_list_last_report_scet', 32),
    ('ContextMgmt_param_hk_tm_sid2_reporting_enabled', 1),
    ('ContextMgmt_param_hk_tm_sid4_reporting_enabled', 1),
    ('ContextMgmt_param_hv_reset_delay_from_flare', 16),
    ('ContextMgmt_param_lv_state', 1), ('ContextMgmt_param_mem_load_enabled',
                                        1),
    ('ContextMgmt_param_fdir_sw_psut_min', 12),
    ('ContextMgmt_param_ql_flaredet_dete_mask', 32),
    ('ContextMgmt_param_ql_spectrum_number_of_wait_iterations', 7),
    ('ContextMgmt_param_rcr_b0', 32),
    ('ContextMgmt_param_spw_time_code_reception_timeout_ms', 32),
    ('ContextMgmt_param_fdir_sw_psut_max', 12),
    ('ContextMgmt_param_flare_sel_period', 8),
    ('ContextMgmt_param_flare_sel_latency', 8),
    ('ContextMgmt_param_flare_sel_enabled', 1),
    ('ContextMgmt_param_flare_sel_start', 32),
    ('ContextMgmt_param_flare_sel_stop', 32),
    ('ContextMgmt_param_fs_rewrite_files_after_n_seus', 8),
    ('ContextMgmt_params_att_global_disable_flag', 8),
    ('ContextMgmt_params_asic_latency_delay', 8)
]

ASIC_REGISTERS = [
    'ContextMgmt_param_xray01_registers', 'ContextMgmt_param_xray02_registers',
    'ContextMgmt_param_xray03_registers', 'ContextMgmt_param_xray04_registers',
    'ContextMgmt_param_xray05_registers', 'ContextMgmt_param_xray06_registers',
    'ContextMgmt_param_xray07_registers', 'ContextMgmt_param_xray08_registers',
    'ContextMgmt_param_xray09_registers', 'ContextMgmt_param_xray10_registers',
    'ContextMgmt_param_xray11_registers', 'ContextMgmt_param_xray12_registers',
    'ContextMgmt_param_xray13_registers', 'ContextMgmt_param_xray14_registers',
    'ContextMgmt_param_xray15_registers', 'ContextMgmt_param_xray16_registers',
    'ContextMgmt_param_xray17_registers', 'ContextMgmt_param_xray18_registers',
    'ContextMgmt_param_xray19_registers', 'ContextMgmt_param_xray20_registers',
    'ContextMgmt_param_xray21_registers', 'ContextMgmt_param_xray22_registers',
    'ContextMgmt_param_xray23_registers', 'ContextMgmt_param_xray24_registers',
    'ContextMgmt_param_xray25_registers', 'ContextMgmt_param_xray26_registers',
    'ContextMgmt_param_xray27_registers', 'ContextMgmt_param_xray28_registers',
    'ContextMgmt_param_xray29_registers', 'ContextMgmt_param_xray30_registers',
    'ContextMgmt_param_xray31_registers', 'ContextMgmt_param_xray32_registers'
]

if __name__ == '__main__':
    print('number of parameters:')
    print(len(CONTEXT_PARAMETER_BIT_SIZE))