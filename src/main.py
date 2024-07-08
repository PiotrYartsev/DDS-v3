#!/usr/bin/env python3
import argparse
import logging
from logging.handlers import RotatingFileHandler
import yaml
import sys
import os

from src.storage_interface import load_files_dump_from_RSE,generate_SQLite_database_for_temporal_check 
from src.log_config import logger
# TODO: Uncomment these imports when the modules are implemented
"""
from src.rucio_interface import get_rucio_files
from src.storage_interface import get_storage_files
from src.comparison_engine import compare_files
from src.report_generator import generate_report
"""

def parse_arguments():
    """
    Parse command line arguments for the Dark Data Search toolkit.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Dark Data Search toolkit, version 3, developed for the search and analysis of dark data at LDCS/LDMX.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--rse', required=True, help='RSE to use for the dark data search')
    parser.add_argument('--threads', type=int, help='Number of threads to use')
    parser.add_argument('--output-format', choices=['json', 'csv', 'txt'], help='Output format for the report')
    return parser.parse_args()

def load_config():
    """
    Load the configuration from the 'config/config.yaml' file.

    Returns:
        dict: The loaded configuration as a dictionary.

    Raises:
        FileNotFoundError: If the 'config.yaml' file is not found in the config directory.
        yaml.YAMLError: If there is an error parsing the 'config.yaml' file.
    """
    try:
        with open('config/config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config.yaml not found in the config directory.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing config.yaml: {e}")
        sys.exit(1)

def main():
    """
    Entry point of the Dark Data Search application.
    
    This function loads the configuration, parses command line arguments, and performs the dark data search.
    It loads the RSE and Rucio dump files, finds the dark data and missing data, and generates a report.
    """
    config = load_config()
    
    logger.info("Starting Dark Data Search")
    
    args = parse_arguments()
    logger.info(f"Arguments parsed: RSE={args.rse}, threads={args.threads}, output_format={args.output_format}")

    # Use config values, but override with command line arguments if provided
    threads = args.threads or config['performance']['default_threads']
    output_format = args.output_format or config['reporting']['default_format']
    logger.info(f"Using {threads} threads and {output_format} output format")

    try:
        # Load the RSE and Rucio dump files
        rse_files = load_files_dump_from_RSE('rsedump', args.rse, logger)
        rucio_files = load_files_dump_from_RSE('ruciodump', args.rse, logger)

        logger.info(f"RSE files: {len(rse_files)}")
        logger.info(f"Rucio files: {len(rucio_files)}")

        # Find the dark data and missing data
        dark_data = rse_files - rucio_files
        missing_data = rucio_files - rse_files

        logger.info(f"Dark data: {len(dark_data)}")
        logger.info(f"Missing data: {len(missing_data)}")

        # TODO: Generate and output the report
        # report = generate_report(dark_data, missing_data, args.rse, output_format)
        logger.info("Report generation placeholder - not yet implemented")
    except Exception as e:
        logger.exception("An unexpected error occurred")
        sys.exit(f"An unexpected error occurred: {e}")

    #if the database for the temporal check is not found, generate it
    try:
        if not os.path.exists(config['temporal_check']['database_file']):
            generate_SQLite_database_for_temporal_check(config['temporal_check']['database_file'])
    
    except Exception as e:
        logger.exception("An unexpected error occurred")
        sys.exit(f"An unexpected error occurred: {e}")
    

    logger.info("Dark Data Search completed successfully")

if __name__ == "__main__":
    main()