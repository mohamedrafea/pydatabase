# pydatabase

Database layer on top of SQLAlchemy that accelerates the development of CRUD and search operations. In addition, the project contains reusable code for some common 
dimensions used in dimensional modelling.

## Prerequisites

- Python 3, SQLAlchemy and pandas
- MySQL or PostgreSQL

## Installing

Run python setup.py install

## Getting Started
- Copy pydatabase.cfg to the root directory of your project and customize its values according to the databases you will connect to in your local, testing,
  and production environments.
  
- In your initialization module:
1- import pydatabase 
2- import Environment from pydatabase.env.environment 
3- call pydatabase.init(Environment.ENV_LOCAL) ; Environment.ENV_LOCAL will initialize the database to your local ennvironment as specified in pydatabase.cfg.

## Running the tests

From the root directory of the project, run python -m unittest tests/table/test_tableobject.py to do basic tests for pydatabase.table.tableobject module.
Tests are still Work-in-Progress.

## License

This project is licensed under the MIT License - see the LICENSE file for details

