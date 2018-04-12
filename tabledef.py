#!/usr/bin/env python3

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy import create_engine

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@packetqueue.net"

Base = declarative_base()
engine = create_engine('sqlite:///spork.db', echo=True)


class Room(Base):
    __tablename__ = 'rooms'

    room_id = Column(String, primary_key=True)
    title = Column(String)
    room_type = Column(String)
    is_locked = Column(Boolean)
    last_activity = Column(String)
    creator_id = Column(String, ForeignKey('people.person_id'))
    created = Column(String)

    def __init__(self, room_id, title, room_type, is_locked, last_activity, creator_id, created):
        self.room_id = room_id
        self.title = title
        self.room_type = room_type
        self.is_locked = is_locked
        self.last_activity = last_activity
        self.creator_id = creator_id
        self.created = created


class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(String, primary_key=True)
    room_id = Column(String, ForeignKey('rooms.room_id'))
    room_type = Column(String)
    text = Column(String)
    person_id = Column(String, ForeignKey('people.person_id'))
    person_email = Column(String, ForeignKey('people.emails'))
    created = Column(String)

    def __init__(self, message_id, room_id, room_type, text, person_id, person_email, created):
        self.room_id = room_id
        self.message_id = message_id
        self.room_type = room_type
        self.text = text
        self.person_email = person_id
        self.person_email = person_email
        self.created = created


class People(Base):
    __tablename__ = 'people'

    person_id = Column(String, primary_key=True)
    emails = Column(String)
    displayName = Column(String)
    nickName = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    avatar = Column(String)
    org_id = Column(String)
    created = Column(String)
    person_type = Column(String)

    def __init__(self, person_id, emails, display_name, nick_name, first_name, last_name,
                 avatar, org_id, created, person_type):
        self.person_id = person_id
        self.emails = emails
        self.displayName = display_name
        self.nickName = nick_name
        self.firstName = first_name
        self.lastName = last_name
        self.avatar = avatar
        self.org_id = org_id
        self.created = created
        self.person_type = person_type


class Teams(Base):
    __tablename__ = 'teams'

    team_id = Column(String, primary_key=True)
    team_name = Column(String)
    creator_id = Column(String, ForeignKey('people.person_id'))
    created = Column(String)

    def __init__(self, team_id, team_name, creator_id, created):
        self.team_id = team_id
        self.team_name = team_name
        self.creator_id = creator_id
        self.created = created


class Memberships(Base):
    __tablename__ = 'memberships'

    membership_id = Column(String, primary_key=True)
    room_id = Column(String, ForeignKey('rooms.room_id'))
    person_id = Column(String, ForeignKey('people.person_id'))
    person_email = Column(String, ForeignKey('people.emails'))
    person_display_name = Column(String, ForeignKey('people.displayName'))
    person_org_id = Column(String, ForeignKey('people.org_id'))
    is_moderator = Column(String)
    is_monitor = Column(String)
    created = Column(String)

    def __init__(self, membership_id, room_id, person_id, person_email, person_display_name,
                 person_org_id, is_moderator, is_monitor, created):
        self.membership_id = membership_id
        self.room_id = room_id
        self.person_id = person_id
        self.person_email = person_email
        self.person_display_name = person_display_name
        self.person_org_id = person_org_id
        self.is_moderator = is_moderator
        self.is_monitor = is_monitor
        self.created = created


Base.metadata.create_all(engine)
