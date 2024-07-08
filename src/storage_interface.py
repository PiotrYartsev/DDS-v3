import os
import sys
import sqlite3
from src.log_config import logger

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
