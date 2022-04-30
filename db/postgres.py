import psycopg2
from sqlalchemy import create_engine
from os import environ
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

def connect_to_database(user, password, host, database):
    print(user, password)
    conn_string = f'postgresql://{user}:{password}@{host}/{database}'
    db = create_engine(conn_string)
    conn = db.connect()
    return conn

def insert(data, conn):
    data.to_sql('abc_article', con=conn, if_exists='append',
                index=False)


if __name__ == "__main__":
    conn = connect_to_database(environ.get('POSTGRES_USER'), 
                               environ.get('POSTGRES_PASSWORD'),
                               environ.get('POSTGRES_HOST'),
                               environ.get('POSTGRES_DATABASE_NAME'))