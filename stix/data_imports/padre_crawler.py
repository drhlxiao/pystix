"""
PADRE Data Crawler and MongoDB Integration
Crawls PADRE MEDDEA spectrum data and stores it in MongoDB
"""

import pickle
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dateutil.relativedelta import relativedelta
import pymongo
import requests
import numpy as np
import os
import pandas as pd
from datetime import datetime, date
from dateutil import parser as dtparser
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import sys

# Add PADRE MEDDEA to path
sys.path.append('/home/xiaohl/FHNW/STIX/PADRE/padre_meddea/')
sys.path.append('/opt/stix/padre/padre_meddea/')
from padre_meddea.io import read_file

DOWNLOAD_DIR = '/data/padre'
def unix2datetime(t):
    dt=pd.to_datetime(t, unit='s', utc=True).to_pydatetime()
    return dt.replace(microsecond=int(dt.microsecond))

class PADRECrawler:
    """Class for crawling and managing PADRE MEDDEA spectrum data"""
    
    BASE_URL = "https://umbra.nascom.nasa.gov/padre/padre-meddea/l0/spectrum/"
    
    def __init__(self):
        """
        Initialize PADRE crawler
        
        Parameters:
        -----------
        mongo_host : str
            MongoDB host address
        mongo_db : str
            MongoDB database name
        mongo_collection : str
            MongoDB collection name
        """
        # Setup MongoDB connection
        self.mongo_client = pymongo.MongoClient('localhost')
        self.db = self.mongo_client['stix']['padre']
        
        # Setup requests session
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        if hasattr(self, 'session'):
            self.session.close()
        if hasattr(self, 'mongo_client'):
            self.mongo_client.close()
    
    def list_dirs(self, url, length=None):
        """
        List directories from a URL
        
        Parameters:
        -----------
        url : str
            URL to list directories from
        length : int, optional
            Filter directories by name length
            
        Returns:
        --------
        list : List of directory names
        """
        r = self.session.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        dirs = []
        for a in soup.find_all("a", href=True):
            href = a["href"]

            if not href.endswith("/"):
                continue
            if href in ("../",):
                continue

            name = href.strip("/")

            if length is not None and len(name) != length:
                continue
            if not name.isdigit():
                continue

            dirs.append(name)

        return dirs
    
    def list_files(self, url):
        """
        List files from a URL
        
        Parameters:
        -----------
        url : str
            URL to list files from
            
        Returns:
        --------
        list : List of filenames
        """
        r = self.session.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        files = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.endswith("/") or href.startswith("?") or href == "../":
                continue
            files.append(href)

        return files
    

    def crawl_recent(self, nmon=2):
        """
        Crawl recent PADRE data from the last N months
        
        Parameters:
        -----------
        nmon : int
            Number of months to look back
            
        Returns:
        --------
        list : List of dictionaries containing file information
        """
        today = date.today()
        start = today - relativedelta(months=nmon)

        results = []

        # Years that could possibly be involved
        years = {today.year, start.year}

        for year in sorted(years):
            year_url = urljoin(self.BASE_URL, f"{year}/")

            try:
                months = self.list_dirs(year_url, length=2)
            except requests.RequestException:
                continue

            for month in months:
                y, m = int(year), int(month)

                # Month-level filter
                if date(y, m, 1) < date(start.year, start.month, 1):
                    continue
                if date(y, m, 1) > date(today.year, today.month, 1):
                    continue

                month_url = urljoin(year_url, f"{month}/")

                try:
                    days = self.list_dirs(month_url, length=2)
                except requests.RequestException:
                    continue

                for day in days:
                    d = int(day)
                    try:
                        day_date = date(y, m, d)
                    except ValueError:
                        continue

                    if not (start <= day_date <= today):
                        continue

                    day_url = urljoin(month_url, f"{day}/")

                    try:
                        files = self.list_files(day_url)
                    except requests.RequestException:
                        continue

                    for f in files:
                        results.append({
                            "date": day_date,
                            "filename": f,
                            "url": urljoin(day_url, f),
                        })

        return results
    
    def parse_raw_spectrum(self, spec_list):
        """
        Plot PADRE spectrogram
        
        Parameters:
        -----------
        spec_list : object
            PADRE spectrogram data object
        show_plot : bool
            Whether to display the plot
            
        Returns:
        --------
        tuple : (image array, times array)
        """
        # Get and prepare the PADRE data
        times = spec_list.spectrogram()['time']
        times_floats = times[:].unix
        times_dt = [unix2datetime(t) for t in times_floats]

        im = spec_list.spectrogram()['specgram']
        #g = (347 - 144) / 50  # ADC_channels/keV
        #o = 144 - g * 31      # ADC_channels
        ## ADC_Ch = g*E[keV] + o
        #ee = (np.arange(512) - o) / g
        #
        #     cut_pos = np.where(ee >= 0)[0]
        #ee = ee[cut_pos]
        #im = im[:, cut_pos]
        #gain = (4.06 -31)* e +144
        
        

        return im, times
    
    def file_exists_in_mongo(self, filename):

        filename_no_ext = os.path.splitext(filename)[0]
        return self.db.find_one({"filename": filename_no_ext}) is not None
    
    def download_file(self, url, local_path):

        try:
            print(f"Downloading {url}...")
            r = self.session.get(url, timeout=30)
            r.raise_for_status()
            
            with open(local_path, 'wb') as f:
                f.write(r.content)
            
            return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False
    
    def parse_and_write_to_mongo(self, filename, file_url=None, download_dir= DOWNLOAD_DIR):

        # Extract just the filename for MongoDB lookup
        base_filename = os.path.basename(filename)
        
        # Check if file already exists in MongoDB
        if self.file_exists_in_mongo(base_filename):
            print(f"File {base_filename} already exists in MongoDB, skipping...")
            return False
        
        # Determine local file path
        if file_url and not os.path.exists(filename):
            # Need to download the file
            os.makedirs(download_dir, exist_ok=True)
            local_path = os.path.join(download_dir, base_filename)
            
            if not self.download_file(file_url, local_path):
                return False
            
            should_cleanup = True
        else:
            # File already exists locally
            local_path = filename
            should_cleanup = False
        
        try:
            # Read and process the file
            print(f"Processing {base_filename}...")
            hdu = read_file(local_path)
            im, times = self.parse_raw_spectrum(hdu)
            
            base_filename_no_ext = os.path.splitext(base_filename)[0]
            # Prepare document for MongoDB
            doc = {
                "filename": base_filename_no_ext,
                "url": file_url,
                "creation_time": datetime.now(),
                #"times": times[:].unix.tolist() if hasattr(times[:], 'unix') else times.tolist(),
                #"spectrogram": im.value.tolist() if hasattr(im, 'value') else im.tolist(),
                "time_start": times[0].unix if hasattr(times[0], 'unix') else times[0],
                "time_end": times[-1].unix if hasattr(times[-1], 'unix') else times[-1],
            }

            
            
            # Insert into MongoDB
            self.db.insert_one(doc)
            print(f"Successfully inserted {base_filename} into MongoDB")
            doc["times"] = times[:].unix.tolist() if hasattr(times[:], 'unix') else times.tolist()
            doc["spectrogram"] = im.value.tolist() if hasattr(im, 'value') else im.tolist()
            pkl_fname = os.path.join(download_dir, base_filename_no_ext+'.pkl')
            print(pkl_fname)
            with open(pkl_fname,'wb') as f:
                pickle.dump(doc,f)


            # Clean up downloaded file if needed
            if should_cleanup:
                os.remove(local_path)
            
            return True
            
        except Exception as e:
            print(f"Error processing {base_filename}: {e}")
            
            # Clean up downloaded file if needed
            if should_cleanup and os.path.exists(local_path):
                os.remove(local_path)
            
            return False
    
    def crawl_recent_and_parse(self, nmon=2, download_dir=DOWNLOAD_DIR):
        """
        Crawl recent PADRE data and write to MongoDB if not already present
        
        Parameters:
        -----------
        nmon : int
            Number of months to look back
        download_dir : str
            Directory to download files to
            
        Returns:
        --------
        dict : Statistics about the crawl
        """
        import os
        
        # Create download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)
        
        # Crawl recent files
        print(f"Crawling PADRE data from the last {nmon} months...")
        files = self.crawl_recent(nmon=nmon)
        print(f"Found {len(files)} files")
        
        stats = {
            "total_files": len(files),
            "already_in_db": 0,
            "successfully_added": 0,
            "errors": 0
        }
        
        for file_info in files:
            filename = file_info['filename']
            url = file_info['url']
            
            # parse_and_write_to_mongo will check if file exists and download if needed
            result = self.parse_and_write_to_mongo(
                filename=filename,
                file_url=url,
                download_dir=download_dir
            )
            
            if result is False:
                # Check if it was skipped because already in DB
                if self.file_exists_in_mongo(filename):
                    stats["already_in_db"] += 1
                else:
                    stats["errors"] += 1
            else:
                stats["successfully_added"] += 1
        
        return stats


def main(nmon=2):
    """Main function to run the PADRE crawler"""
    print("PADRE Data Crawler and MongoDB Integration")
    print("=" * 50)
    
    # Initialize crawler
    crawler = PADRECrawler()
    
    # Crawl recent data and update MongoDB
    stats = crawler.crawl_recent_and_parse(nmon)
    
    print("\nCrawl Statistics:")
    print(f"  Total files found: {stats['total_files']}")
    print(f"  Already in database: {stats['already_in_db']}")
    print(f"  Successfully added: {stats['successfully_added']}")
    print(f"  Errors: {stats['errors']}")
    print("\nDone!")


if __name__ == "__main__":
    main()
