from ciscosparkapi import CiscoSparkAPI
import os
from itertools import islice

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@wwt.com"

# Load spark API token from environment
spark_token = os.environ["SPARK_ACCESS_TOKEN"]

# For using CiscoSparkAPI
api = CiscoSparkAPI()


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
    room_messages = [item for item in api.messages.list(roomId=room_id)]
    for msg in room_messages:
        yield msg


def get_room_msg_lst(room_id: str, max_msg: int):
    """
    Returns messages from a given room ID
    :param room_id:
    :param max_msg: 
    :return: 
    """
    room_messages = api.messages.list(roomId=room_id)
    short_list = list(islice(room_messages, max_msg))
    return short_list


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

