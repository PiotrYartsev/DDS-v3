#!/usr/bin/env python3
import argparse
import logging
from logging.handlers import RotatingFileHandler
import yaml
import sys
import os

from src.storage_interface import load_files_dump_from_RSE,generate_SQLite_database_for_temporal_check,temporal_check,write_report
from src.log_config import logger

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
    output_dir="output" or config['reporting']['output_dir'] 

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

        
        logger.info("Report generation placeholder - not yet implemented")
    except Exception as e:
        logger.exception("An unexpected error occurred")
        sys.exit(f"An unexpected error occurred: {e}")

    #if the database for the temporal check is not found, generate it
    try:
        if not os.path.exists(config['temporal_check']['database_file']+ ".db"):
            logger.info("Database for temporal check not found. Generating it")
            generate_SQLite_database_for_temporal_check(config['temporal_check']['database_file'])
        else:
            logger.info("Database for temporal check found")
    except Exception as e:
        logger.exception("An unexpected error occurred with the temporal check database")
        sys.exit(f"An unexpected error occurred: {e}")
    
    try:
        #perform the temporal check
        missing_data_over_days_between_checks, dark_data_over_days_between_checks=temporal_check(config['temporal_check']['database_file'], args.rse , missing_data,  dark_data, config['temporal_check']['days_between_checks'])
    except Exception as e:
        logger.exception("An unexpected error occurred with the temporal check")
        sys.exit(f"An unexpected error occurred: {e}")
    if len(missing_data_over_days_between_checks) == 0:
        logger.info("No missing data found after the temporal check")
    else:
        logger.info("Writing the report in the format specified: {}".format(output_format))
        logger.info("Writing missing data")
        try:
            write_report(missing_data_over_days_between_checks, args.rse, "missing_data", output_format,output_dir)
        except  Exception as e:
            logger.exception("An unexpected error occurred with the writing of the missing data report")
            sys.exit(f"An unexpected error occurred: {e}")
    if len(dark_data_over_days_between_checks) == 0:
        logger.info("No dark data found after the temporal check")
    else:    
        try:
            logger.info("Writing dark data")
            write_report(dark_data_over_days_between_checks, args.rse, "dark_data", output_format,output_dir)
        except Exception as e:
            logger.exception("An unexpected error occurred with the writing of the dark data report")
            sys.exit(f"An unexpected error occurred: {e}")
 



    # TODO: Generate and output the report
        # report = generate_report(dark_data, missing_data, args.rse, output_format)



    #TODO: add GRIDFTP address correction
    #TODO: make the output report
    #       make it work with the output format
    
    #TODO: make the optimization changes
    # implement multithreading
    # implement the chunk loading of the files

    #TODO: make the mock Rucio mode work 

    #TODO: Make the debug mode work
    
    #TODO: Make the real Rucio mode work NOTE: this requires me to contact Lene, maybe Florido

    #TODO: Implement replicas check
    #       check if the replicas are in the same RSE
    #       check if the replicas are in another RSE 
    #       mark the file as it can be restored

    #TODO: Implement the duplicate files search among the dark data. 
    logger.info("Dark Data Search completed successfully")

if __name__ == "__main__":
    main()