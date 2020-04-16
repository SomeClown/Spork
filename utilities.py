#!/usr/bin/env python3

"""
Utility module for Spork. GET/PUSH operations on the Spark API, as well as SQLAlchemy operations
"""

from itertools import islice
import os
from ciscosparkapi import CiscoSparkAPI
from webexteamssdk import WebexTeamsAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from tabledef import *

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@wwt.com"

# Load spark API token from environment
spark_token = os.environ["SPARK_ACCESS_TOKEN"]

# Create Spark API instance
# api = CiscoSparkAPI()
api = WebexTeamsAPI()


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
        __rooms = [room for room in api.rooms.list()]
        for room in __rooms:
            yield room

    @staticmethod
    def get_my_rooms_lst():
        """
        Returns a list of rooms by ID
        :return: 
        """
        __rooms = [room for room in api.rooms.list()]
        return __rooms

    @staticmethod
    def get_people(person_id):
        """
        Returns a people object
        :return: 
        """
        __people = [peeps for peeps in api.people.list(id=person_id)]
        for peeps in __people:
            yield peeps

    @staticmethod
    def get_memberships():
        """
        returns memberships
        :return: 
        """
        __rooms = [room for room in api.rooms.list()]
        for item in __rooms:
            __membership = [members for members in api.memberships.list(item.id)]
            for members in __membership:
                yield members

    @staticmethod
    def get_teams():
        """
        returns team membership information
        :return: 
        """
        __teams = [team for team in api.teams.list()]
        for team in __teams:
            yield team

    @staticmethod
    def get_room_msg(room_id):
        """
        Returns messages from a given room ID
        :param room_id: 
        :return: 
        """
        __room_messages = [item for item in api.messages.list(roomId=room_id)]
        for msg in __room_messages:
            yield msg

    @staticmethod
    def get_room_msg_lst(room_id: str, max_msg: int):
        """
        Returns messages from a given room ID
        :param room_id:
        :param max_msg: 
        :return: 
        """
        __room_messages = api.messages.list(roomId=room_id)
        __short_list = list(islice(__room_messages, max_msg))
        return __short_list

    def name_to_id(self, room_name: str):
        """
        Takes a room name and returns its id
        :param room_name:
        :return:
        """
        __rooms_list = self.get_my_rooms_lst()
        for room in __rooms_list:
            if room_name in room.title:
                return room.id

    def id_to_name(self, room_id: str):
        """
        Takes a room id and returns its name
        :param room_id:
        :return:
        """
        __rooms_list = self.get_my_rooms_lst()
        for room in __rooms_list:
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

    def rooms(self):
        """
        commit all rooms information to database
        :return: 
        """
        my_data = GrabData()
        my_rooms = my_data.get_my_rooms()
        for item in my_rooms:
            db_entry = Room(item.id, item.title, item.type, item.isLocked, item.lastActivity,
                            item.teamId, item.creatorId, item.created)
            self.session.add(db_entry)
            try:
                self.session.commit()
            except exc.IntegrityError:
                self.session.rollback()

    def people(self):
        """
        commit people to database
        :return: 
        """
        my_data = GrabData()
        people = my_data.get_memberships()
        for person in people:
            my_people = my_data.get_people(person.personId)
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
        my_data = GrabData()
        memberships = my_data.get_memberships()
        for item in memberships:
            db_entry = Memberships(item.id, item.roomId, item.personId, item.personEmail,
                                   item.personDisplayName, item.personOrgId, item.isModerator,
                                   item.isMonitor, item.created)
            self.session.add(db_entry)
            try:
                self.session.commit()
            except exc.IntegrityError:
                self.session.rollback()

    def teams(self):
        """
        commit team membership information to database
        :return: 
        """
        my_data = GrabData()
        my_teams = my_data.get_teams()
        for item in my_teams:
            db_entry = Teams(item.id, item.name, item.creatorId, item.created)
            self.session.add(db_entry)
            try:
                self.session.commit()
            except exc.IntegrityError:
                self.session.rollback()

    def messages(self, room):
        """
        commit messages, by room, to database
        :return: 
        """
        my_data = GrabData()
        if isinstance(room, str):
            one_room = room
            my_messages = my_data.get_room_msg(room_id=one_room)
            for item in my_messages:
                db_entry = Message(item.id, item.roomId, item.roomType, item.text,
                                   item.personId, item.personEmail, item.created)
                self.session.add(db_entry)
                try:
                    self.session.commit()
                except exc.IntegrityError:
                    self.session.rollback()
        elif isinstance(room, list):
            many_rooms = room
            for item in many_rooms:
                my_messages = my_data.get_room_msg(room_id=item.id)
                for items in my_messages:
                    db_entry = Message(items.id, items.roomId, items.roomType, items.text,
                                       items.personId, items.personEmail, items.created)
                    self.session.add(db_entry)
                    try:
                        self.session.commit()
                    except exc.IntegrityError:
                        self.session.rollback()

    def search_email(self, search_term):
        """
        test
        :return: 
        """
        for search_result in self.session.query(People).order_by(People.emails):
            if search_term in search_result.emails:
                yield search_result
            else:
                pass

    def search_team_creator_id(self, person_id):
        """
        testing
        :param person_id: 
        :return: 
        """

        # Searches the Teams and People tables to find teams created by a person (person_id)
        results = self.session.query(Teams) \
            .join(People).filter(People.person_id == person_id).all()
        return results

