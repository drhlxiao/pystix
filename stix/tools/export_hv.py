import os
import sys
import argparse
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta

# --- Global Config ---
MONGO_URI = "mongodb://localhost:27017"
HV_THRESHOLD = 100
MAX_GAP_SECONDS = 300
DEFAULT_START = datetime(2020, 4, 1, tzinfo=timezone.utc)

client = MongoClient(MONGO_URI)
col = client['stix']['packets']
monitor_col = client['stix']['hk_monitor']

look_back_weeks=3

def infer_time_range():
    """Infer start/end from last monitor run, or use defaults."""
    t_end = datetime.now(tz=timezone.utc) - timedelta(weeks=look_back_weeks)

    last_doc = list(monitor_col.find(
            {'event_type':'POSSIBLE_DET_DEPOL'},{}
    ).sort('run_metadata.run_time', -1).limit(1))

    try:
        t_start = last_doc[0]['run_metadata']['data_time_range']['end']
        if t_start.tzinfo is None:
            t_start = t_start.replace(tzinfo=timezone.utc)
    except Exception as e:
        raise e
        print(e)
        print('Default start time instead')
        t_start = DEFAULT_START

    return t_start, t_end


def get_utc_str(header):
    utc_val = header.get('UTC')
    if utc_val:
        return utc_val
    return datetime.fromtimestamp(header['unix_time'], tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def main(start_utc=None, end_utc=None):
    # --- 1. Determine Time Range ---
    if start_utc is None or end_utc is None:
        inferred_start, inferred_end = infer_time_range()
        
        t_start_global = start_utc if start_utc is not None else inferred_start
        t_end_global = end_utc if end_utc is not None else inferred_end
    else:
        t_start_global = start_utc
        t_end_global = end_utc

    # Ensure timezone awareness
    if t_start_global.tzinfo is None:
        t_start_global = t_start_global.replace(tzinfo=timezone.utc)
    if t_end_global.tzinfo is None:
        t_end_global = t_end_global.replace(tzinfo=timezone.utc)

    print(f"Processing range: {t_start_global.isoformat()} -> {t_end_global.isoformat()}")

    if t_start_global >= t_end_global:
        print("No new data to process. Exiting.")
        return 0

    # --- 2. Run Metadata ---

    # --- 3. State ---
    last_hash, last_unix_time, last_utc_time = None, None, None
    hv_was_low, hv_low_start, hv_low_start_utc = False, None, None
    current_batch_start = t_start_global
    total_inserted = 0

    # --- 4. Processing Loop ---
    while current_batch_start < t_end_global:
        current_batch_end = min(current_batch_start + relativedelta(months=1), t_end_global)
        print(f"Processing: {current_batch_start.strftime('%B %Y')}...")

        batch_docs = []
        run_metadata = {
            'data_time_range': {
                'start': current_batch_start,
                'end': current_batch_end,
            },
            
            'hv_thr':HV_THRESHOLD,
            'max_gap_sec':MAX_GAP_SECONDS,
            'run_time': datetime.now(tz=timezone.utc)
        }

        query = {
            'header.SPID': 54102,
            'header.unix_time': {
                '$gte': current_batch_start.timestamp(),
                '$lt': current_batch_end.timestamp()
            }
        }
        cursor = col.find(query, {'header': 1, 'parameters': 1, 'hash': 1}).sort('header.unix_time', 1)

        for doc in cursor:
            header = doc['header']
            u_time = header['unix_time']
            utc_time = get_utc_str(header)
            h_val = doc.get('hash')

            if h_val == last_hash:
                continue
            last_hash = h_val

            # Gap Detection
            if last_unix_time is not None and (u_time - last_unix_time) > MAX_GAP_SECONDS:
                batch_docs.append({
                    'event_subtype': 'DATA_GAP',
                    'event_type': 'POSSIBLE_DET_DEPOL',
                    'start_time': last_unix_time,
                    'end_time': u_time,
                    'start_time_utc': last_utc_time,
                    'end_time_utc': utc_time,
                    'hv1': None,
                    'hv2': None,
                    'duration_sec': u_time - last_unix_time,
                    'run_metadata': run_metadata
                })
                hv_was_low = False

            # HV Analysis
            params = doc.get('parameters', [])
            if len(params) > 36:
                hv1, hv2 = abs(params[34][2]), abs(params[36][2])

                if hv1 < HV_THRESHOLD:
                    if not hv_was_low:
                        hv_low_start, hv_low_start_utc, hv_was_low = u_time, utc_time, True
                elif hv_was_low:
                    duration = u_time - hv_low_start
                    if duration >= MAX_GAP_SECONDS:
                        batch_docs.append({
                            'event_subtype': 'HV_LOW',
                            'start_time': hv_low_start,
                            'event_type': 'POSSIBLE_DET_DEPOL',
                            'end_time': u_time,
                            'start_time_utc': hv_low_start_utc,
                            'end_time_utc': utc_time,
                            'hv1': hv1,
                            'hv2': hv2,
                            'duration_sec': duration,
                            'run_metadata': run_metadata
                        })
                    hv_was_low = False

            last_unix_time, last_utc_time = u_time, utc_time

        # --- 5. Write batch to MongoDB ---
        if batch_docs:
            monitor_col.insert_many(batch_docs)
            total_inserted += len(batch_docs)
            print(f"   -> Inserted {len(batch_docs)} events for this month.")

        current_batch_start = current_batch_end

    print(f"Finished. Total events inserted: {total_inserted}")
    return total_inserted


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run HK monitor event detection.")
    parser.add_argument(
        "--start", type=str, default=None,
        help="Start time in ISO 8601 format, e.g. 2024-01-01T00:00:00Z"
    )
    parser.add_argument(
        "--end", type=str, default=None,
        help="End time in ISO 8601 format, e.g. 2024-06-01T00:00:00Z"
    )
    args = parser.parse_args()

    start_utc = datetime.fromisoformat(args.start.replace("Z", "+00:00")) if args.start else None
    end_utc = datetime.fromisoformat(args.end.replace("Z", "+00:00")) if args.end else None

    main(start_utc=start_utc, end_utc=end_utc)
