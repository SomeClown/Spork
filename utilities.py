#!/usr/bin/env python3

import json
import pickle
import csv
from ciscosparkapi import CiscoSparkAPI
import os


__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@wwt.com"

spark_token = os.environ["SPARK_ACCESS_TOKEN"]
api = CiscoSparkAPI()


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

