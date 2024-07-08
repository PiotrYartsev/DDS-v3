# Dark Data Search Toolkit v3 (DDS-v3)

## Overview

The Dark Data Search Toolkit v3 (DDS-v3) is an advanced tool designed to identify discrepancies between data registered in Rucio and data actually present in storage. It efficiently detects dark data (files in storage but not in Rucio) and missing data (files in Rucio but not in storage) across entire Rucio Storage Elements (RSEs).

## Features

- Full RSE scanning capability
- Efficient set-based comparison algorithms
- Multithreaded processing for improved performance
- Flexible output formats (JSON, CSV)
- Optimized for large-scale storage systems

## Parameters

- --rse: (Mandatory) Specifies the Rucio Storage Element to analyze
- --threads: (Optional) Number of threads for parallel processing (default: 1)
- --output-format: (Optional) Desired format for results (default: JSON)

## Output
The tool generates a report containing:

- List of dark data files
- List of missing files
- Summary statistics

## Requirements

- Python 3.7+
- Rucio client library
- Access to Rucio server and storage systems

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## dFuture Enhancements


@startuml
start
:Parse Command Line Arguments;
:Load Configuration;
:Setup Logging;
:Initialize Rucio Client;
:Retrieve Rucio File List;
:Retrieve Storage (RSE) File List;
fork
  :Identify Dark Data;
fork again
  :Identify Missing Data;
end fork
:Generate Report;
:Output Report (JSON/CSV/TXT);
:Cleanup and Close Connections;
stop
@enduml