from ciscosparkapi import CiscoSparkAPI
import os
from itertools import islice
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from tabledef import *

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@wwt.com"

# Load spark API token from environment
spark_token = os.environ["SPARK_ACCESS_TOKEN"]

# For using CiscoSparkAPI
api = CiscoSparkAPI()


class GrabData(object):
    """
    encapsulate all functions/methods acting to retrieve data from the Spark API
    """
    def __init__(self):
        pass

    @staticmethod
    def get_my_rooms():
        """
        Returns a list of rooms by ID
        :return: 
        """
        rooms = [room for room in api.rooms.list()]
        for room in rooms:
            yield room

    @staticmethod
    def get_my_rooms_lst():
        """
        Returns a list of rooms by ID
        :return: 
        """
        rooms = [room for room in api.rooms.list()]
        return rooms

    @staticmethod
    def get_people(person_id):
        """
        Returns a people object
        :return: 
        """
        people = [peeps for peeps in api.people.list(id=person_id)]
        for peeps in people:
            yield peeps

    @staticmethod
    def get_memberships():
        """
        returns memberships
        :return: 
        """
        rooms = [room for room in api.rooms.list()]
        for item in rooms:
            membership = [members for members in api.memberships.list(item.id)]
            for members in membership:
                yield members

    @staticmethod
    def get_teams():
        """
        returns team membership information
        :return: 
        """
        teams = [team for team in api.teams.list()]
        for team in teams:
            yield team

    @staticmethod
    def get_room_msg(room_id):
        """
        Returns messages from a given room ID
        :param room_id: 
        :return: 
        """
        room_messages = [item for item in api.messages.list(roomId=room_id)]
        for msg in room_messages:
            yield msg

    @staticmethod
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

    def flatten(self, lst: list):
        """
        Not used at this point. Flattens a nested list. Also not quite working, so, there's that.
        :param lst: 
        :return: 
        """
        for element in lst:
            if hasattr(element, "__iter__"):
                yield from self.flatten(element)
            elif element is not None:
                yield element

    def name_to_id(self, room_name: str):
        """
        Takes a room name and returns its id
        :param room_name:
        :return:
        """
        rooms_list = self.get_my_rooms_lst()
        for room in rooms_list:
            if room_name in room.title:
                return room.id

    def id_to_name(self, room_id: str):
        """
        Takes a room id and returns its name
        :param room_id:
        :return:
        """
        rooms_list = self.get_my_rooms_lst()
        for room in rooms_list:
            if room_id in room.id:
                return room.title


class DBOps(object):
    """
    class to encapsulate all database operations
    """
    def __init__(self):
        pass

    my_engine = create_engine('sqlite:///spork.db', echo=True)
    my_session = sessionmaker(bind=my_engine)
    session = my_session()
    my_data = GrabData()

    def rooms(self):
        """
        commit all rooms information to database
        :return: 
        """
        my_rooms = self.my_data.get_my_rooms()
        for item in my_rooms:
            db_entry = Room(item.id, item.title, item.type, item.isLocked, item.lastActivity,
                            item.teamId, item.creatorId, item.created)
            self.session.add(db_entry)
        self.session.commit()

    def people(self):
        """
        commit people to database
        :return: 
        """
        people = self.my_data.get_memberships()
        for person in people:
            my_people = self.my_data.get_people(person.personId)
            for item in my_people:
                db_entry = People(item.id, item.emails[0], item.displayName, item.nickName, item.firstName,
                                  item.lastName, item.avatar, item.orgId, item.created, item.type)
                self.session.add(db_entry)
                try:
                    self.session.commit()
                except exc.IntegrityError:
                    self.session.rollback()

    def membership(self):
        """
        commit room membership information to database
        :return: 
        """
        memberships = self.my_data.get_memberships()
        for item in memberships:
            db_entry = Memberships(item.id, item.roomId, item.personId, item.personEmail,
                                   item.personDisplayName, item.personOrgId, item.isModerator,
                                   item.isMonitor, item.created)
            self.session.add(db_entry)
        self.session.commit()

    def teams(self):
        """
        commit team membership information to database
        :return: 
        """
        my_teams = self.my_data.get_teams()
        for item in my_teams:
            db_entry = Teams(item.id, item.name, item.creatorId, item.created)
            self.session.add(db_entry)
        self.session.commit()


