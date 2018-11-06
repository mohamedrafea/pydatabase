# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 12:38:19 2017

@author: mohamed
"""
from sqlalchemy import Column, Integer

from pydatabase.table.tableobjectnoid import TableObjectNoID


class TableObject(TableObjectNoID):
    id = Column(Integer, primary_key=True)

    def insert(self, session=None):
        if session is None:
            session = TableObjectNoID.database.Session()
            close = True
        session.add(self)
        session.commit()
        t = self.id
        if close:
            session.close()

    @classmethod
    def getListOfIDs(cls, objects):
        l = []
        for o in objects:
            l.append(o.id)
        return l

    
