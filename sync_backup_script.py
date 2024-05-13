import os
import sys
import shutil
import time
import hashlib
import argparse


def sync_folders(source_path, replica_path, log_file):
    # Ensure replica folder exists
    if not os.path.exists(replica_path):
        os.makedirs(replica_path)

    # Walk through the source folder
    for root, _, files in os.walk(source_path):
        for file in files:
            source_file_path = os.path.join(root, file)
            replica_file_path = os.path.join(replica_path, os.path.relpath(source_file_path, source_path))

            # Check if file exists in replica folder
            if not os.path.exists(replica_file_path):
                shutil.copy2(source_file_path, replica_file_path)
                log(log_file, f"Copied {source_file_path} to {replica_file_path}")
            else:
                # Check if file content is different
                if file_hash(source_file_path) != file_hash(replica_file_path):
                    shutil.copy2(source_file_path, replica_file_path)
                    log(log_file, f"Updated {replica_file_path} from {source_file_path}")

    # Check for files in replica folder that don't exist in source folder
    for root, _, files in os.walk(replica_path):
        for file in files:
            replica_file_path = os.path.join(root, file)
            source_file_path = os.path.join(source_path, os.path.relpath(replica_file_path, replica_path))

            if not os.path.exists(source_file_path):
                os.remove(replica_file_path)
                log(log_file, f"Removed {replica_file_path}")


def file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def log(log_file, message):
    with open(log_file, 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder synchronization program")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("replica", help="Replica folder path")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log", help="Log file path")
    args = parser.parse_args()

    source_path = args.source
    replica_path = args.replica
    sync_interval = args.interval
    log_file = args.log

    while True:
        sync_folders(source_path, replica_path, log_file)
        time.sleep(sync_interval)