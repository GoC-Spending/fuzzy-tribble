# fuzzy-tribble
Processing GoC-Spending data output
![Travis-CI Status](https://travis-ci.org/GoC-Spending/fuzzy-tribble.svg?branch=master)

## Requirements

- Python 3.6
- [MySQL](hhttps://dev.mysql.com/downloads/mysql/)

## Installation

- Create a python virtual environment
  - `python -m venv env`
- Install required python packages
  - `pip install -r requirements.txt`
  - `pip install -e .` 

## Usage

- `source env/bin/activate` (run each time you open the repo in a shell, to activate the virtual environment)
- `tribble --help`

### First run

Welcome to `fuzzy-tribble`! Here are steps to follow once you’ve cloned the repo and installed it:

1. Clone [the spending data repo](https://github.com/GoC-Spending/goc-spending-data) into a separate directory. This will give you the data that `fuzzy-tribble` will load into the database.
2. Run `tribble create_db`. This will create the database in MySQL.
    * By default, this database will be named `spending`. You can choose a custom name for it with the `--schema` option: `tribble --schema [your_database_name] create_db`.
3. Run `tribble init_db`. This will add the necessary tables to the database.
4. Run `tribble load [input-dir]`, substituting `[input-dir]` for the path to the data repo that you cloned in step 1.
5. Load your MySQL installation with your viewer of choice and check out the tables in your database!
    * `raw_contracts` will contain the input data, unprocessed.
    * `contracts` will contain the processed contract data, run through `fuzzy-tribble`’s transformers.
