# Halligan Helper 2
[![pylint Score](https://mperlet.github.io/pybadge/badges/9.66.svg)](https://github.com/PyCQA/pylint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A utility for managing a queue of hungry hungry students that want to get help from overworked TAs

## Usage: 
    
    ./queue <comp_class_number>

ex: 

    ./queue 11

**Must be run from a terminal `ssh`'d into Halligan!**

## Does the following:
-  Determines if the user is a TA for the class.
- Gives user access to appropriate commands for their role.
- run `help` from within the queue manager to see available commands.

## Some fun features:
- Queue is locked while writing so no more than one person can change it at once.
- Nicely formatted and colorized queue is shown with the `print` command.

## Required Python Libraries:
- sys
- os
- csv
- cmd
- datetime
- [termcolor](https://pypi.org/project/termcolor/)
- [filelock](https://py-filelock.readthedocs.io/en/latest/api.html)

definitely still a work in progress :)
