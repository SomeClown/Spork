#!/usr/bin/env python3

"""
CLI for Spork command line Spark client
"""

import click
import utilities

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


@click.command(options_metavar='[no options]',
               short_help='Various options to populate database tables in the Spark database')
@click.option('-r', '--rooms', is_flag=True, help='populate rooms database table')
@click.option('-p', '--people', is_flag=True, help='populate people database table')
@click.option('-m', '--membership', is_flag=True, help='populate membership database table')
@click.option('-t', '--teams', is_flag=True, help='populate teams database table')
@click.option('-M', '--messages', is_flag=True, help='populate messages database table')
def populate_db(rooms: bool, people: bool, membership: bool, teams: bool, messages: bool):
    """
    Various options to populate database tables in the Spark database
    :param rooms: 
    :param people: 
    :param membership: 
    :param teams:
    :param messages:
    :return: 
    """
    if rooms:
        action = utilities.DBOps()
        action.rooms()
    elif people:
        action = utilities.DBOps()
        action.people()
    elif membership:
        action = utilities.DBOps()
        action.membership()
    elif teams:
        action = utilities.DBOps()
        action.teams()
    elif messages:
        action = utilities.DBOps()
        foo = utilities.GrabData.get_my_rooms_lst()
        action.messages(foo)


@click.command(options_metavar='[no options]', short_help='Various options to search the Spork database')
@click.option('-t', '--term', 'search_term', help='Search term')
def search_db(search_term):
    """
    Search term testing. This MUST BE CLEANED UP BEFORE USING as there are no sanity checks on input
    :param search_term: 
    :return: 
    """
    test = utilities.DBOps()
    for returned_item in test.search_email(search_term):
        print(returned_item)


cli.add_command(populate_db, 'populate_db')
cli.add_command(search_db, 'search_db')

if __name__ == '__main__':
    cli()
