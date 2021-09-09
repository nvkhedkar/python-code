from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, create_engine, DateTime
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

class Shape(Base):
  __tablename__ = 'shapes'
  id = Column(Integer, primary_key=True)
  time_str = Column(String)
  time_stamp = Column(DateTime)
  shape = Column(String)

  def __init__(self, t_str, s):
    self.time_str = t_str
    self.time_stamp = self.get_time_stamp()
    self.shape = s

  def get_time_stamp(self):
    return datetime.fromtimestamp(int(self.time_str))

class ShapeInteractions:
  def __init__(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    pass

  def add_test_row(self):
    curr_time = int(time.mktime(datetime.now().timetuple()))
    s = '\t<circle stroke="black" stroke-width="1" fill="black" r="36" cx="64" cy="70" />\n'
    shape_test = Shape(curr_time, s)
    self.session.add(shape_test)
    self.session.commit()

  def add_shape(self, time_str, shape_str):
    """Add shape to db"""
    shape_test = Shape(time_str, shape_str)
    self.session.add(shape_test)
    self.session.commit()

  def show_shapes(self):
    """Query and Show all Shape rows in db"""
    shapes = self.session.query(Shape)
    for i, shape in enumerate(shapes):
      print(f"DB [{i+1}]:", shape.time_stamp.strftime("%Y-%b-%d %H:%M:%S"), shape.shape.strip())

  def get_shapes_list(self):
    """Get a list of all shapes in the 'shapes' table"""
    shapes_list = []
    shapes = self.session.query(Shape)
    for shape in shapes:
      shapes_list.append(shape.time_str +',' + shape.shape)
    return shapes_list

  def get_num_shapes(self):
    return self.session.query(Shape).count()

  def __del__(self):
    self.session.close()


# Shape.__table__.drop(engine)
si = ShapeInteractions()
# si.add_test_row()
# si.show_shapes()

def performance_test():
  import time
  start = time.perf_counter()
  for i in range(3_000):
    lst = si.get_shapes_list()
  end = time.perf_counter() - start
  print(f"DB finished in {end:0.2f} seconds.")

# performance_test()
