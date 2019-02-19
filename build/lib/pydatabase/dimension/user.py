import pandas as pd
from sqlalchemy import Column, Integer, String, Boolean,DateTime

from pydatabase.dimension.month import Month
from pydatabase.table.tableobjectnoid import TableObjectNoID


class User(TableObjectNoID, TableObjectNoID.Base):
    __abstract__ = True
    id = Column(Integer,primary_key=True)
    gender = Column(String)
    birthDate = Column(DateTime)

    language = Column(String)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    created = Column(DateTime)
    isEmailVerified = Column(Boolean)
    isPhoneVerified = Column(Boolean)

