import os
import json
import argparse
from datetime import datetime

LOG_DIR = "logs/"

def parse_args():
    parser = argparse.ArgumentParser(description="Log Query Interface")
    parser.add_argument('--level', type=str, help='Filter by log level')
    parser.add_argument('--log_string', type=str, help='Search log string')
    parser.add_argument('--start_time', type=str, help='Start timestamp in ISO 8601 format (e.g., 2023-09-10T00:00:00Z)')
    parser.add_argument('--end_time', type=str, help='End timestamp in ISO 8601 format (e.g., 2023-09-15T23:59:59Z)')
    parser.add_argument('--source', type=str, help='Source log file')
    return parser.parse_args()

def is_within_time_range(timestamp, start_time, end_time):
    log_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if start_time and log_time < start_time:
        return False
    if end_time and log_time > end_time:
        return False
    return True

def search_logs(args):
    logs = []
    start_time = datetime.fromisoformat(args.start_time.replace("Z", "+00:00")) if args.start_time else None
    end_time = datetime.fromisoformat(args.end_time.replace("Z", "+00:00")) if args.end_time else None
    
    for log_file in os.listdir(LOG_DIR):
        if args.source and args.source != log_file:
            continue
        with open(os.path.join(LOG_DIR, log_file), 'r') as f:
            for line in f:
                log_entry = json.loads(line)
                if args.level and log_entry['level'] != args.level:
                    continue
                if args.log_string and args.log_string not in log_entry['log_string']:
                    continue
                if not is_within_time_range(log_entry['timestamp'], start_time, end_time):
                    continue
                logs.append(log_entry)
    return logs

if __name__ == '__main__':
    args = parse_args()
    result_logs = search_logs(args)
    for log in result_logs:
        print(json.dumps(log, indent=2))
