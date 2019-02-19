# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 12:55:42 2017

@author: mohamed
"""
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

logging.basicConfig()
logger = logging.getLogger("myapp.sqltime")
logger.setLevel(logging.ERROR)

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                          parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())
    logger.debug("Start Query: %s", statement)

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    logger.debug("Query Complete!")
    logger.debug("Total Time: %f", total)

class DBConnectionManager(object):
    databaseURL = {'postgres': 'postgresql://{}:{}@{}:{}/{}', 'mysql': 'mysql+mysqlconnector://{}:{}@{}:{}/{}'}



    def setEngine(self):
        if self.databaseType == 'postgres':
            # The return value of create_engine() is our connection object
            # this is used for postgres
            self.engine = sqlalchemy.create_engine(self.url, client_encoding='utf8')
        elif self.databaseType == 'mysql':
            self.engine = sqlalchemy.create_engine(self.url)
        else:
            raise Exception('Invald database type:', self.databaseType)
        #print(self.engine)

    def __init__(self, env):
        self.env = env
        self.databaseType = env.databaseType
        url = DBConnectionManager.databaseURL[self.databaseType]
        self.url = url.format(env.user, env.password, env.host, env.port, env.db)
        #print('url:', self.url)
        self.setEngine()
        self.Session = sessionmaker(bind=self.engine)
