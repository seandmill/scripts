#!/usr/bin/env python3

# Use this script to analyze the contents of a directory and generate a CSV report.
# The report will include:
# - Full directory path
# - Directory level 1-5
# - Number of files
# - Directory size in MB
# - Last date created
# - Last date modified
# Place in the root directory you want to analyze.

import os
import csv
from datetime import datetime

def analyze_directory(path):
    """
    Recursively count files, total size, newest creation and modification times.
    """
    num_files = 0
    total_size = 0
    latest_ctime = 0
    latest_mtime = 0

    for root, _, files in os.walk(path):
        for fname in files:
            full = os.path.join(root, fname)
            try:
                st = os.stat(full)
            except OSError:
                continue
            num_files += 1
            total_size += st.st_size
            if st.st_ctime > latest_ctime:
                latest_ctime = st.st_ctime
            if st.st_mtime > latest_mtime:
                latest_mtime = st.st_mtime

    size_mb = total_size / (1024**2)
    created = datetime.fromtimestamp(latest_ctime).strftime("%Y-%m-%d %H:%M:%S") if latest_ctime else ""
    modified = datetime.fromtimestamp(latest_mtime).strftime("%Y-%m-%d %H:%M:%S") if latest_mtime else ""
    return num_files, round(size_mb,2), created, modified

def split_levels(path):
    """
    Strip leading slash, split into up to 5 segments, pad with empty strings.
    """
    parts = path.strip(os.sep).split(os.sep)
    segs = parts[:5] + [""]*(5 - len(parts[:5]))
    return segs

def main():
    root = os.getcwd()
    today = datetime.now().strftime("%Y%m%d")
    out = f"{os.getenv('USER')}_file_analysis_{today}.csv"

    with open(out, "w", newline="") as csvf:
        writer = csv.writer(csvf)
        writer.writerow([
            "full_directory_path",
            "directory_l1","directory_l2","directory_l3","directory_l4","directory_l5",
            "num_files","dir_size_in_mb","last_date_created","last_date_modified"
        ])

        for dirpath, dirnames, _ in os.walk(root):
            rel = os.path.relpath(dirpath, root)
            depth = 0 if rel == "." else rel.count(os.sep) + 1
            if depth > 5:
                dirnames[:] = []
                continue

            num, size, created, modified = analyze_directory(dirpath)
            full = os.path.abspath(dirpath)
            l1,l2,l3,l4,l5 = split_levels(full)
            writer.writerow([full, l1, l2, l3, l4, l5, num, size, created, modified])

    print(f"Analysis complete. Report saved to ./{out}")

if __name__ == "__main__":
    main()