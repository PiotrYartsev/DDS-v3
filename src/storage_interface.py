import os
import sys
import sqlite3
from src.log_config import logger
import datetime
import json


def load_files_dump_from_RSE(directory, rse_name, logger):
    logger.info(f"Loading dump from {directory} for RSE {rse_name}")
    if not os.path.exists(directory):
        logger.error(f"Error: '{directory}' directory not found.")
        sys.exit(f"Error: '{directory}' directory not found.")
    
    files = os.listdir(directory)
    if len(files) != 1:
        logger.error(f"Error: Expected 1 dump file in {directory}, found {len(files)}.")
        sys.exit(f"Error: Expected 1 dump file in {directory}, found {len(files)}.")
    
    dump_file = files[0]

    if not dump_file.split('-')[0]==rse_name:
        logger.error(f"Error: Dump file {dump_file} does not match RSE name {rse_name}.")
        sys.exit(f"Error: Dump file {dump_file} does not match RSE name {rse_name}.")
    
    with open(os.path.join(directory, dump_file), 'r') as f:
        file_set = set(f.read().splitlines())
    logger.info(f"Loaded {len(file_set)} files from {dump_file}")
    return file_set


def generate_SQLite_database_for_temporal_check(database_file):
    logger.info("Generating SQLite database for bad data")
    
    conn = sqlite3.connect(database_file+'.db')
    c = conn.cursor()
    conn.execute('''CREATE TABLE dark_data (file TEXT PRIMARY KEY, rse TEXT, timestamp TEXT)''')
    conn.execute('''CREATE TABLE missing_data (file TEXT PRIMARY KEY, rse TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

    logger.info("SQLite database generated successfully")

def temporal_check(database_file, rse,missing_data,  dark_data, days_between_checks):
    logger.info("Performing temporal check")
    conn = sqlite3.connect(database_file + '.db')
    conn.execute("PRAGMA journal_mode=WAL")  # Enable Write-Ahead Logging for better concurrency.
    conn.execute("BEGIN")  # Start a transaction
    c = conn.cursor()

    missing_data_over_days_between_checks = set()
    dark_data_over_days_between_checks = set()
    # Prepare the SELECT statement
    select_stmt_missing = "SELECT timestamp FROM missing_data WHERE file = ? and rse = ?"
    insert_stmt_missing = "INSERT INTO missing_data (file, rse, timestamp) VALUES (?, ?, ?)"
    delete_stmt_missing = "DELETE FROM missing_data WHERE file = ? and rse = ?"

    select_stmt_dark = "SELECT timestamp FROM dark_data WHERE file = ? and rse = ?"
    insert_stmt_dark = "INSERT INTO dark_data (file, rse, timestamp) VALUES (?, ?, ?)"
    delete_stmt_dark = "DELETE FROM dark_data WHERE file = ? and rse = ?"

    # Check each missing file
    for file in missing_data:
        c.execute(select_stmt_missing, (file, rse))
        row = c.fetchone()
        if row is None:
            c.execute(insert_stmt_missing, (file, rse, datetime.datetime.now().isoformat()))
        else:
            timestamp = datetime.datetime.fromisoformat(row[0])
            if (datetime.datetime.now() - timestamp).days > days_between_checks:
                c.execute(delete_stmt_missing, (file, rse))
                missing_data_over_days_between_checks.add(file)
    for file in dark_data:
        c.execute(select_stmt_dark, (file, rse))
        row = c.fetchone()
        if row is None:
            c.execute(insert_stmt_dark, (file, rse, datetime.datetime.now().isoformat()))
        else:
            timestamp = datetime.datetime.fromisoformat(row[0])
            if (datetime.datetime.now() - timestamp).days > days_between_checks:
                c.execute(delete_stmt_dark, (file, rse))
                dark_data_over_days_between_checks.add(file)
    
    conn.commit()
    conn.close()
    logger.info("Temporal check complete")
    return missing_data_over_days_between_checks, dark_data_over_days_between_checks


def write_report(report, rse, report_type, output_format, output_dir):
    logger.info(f"Writing report in {output_format} format")
    
    if output_format == 'json':
        # Construct the dictionary
        report_data = {
            "rse": rse,
            "date": datetime.datetime.now().isoformat(),
            "files": [{"name": item} for item in report]
        }

        # Write the dictionary to a file
        with open(f"{output_dir}/{report_type}_report.json", 'w') as f:
            json.dump(report_data, f, indent=4)
    elif output_format == 'txt':
        with open(output_dir+'/'+report_type+'_report.txt', 'w') as f:
            [f.write(item+'\n') for item in report]
            """elif output_format == 'csv':
                with open(output_dir+'/'+report_type+'_report.csv', 'w') as f:
                    [f.write(item+'\n') for item in report]"""
    
    else:
        logger.error(f"Error: Unknown output format {output_format}")
        sys.exit(f"Error: Unknown output format {output_format}")
    logger.info("Report written successfully")