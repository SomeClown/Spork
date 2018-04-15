#!/usr/bin/env python3

import click
import utilities
from sqlalchemy.orm import sessionmaker
from tabledef import *

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@wwt.com"


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
EPILOG = 'Have a fun time throwing foo\'s at bars'


@click.group(epilog=EPILOG, context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Quick and dirty proof of concept. Exercises the Spark API without killing any kittens.
  
    """
    pass


@click.command(options_metavar='[no options]', short_help='get list of files')
@click.option('-r', '--rooms', is_flag=True, help='populate rooms database table')
@click.option('-p', '--people', is_flag=True, help='populate people database table')
def populate_db(rooms: bool, people: bool):
    if rooms:
        action = utilities.DBOps()
        action.rooms()
    elif people:
        action = utilities.DBOps()
        action.people()


cli.add_command(populate_db, 'populate_db')

if __name__ == '__main__':
    cli()
