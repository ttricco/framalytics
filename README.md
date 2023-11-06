# Framalytics Package

This repository contains the Framalytics package, an open-source project developed based on FRAM

## Structure

- `framalytics/`: Main package directory
  - `__init__.py`: Initializes the Python package
  - `read_xfmv.py`: Module for reading XFMV files
  - `visualize.py`: Module for visualization purposes
  - `xfmv_parser.py`: Module for parsing XFMV file content
- `tests/`: Contains all the unit tests for the package
  - `test_read_xfmv.py`: Tests for the read_xfmv module
  - `test_visualize.py`: Tests for the visualize module
  - `test_xfmv_parser.py`: Tests for the xfmv_parser module
- `.github/`: Contains GitHub-related configurations
  - `workflows/`: Contains GitHub Actions workflows
    - `python-package.yml`: Workflow for Python package testing and linting
- `requirements.txt`: Lists the Python package dependencies

