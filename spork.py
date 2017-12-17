#!/usr/bin/env python3

import os
from ciscosparkapi import CiscoSparkAPI, SparkApiError
from random import randint
import time
import click
import datetime
import json
import pickle
import csv
from tqdm import tqdm

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@wwt.com"


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
EPILOG = 'Have a fun time throwing foo\'s at bars'

spark_token = os.environ["SPARK_ACCESS_TOKEN"]
api = CiscoSparkAPI()

color_black2 = "\033[1;30m"
color_red2_on = "\033[01;31m"
color_red2_off = "\33[00m"
color_green2 = "\033[1;32m"
color_yellow2 = "\033[1;33m"
color_blue2 = "\033[1;34m"
color_purple2 = "\033[1;35m"
color_cyan2 = "\033[1;36m"
color_white2 = "\033[1;37m"
color_off = "\33[00m"


@click.group(epilog=EPILOG, context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Quick and dirty proof of concept. Exercises the Spark API without killing any kittens.
    :return: 
    """
    pass


def get_my_rooms():
    """
    Returns a list of rooms by ID
    :return: 
    """
    rooms = [room for room in api.rooms.list()]
    for room in rooms:
        yield room


def get_my_rooms_lst():
    """
    Returns a list of rooms by ID
    :return: 
    """
    rooms = [room for room in api.rooms.list()]
    return rooms


def get_room_msg(room_id):
    """
    Returns messages from a given room ID
    :param room_id: 
    :return: 
    """
    room_messages = [item for item in api.messages.list(roomId=room_id) if item.files is not None]
    for msg in room_messages:
        yield msg


def get_room_msg_lst(room_id):
    """
    Returns messages from a given room ID
    :param room_id: 
    :return: 
    """
    room_messages = [item for item in api.messages.list(roomId=room_id) if item.files is not None]
    return room_messages


def flatten(lst: list):
    """
    Not used at this point. Flattens a nested list. Also not quite working, so, there's that.
    :param lst: 
    :return: 
    """
    for element in lst:
        if hasattr(element, "__iter__"):
            yield from flatten(element)
        elif element is not None:
            yield element


def save_files(data: dict, file_name: str, file_type: str):
    """
    Save data to file in a variety of formats
    :param data: dictionary
    :param file_name: file name
    :param file_type: one of json, text, csv, pickle
    :return: 
    """
    if file_type == 'json':
        name = json.dumps(data)
        with open(file_name, 'w') as f:
            f.write(name)
    elif file_type == 'pkl':
        with open(file_name, 'wb') as f:
            pickle.dump(data, f)
    elif file_type == 'csv':
        file = csv.writer(open(file_name, "w"))
        for key, value in data.items():
            file.writerow([key, value])
    elif file_type == 'text':
        with open(file_name, "w") as f:
            f.write(str(data))


@click.command(options_metavar='[no options]', short_help='get list of files')
@click.option('-t', '--type', 'file_type', help='Type of file: json, csv, binary, text')
def get_all_files_list(file_type):
    """
    Returns a list of file attachments in room(s) and stores in a user-specified file and format
    :return: 
    """
    start = time.time()
    rooms_dict = {}
    my_rooms = get_my_rooms_lst()
    for room in tqdm(my_rooms, desc='%sTotal of all rooms completed: %s' % (color_red2_on, color_red2_off)):
        msg_list = get_room_msg_lst(room.id)
        files_temp = []
        for item in msg_list:
            files_temp.append(item.files)
        rooms_dict[room.id] = (len(msg_list), room.title, files_temp)
        tqdm.write("%sCompleted room  %s %s " % (color_red2_on, color_blue2, room.title))
    filename = ('.files.' + file_type)
    save_files(rooms_dict, file_type=file_type, file_name=filename)
    finish = time.time()
    elapsed = finish - start
    print('\nElapsed time: ' + '{:.2f}'.format(elapsed) + ' seconds')


@click.command(options_metavar='[no options]', short_help='return a list of channels')
def retrieve_rooms():
    """
    Returns a list of rooms the user is a part of, or spaces, or whatever we're calling it today
    :return: 
    """
    all_rooms = get_my_rooms()
    rooms_dict = {}
    for room in all_rooms:
        dt = datetime.datetime.strptime(room.lastActivity, "%Y-%m-%dT%H:%M:%S.%fZ")
        rm = room.title
        rm_id = room.id
        rooms_dict[rm_id] = (str(dt.date()), rm)
        save_files(rooms_dict, '.rooms.json', 'json')
    for _, v in rooms_dict.items():
        (activity_date, room_title) = v
        print(color_red2_on + '{:45}'.format(room_title) + color_red2_off +
              '--' + color_blue2 + 'Last Activity: ' + color_yellow2 + str(activity_date))


@click.command(short_help='Spam a foo', help='#KeepCalmAndSpamOn')
@click.argument('channel', metavar='[channel]')
@click.argument('spam_file', metavar='[file]')
def fortune_spam(channel, spam_file):
    """
    Spams a room with a line from the include fortunes database, you know, as one does. Can just
    as easily spam from any other file as well, it's just written at the moment for this.

    :param channel: Which room to send to
    :param spam_file: Which file to pull fortunes from
    :return: 
    """
    all_rooms = get_my_rooms_lst()
    room_id = ''
    for thing in all_rooms:
        if channel in thing.title:
            room_id = thing.id
    parsed_fortunes = []
    n = 0
    try:
        with open(spam_file, 'r') as f:
            temp_fortunes = f.read().split('%')
            for item in temp_fortunes:
                parsed_fortunes.append(item.split('%'))

        for item in parsed_fortunes:
            for a, b in enumerate(item):
                item[a] = b.replace('\n', ' ')

        while n <= len(parsed_fortunes) - 1:
            rand_timer = randint(600, 1800)
            rand_item = randint(0, len(parsed_fortunes) - 1)
            message = ''.join(parsed_fortunes[rand_item])
            api.messages.create(room_id, text=message)
            print(message)
            n += n
            time.sleep(rand_timer)
    except BaseException as e:
        print('Not sure what shit the bed, but the shit looks like this:')
        print(color_red2_on + str(e) + color_red2_off)


@click.command(short_help='List messages in a room', help='List messages in a room')
@click.option('-n', '--name', 'name', help='name of room')
def get_messages(name):
    my_room_id = []
    all_rooms = get_my_rooms()
    count = 0
    start = time.time()
    for one_room in all_rooms:
        if name.capitalize() in one_room.title.capitalize():
            my_room_id = one_room.id
    room_messages = api.messages.list(my_room_id)
    try:
        for message in room_messages:
            """ Formatting here can be better, but it's serviceable for now """
            print(color_blue2 + '{:45}'.format(message.personEmail) + color_off + message.text)
            count += 1
        finish = time.time()
        elapsed = finish - start
        print('\n' + str(count) + ' messages retrieved in ' + '{:.2f}'.format(elapsed) + ' seconds')
    except TypeError:
        """ This is really a placeholder error. Need to get more specific in error handling here """
        print(color_red2_on + '\nRoom doesn\'t appear to exist\n' + color_red2_off)


@click.command(short_help='Send message to a room')
@click.option('-r', '--room', 'room', help='room')
@click.option('-m', '--message', 'message', help='message')
def send_message(room: str, message: str):
    """
    Send a message to a given room
    :param room:
    :param message:
    :return:
    """
    room_id = name_to_id(room)
    my_message = api.messages.create(room_id, text=message)
    print(my_message)


def name_to_id(room_name: str):
    """
    Takes a room name and returns its id
    :param room_name:
    :return:
    """
    rooms_list = get_my_rooms_lst()
    for room in rooms_list:
        if room_name in room.title:
            return room.id


def id_to_name(room_id: str):
    """
    Takes a room id and returns its name
    :param room_id:
    :return:
    """
    rooms_list = get_my_rooms_lst()
    for room in rooms_list:
        if room_id in room.id:
            return room.title


""" Adding the cli commands which trigger the functions above """
cli.add_command(get_all_files_list, 'files')
cli.add_command(retrieve_rooms, 'rooms')
cli.add_command(fortune_spam, 'spam')
cli.add_command(get_messages, 'messages')
cli.add_command(send_message, 'send')

if __name__ == '__main__':
    cli()
    """
    try:
        cli()
    except TypeError as err:
        print('Not sure what shit the bed, but we\'ll blame it on you. The error is below:')
        print(color_red2_on + str(err) + color_red2_off)
    """