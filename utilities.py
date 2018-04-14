import json
import pickle
import csv
from ciscosparkapi import CiscoSparkAPI
import os
from itertools import islice
import requests

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@wwt.com"

spark_token = os.environ["SPARK_ACCESS_TOKEN"]
api = CiscoSparkAPI()
api_url_base = 'https://api.ciscospark.com/v1/'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Umbrella Corporation',
           'Authorization': 'Bearer {0}'.format(spark_token)}
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


class RoomsObject(object):
    """
    Modeling an object to hold rooms data... for use if we rewrite the application to
    use native REST API calls via Response library instead of CiscoSparkAPI SDK
    """
    def __init__(self, data):
        self.rooms = data

    def count(self):
        """
        returns number of items (rooms) in the incoming json list
        :return: int
        """
        return len(self.rooms['items'])

    def __len__(self):
        my_length = self.count()
        return my_length

    def room_id(self, position: int):
        """
        returns one title, given a list position number
        :param position:
        :return: 
        """
        if 'id' in self.rooms['items'][position].keys():
            return self.rooms['items'][position]['id']
        else:
            return 0

    def title(self, position: int):
        """
        returns one title, given a list position number
        :param position: 
        :return: 
        """
        if 'title' in self.rooms['items'][position].keys():
            return self.rooms['items'][position]['title']
        else:
            return 0

    def room_type(self, position: int):
        """
        returns one room type, given a list position number
        :param position:
        :return: 
        """
        if 'type' in self.rooms['items'][position].keys():
            return self.rooms['items'][position]['type']
        else:
            return 0

    def is_locked(self, position: int):
        """
        returns one instance of isLocked, given a list position number
        :param position:
        :return: 
        """
        if 'isLocked' in self.rooms['items'][position].keys():
            return self.rooms['items'][position]['isLocked']
        else:
            return 0

    def last_activity(self, position: int):
        """
        returns one instance of lastActivity, given a list position number
        :param position:
        :return: 
        """
        if 'lastActivity' in self.rooms['items'][position].keys():
            return self.rooms['items'][position]['lastActivity']
        else:
            return 0

    def team_id(self, position: int):
        """
        returns one instance of teamId, given a list position number
        :param position:
        :return: 
        """
        if 'teamId' in self.rooms['items'][position].keys():
            return self.rooms['items'][position]['teamId']
        else:
            return 0

    def creator_id(self, position: int):
        """
        returns one instance of creatorId, given a list position number
        :param position:
        :return: 
        """
        if 'creatorId' in self.rooms['items'][position].keys():
            return self.rooms['items'][position]['creatorId']
        else:
            return 0

    def created(self, position: int):
        """
        returns one instance of created, given a list position number
        :param position:
        :return: 
        """
        if 'created' in self.rooms['items'][position].keys():
            return self.rooms['items'][position]['created']
        else:
            return 0

    def __repr__(self):
        return "I'm sorry, Dave. I'm afraid I can't do that."


def get_stuff(suffix: str):
    """
    return a python response object to calling object
    :param: suffix
    :return: json object
    """
    api_url = (api_url_base + suffix)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    elif response.status_code >= 500:
        print(color_red2_on + '\n[!] [{0}] Server Error'.format(response.status_code) + color_off)
        return None
    elif response.status_code == 404:
        print(color_red2_on + '\n[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url) + color_off)
        return None
    elif response.status_code == 401:
        print(color_red2_on + '\n[!] [{0}] Authentication Failed'.format(response.status_code) + color_off)
        return None
    elif response.status_code == 400:
        print(color_red2_on + '\n[!] [{0}] Bad Request'.format(response.status_code) + color_off)
        return None
    elif response.status_code >= 300:
        print(color_red2_on + '\n[!] [{0}] Unexpected Redirect'.format(response.status_code) + color_off)
        return None
    else:
        print(color_red2_on + '\n[?] Unexpected Error: [HTTP {0}]: '
                              'Content: {1}'.format(response.status_code, response.content) + color_off)
        return None


def save_files(data: dict, file_name: str, file_type: str):
    """
    Save data to file in a variety of formats
    :param data: dictionary
    :param file_name: file name
    :param file_type: one of json, text, csv, pickle
    :return: 
    """
    complete_file_name = './.data/' + file_name
    if file_type == 'json':
        os.makedirs(os.path.dirname(complete_file_name), exist_ok=True)
        name = json.dumps(data)
        with open(complete_file_name, 'w') as f:
            f.write(name)
    elif file_type == 'pkl':
        os.makedirs(os.path.dirname(complete_file_name), exist_ok=True)
        with open(complete_file_name, 'wb') as f:
            pickle.dump(data, f)
    elif file_type == 'csv':
        os.makedirs(os.path.dirname(complete_file_name), exist_ok=True)
        file = csv.writer(open(complete_file_name, "w"))
        for key, value in data.items():
            file.writerow([key, value])
    elif file_type == 'text':
        os.makedirs(os.path.dirname(complete_file_name), exist_ok=True)
        with open(complete_file_name, "w") as f:
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

