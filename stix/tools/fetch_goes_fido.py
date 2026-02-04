import numpy as np
import pandas as pd
from sunpy import timeseries as ts
from sunpy.net import Fido
from sunpy.net import attrs as a
from datetime import datetime, timedelta
import pymongo
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Adjust connection string as needed
db = client['stix']
collection = db['goes_fluxes']

# Time range
tstart = datetime.strptime("2025-07-31 07:06", "%Y-%m-%d %H:%M")
tend = datetime.strptime("2025-08-21 19:25", "%Y-%m-%d %H:%M")

# 8-hour window
window_hours = 8
window_delta = timedelta(hours=window_hours)

current_start = tstart
while current_start < tend:
    # Calculate end time for current window
    current_end = min(current_start + window_delta, tend)
    
    print(f"Downloading data from {current_start} to {current_end}")
    
    try:
        # Search for data in current window
        result = Fido.search(
            a.Time(current_start.strftime("%Y-%m-%d %H:%M"), 
                   current_end.strftime("%Y-%m-%d %H:%M")), 
            a.Instrument("XRS"), 
            a.goes.SatelliteNumber(18), 
            a.Resolution('avg1m')
        )
        
        if len(result[0]) > 0:
            print(f"Found {len(result[0])} files")
            
            # Download the files
            goes_files = Fido.fetch(result)
            
            # Process each file
            for goes_file in goes_files:
                # Load the data
                flux = ts.TimeSeries(goes_file)
                df = flux.to_dataframe()
                df = df.reset_index()
                
                # Ensure the column is datetime type
                df['datetime'] = pd.to_datetime(df['index'])
                df['time_tag'] = df['datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S')
                df['unix_time'] = df['datetime'].astype('int64') // 10**9
                
                docs = []
                for idx, row in df.iterrows():
                    # XRSA channel (0.05-0.4nm)
                    doc_a = {
                        "energy": "0.05-0.4nm",
                        "unix_time": int(row['unix_time']),
                        "flux": float(row['xrsa']),
                        "satellite": 18,
                        "time_tag": row['time_tag'],
                        'run_id':20250908,
                    }
                    docs.append(doc_a)
                    
                    # XRSB channel (0.1-0.8nm)
                    doc_b = {
                        "energy": "0.1-0.8nm",
                        "unix_time": int(row['unix_time']),
                        "flux": float(row['xrsb']),
                        "satellite": 18,
                        'run_id':20250908,
                        "time_tag": row['time_tag']
                    }
                    docs.append(doc_b)
                
                # Insert documents to MongoDB
                if docs:
                    try:
                        result_insert = collection.insert_many(docs)
                        print(f"Inserted {len(result_insert.inserted_ids)} documents to MongoDB")
                    except Exception as e:
                        print(f"Error inserting to MongoDB: {e}")
        else:
            print("No data found for this time window")
            
    except Exception as e:
        print(f"Error processing window {current_start} to {current_end}: {e}")
    
    # Move to next window
    current_start = current_end

print("Data download and MongoDB insertion completed!")

# Optional: Create index on unix_time for better query performance
#try:
#    collection.create_index("unix_time")
#    collection.create_index("energy")
#    print("Indexes created on unix_time and energy fields")
#except Exception as e:
#    print(f"Error creating indexes: {e}")

# Close MongoDB connection
client.close()
