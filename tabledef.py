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
    creator_id = Column(String)
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
    person_id = Column(String)
    person_email = Column(String)
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
    emails = Column(String, ForeignKey('messages.person_email'))
    displayName = Column(String)
    nickName = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    avatar = Column(String)
    org_id = Column(String)
    created = Column(String)
    person_type = Column(String)

    def __init__(self, person_id, emails, displayName, nickName, firstName, lastName,
                 avatar, org_id, created, person_type):
        self.person_id = person_id
        self.emails = emails
        self.displayName = displayName
        self.nickName = nickName
        self.firstName = firstName
        self.lastName = lastName
        self.avatar = avatar
        self.org_id = org_id
        self.created = created
        self.person_type = person_type


Base.metadata.create_all(engine)
