import pandas as pd
import numpy as np
import sys
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

df = pd.DataFrame([
    ['jurassic', 'speil', 'english', '1992'],
    ['jaws', 'speil', 'english', '1985'],
    ['godfather', 'coppolla', 'english', '1973'],
    ['sholey', 'sippy', 'hindi', '1975'],
    ['golmaal', 'mukher', 'hindi', '1978']
], columns=['title', 'director', 'language', 'year'])

films = df.to_records(index=False)
print(type(films), type(films[0]))
fd = df.to_dict(orient=1)
print(type(fd))
print(fd)
DATABASE_URI = f'postgresql+psycopg2://guest:guest@10.192.39.4:5432/nvktestdb1'


def simple_table_create():
    engine = create_engine(DATABASE_URI)
    engine.execute("CREATE TABLE IF NOT EXISTS myfilms (title text, director text, language text, year text)")


# engine.connect()
# print('done')

# if not database_exists(engine.url):
#     create_database(engine.url)
#     print('Creating')
# else:
#     # Connect the database if exists.
#     engine.connect()
#     print('connected')
