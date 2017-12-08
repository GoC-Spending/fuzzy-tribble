# fuzzy-tribble
Processing GoC-Spending data output
![Travis-CI Status](https://travis-ci.org/GoC-Spending/fuzzy-tribble.svg?branch=master)

## Requirements

- Python 3.6
- [MySQL](hhttps://dev.mysql.com/downloads/mysql/)

## Installation

- Create a python virtual environment
  - `python -m venv env`
  - `source env/bin/activate`
- Install required python packages
  - `pip install -r requirements.txt`
  - `pip install -e .` 

## Usage

### General tips

- Run `source env/bin/activate` each time you open the repo in a shell, to activate the virtual environment
* Run `--help` after any command to get documentation specific to it. `tribble --help` will give you information about the package in general. `tribble [command_name] --help` (where `[command_name]` is a command like `create_db`) will give you information about the command specified.

### First run

Welcome to `fuzzy-tribble`! Here are steps to follow once you’ve cloned the repo and installed it:

1. Clone [the spending data repo](https://github.com/GoC-Spending/goc-spending-data) into a separate directory. This will give you the data that `fuzzy-tribble` will load into the database.
2. Run `tribble create_db`. This will create the database in MySQL.
    * By default, this database will be named `spending`. You can choose a custom name for it with the `--schema` option: `tribble --schema [your_database_name] create_db`.
    * Specify the MySQL user (`--user`), password (`--password`), and, if necessary, the host (`--host`). We’ve set up sensible defaults for these, which may work for you. *Note*: These options *precede* the `create_db` command (i.e. `tribble --user [mysql_user] create_db`). This note applies for all other commands.
3. Run `tribble init_db`. This will add the necessary tables to the database.
4. Run `tribble load [input-dir]`, substituting `[input-dir]` for the path to the data repo that you cloned in step 1.
5. Load your MySQL installation with your viewer of choice and check out the tables in your database!
    * `raw_contracts` will contain the input data, unprocessed.
    * `contracts` will contain the processed contract data, run through `fuzzy-tribble`’s transformers.

### Important notes

* Make sure to provide the parameters before the relevant command. For global options (e.g. `--user`), they must come before the command (e.g. `create_db`). `tribble --user USER create_db` will work; `tribble create_db --user USER` will not. For command options (e.g. `--runtime-user` for the `create_db` command), they must come after the command.
