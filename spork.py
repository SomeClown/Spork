#!/usr/bin/env python3

from random import randint
import time
import click
import datetime
from tqdm import tqdm
import utilities
import requests
import json

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@wwt.com"


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
EPILOG = 'Have a fun time throwing foo\'s at bars'

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


@click.command(options_metavar='[no options]', short_help='get list of files')
@click.option('-t', '--type', 'file_type', help='Type of file: json, csv, binary, text')
def get_all_files_list(file_type: str):
    """
    Returns a list of file attachments in room(s) and stores in a user-specified file and format
    
    :param file_type: type of file in which to store the data
    :return: 
    """
    start = time.time()
    my_rooms = utilities.get_my_rooms_lst()
    for room in tqdm(my_rooms, desc='%sTotal of all rooms completed: %s' % (color_red2_on, color_red2_off)):
        rooms_dict = {}
        msg_list = utilities.get_room_msg_lst(room.id)
        files_temp = []
        for item in msg_list:
            files_temp.append(item.files)
        rooms_dict[room.id] = (len(msg_list), room.title, files_temp)
        tqdm.write("%sCompleted room  %s %s " % (color_red2_on, color_blue2, room.title))
        filename = (room.id + '.' + file_type)
        utilities.save_files(rooms_dict, file_type=file_type, file_name=filename)
    finish = time.time()
    elapsed = finish - start
    print('\nElapsed time: ' + '{:.2f}'.format(elapsed) + ' seconds')


@click.command(options_metavar='[no options]', short_help='return a list of channels')
def display_rooms():
    """
    Returns a list of rooms the user is a part of, or spaces, or whatever we're calling it today
    :return: 
    """
    all_rooms = utilities.get_my_rooms()
    rooms_dict = {}
    for room in all_rooms:
        dt = datetime.datetime.strptime(room.lastActivity, "%Y-%m-%dT%H:%M:%S.%fZ")
        rm = room.title
        rm_id = room.id
        rooms_dict[rm_id] = (str(dt.date()), rm)
        utilities.save_files(rooms_dict, '.rooms.json', 'json')
    for _, v in rooms_dict.items():
        (activity_date, room_title) = v
        print(color_red2_on + '{:45}'.format(room_title) + color_red2_off +
              '--' + color_blue2 + 'Last Activity: ' + color_yellow2 + str(activity_date))


@click.command(options_metavar='[no options]', short_help='return a list of channels')
def testing():
    """
    Testing
    :return: 
    """
    get_rooms = utilities.get_stuff(suffix='rooms')
    rooms = utilities.RoomsObject(get_rooms)
    # print(len(rooms))
    rooms.titles()


@click.command(short_help='Spam a foo', help='#KeepCalmAndSpamOn')
@click.argument('channel', metavar='[channel]')
@click.argument('spam_file', metavar='[file]')
def fortune_spam(channel: str, spam_file: str):
    """
    Spams a room with a line from the include fortunes database, you know, as one does. Can just
    as easily spam from any other file as well, it's just written at the moment for this.

    :param channel: Which room to send to
    :param spam_file: Which file to pull fortunes from
    :return: 
    """
    room_id = utilities.name_to_id(channel)
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
            utilities.api.messages.create(room_id, text=message)
            print(message)
            n += n
            time.sleep(rand_timer)
    except BaseException as e:
        print('Herp-derp')
        print(color_red2_on + str(e) + color_red2_off)


@click.command(short_help='List messages in a room', help='List messages in a room')
@click.option('-n', '--name', 'name', help='name of room')
@click.option('-m', '--max', 'maximum', default=10, help='maximum messages to retrieve')
def get_messages(name: str, maximum: int):
    """
    Get messages in a room
    
    :param name: Room name to retrieve messages from
    :param maximum: Number of messages to retrieve - seems to be ignored by the API
    :return: 
    """
    my_room_id = []
    all_rooms = utilities.get_my_rooms()
    count = 0
    start = time.time()
    for one_room in all_rooms:
        if name.capitalize() in one_room.title.capitalize():
            my_room_id = one_room.id
    print('\nThis may take a while if the room has a lot of messages\n')
    room_messages = utilities.get_room_msg_lst(room_id=my_room_id, max_msg=maximum)
    for message in reversed(room_messages):
        if message.personEmail and message.text is not None:
            """ Formatting here can be better, but it's serviceable for now """
            print(color_blue2 + '{:45}'.format(message.personEmail) + color_off + message.text)
            count += 1
    finish = time.time()
    elapsed = finish - start
    print('\n' + str(count) + ' messages retrieved in ' + '{:.2f}'.format(elapsed) + ' seconds')


@click.command(short_help='Send message to a room')
@click.option('-r', '--room', 'room', help='room')
@click.option('-m', '--message', 'message', help='message')
def send_message(room: str, message: str):
    """
    Send a message to a given room
    
    :param room: Name of room to send message to
    :param message: Message to send
    :return:
    """
    room_id = utilities.name_to_id(room)
    my_message = utilities.api.messages.create(room_id, text=message)
    print(my_message)


@click.command(short_help='Archives room(s)', help='Get some coffee, this is going to take a while')
@click.option('-r', '--room', 'name', help='Room to archive.')
@click.option('-t', '--type', 'file_t', help='Type of file: json, csv, binary, text')
@click.option('-e', '--everything', is_flag=True, help='You really want to do this?')
def archive(name: str, file_t: str, everything: bool):
    """
    Archives everything except file attachments (messages, people, etc.) in all rooms
    
    :param name: Room to archive, if selectinbg only one room
    :param file_t: File type to store archive as (json, text, csv, pickle)
    :param everything: Boolean flag to archive entire Spark ecosystem to which user belongs
    :return: 
    """
    if name:
        count = 0
        print('\nThis may take a while if the room has a lot of messages\n')
        start = time.time()
        my_room_id = utilities.name_to_id(name)
        msg_lst = utilities.get_room_msg_lst(my_room_id)
        with open('test.txt', 'w') as f:
            for item in msg_lst:
                print(repr(item) + '\n')
        finish = time.time()
        elapsed = finish - start
        print('\n' + str(count) + ' messages retrieved in ' + '{:.2f}'.format(elapsed) + ' seconds')


""" Adding the cli commands which trigger the functions above """
cli.add_command(get_all_files_list, 'files')
cli.add_command(display_rooms, 'rooms')
cli.add_command(fortune_spam, 'spam')
cli.add_command(get_messages, 'messages')
cli.add_command(send_message, 'send')
cli.add_command(archive, 'archive')
cli.add_command(testing, 'test')

if __name__ == '__main__':
    cli()
    """
    try:
        cli()
    except TypeError as err:
        print('Herp-derp')
        print(color_red2_on + str(err) + color_red2_off)
    """