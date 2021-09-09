from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import pandas as pd
import time, functools


db_url = '10.192.39.4:5432'
db_name = 'saas1'
db_user = 'guest'
db_password = 'guest'
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Entity:
  id = Column(Integer, primary_key=True)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)
  last_updated_by = Column(String)

  def __init__(self, created_by):
    self.created_at = datetime.now()
    self.updated_at = datetime.now()
    self.last_updated_by = created_by


class Message(Entity, Base):
  __tablename__ = 'messages'

  # message_id = Column(Integer, primary_key=True)
  message = Column(String)
  transformation = Column(String)
  description = Column(String)

  def __init__(self, message, description, created_by):
    Entity.__init__(self, created_by)
    self.message = message
    if description:
      self.description = description
    else:
      self.description = f"message from {created_by}"
    self.transformation = self.create_transformation(message)

  def create_transformation(self, message):
    transformation = ""
    for c in reversed(message):
      transformation += c
    return transformation


def add_first_message():
  messages = session.query(Message).all()
  if len(messages) == 0:
    # create and persist mock exam
    first_message = Message("Nice Movie", "", "nikhil")
    session.add(first_message)
    session.commit()
    # reload exams
    messages = session.query(Message).all()


def show_messages():
  messages = session.query(Message).all()
  print('### Messages:')
  for message in messages:
      print(f'({message.id}) [{message.last_updated_by}]: {message.message} | {message.description} | {message.transformation}')


def add_messages(msg, des, user):
  first_message = Message(msg, des, user)
  session.add(first_message)
  session.commit()


def add_initial_data():
# start session
  add_messages("Liked the movie!", "", "pratham")
  add_messages("Best action movie of the year!", "", "Amit")
  add_messages("Well shot action sequences!", "", "Pushkaraj")
  show_messages()


Base.metadata.create_all(engine)
session = Session()
session.close()

