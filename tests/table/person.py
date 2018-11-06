from sqlalchemy import Column,String,Boolean,Integer
from pydatabase.table.tableobject import TableObject

class Person(TableObject,TableObject.Base):
    GENDER_FEMALE = 1
    GENDER_MALE = 2
    name = Column(String)
    gender = Column(Integer)
    optedInPush = Column(Boolean,default=False)