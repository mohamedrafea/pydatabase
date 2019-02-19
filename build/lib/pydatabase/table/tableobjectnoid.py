# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 12:38:19 2017

@author: mohamed
"""
import sqlalchemy
from pydatabase.common import Common
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.query import Query

from pydatabase.dbconnectionmanager import DBConnectionManager
from pydatabase.table.sqloperator import SQLOperator
import pandas as pd

class TableObjectNoID(Common):
    #below are class variables
    database = None
    Base = declarative_base()
    @classmethod
    def addColumn(cls,column):
        full_column_name = str(column.compile(dialect=cls.database.engine.dialect))
        column_name = full_column_name[full_column_name.index('.')+1:len(full_column_name)]
        column_name = column_name.replace('"','')
        column_type = column.type.compile(cls.database.engine.dialect)
        defaultValue = None
        if column.default is not None:
            defaultValue = column.default.arg
        #print(dir(column))
        q = 'ALTER TABLE %s ADD COLUMN %s %s' % (cls.__tablename__, column_name, column_type)
        if defaultValue is not None:
            q = q + ' CONSTRAINT '+column_name+'_default DEFAULT '+str(defaultValue)
        conn = cls.database.engine.connect()
        print(q)
        conn.execute(q)

    @classmethod
    def clean(cls,dateField,fromDate, beforeDate):
        fields = [dateField, dateField]
        values = [fromDate, beforeDate]
        operators = [SQLOperator.greaterThanOrEqualOperator, SQLOperator.lessThanOperator]
        session = cls.createSession()
        l = cls.findByFieldsValues(fields, values, operators=operators, onlyOne=False,session=session)
        for o in l:
            o.delete(session)
        session.close()

    def getID(self):
        return None

    @classmethod
    def getListOfIDs(cls, objects):
        l = []
        for o in objects:
            l.append(o.getID())
        return l

    @classmethod
    def cleanAll(cls):
        session = cls.createSession()
        l = cls.findAll(session=session)
        for o in l:
            o.delete(session)
        session.close()

    @classmethod
    def createSession(cls):
        return TableObjectNoID.database.Session()
    @classmethod
    def setDatabase(cls,env):
        #cls.database = DBConnectionManager('poc_role','pocpass','poc')
        #print("in TableObject->setDatabase")
        #print(env)
        cls.database = DBConnectionManager(env)
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    @classmethod 
    def createTable(cls):    
        print('cls.database.engine:',cls.database.engine)
        cls.Base.metadata.create_all(cls.database.engine)

    @classmethod
    def listTables(cls):
        print(cls.getTables())

    @classmethod
    def getTables(cls):
        inspector = inspect(cls.database.engine)
        return inspector.get_table_names()

    @classmethod
    def printColumnNames(cls):
        inst = inspect(cls)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        print(attr_names)
      
    def insert(self,session=None):
        if session is None:
            session = TableObjectNoID.database.Session()
            close = True
        session.add(self)       
        session.commit()
        if close:
            session.close()

    @classmethod
    def batchInsert(cls,listToWrite,session=None):
        metadata = sqlalchemy.schema.MetaData(bind=cls.database.engine,reflect=True)
        table = sqlalchemy.Table(cls.__tablename__, metadata, autoload=True)	   
        close = False
        if session is None:
            session = TableObjectNoID.database.Session()
            close = True
        conn = cls.database.engine.connect()
        conn.execute(table.insert(), listToWrite)
        session.commit()
        if close:
            session.close()		
	#below 2 methods optionally implemented by subclasses that want this feature
    def getUniqueConstraintFields(self):
        pass

    def getUniqueConstraintValues(self):
        pass

    def insertOrLoad(self,session=None):
        o = self.findByFieldsValues(self.getUniqueConstraintFields(),self.getUniqueConstraintValues(),session,True)
        if o is not None:
            return o
        self.insert(session)
        return self
    def delete(self,session):
      
        session.delete(self)       
        session.commit()       
        
    def update(self,session):       
        #session.flush()
        session.commit()
    @classmethod
    def find(cls,oid):
        session = cls.database.Session()
        o = session.query(cls).filter_by(id=oid).first()
        session.close()
        return o

    @classmethod
    def queryToDataframe(cls,query):
        conn = cls.database.engine
        statement = query.statement
        sql = statement.compile(conn)
        #print(sql)
        return pd.read_sql(sql, con=conn)
    @classmethod
    def findAll(cls,joinField = None,session=None,returnDataframe=False):
        close = False
        if session is None:
            session = cls.database.Session()
            close = True
        t = session.query(cls)
        if not (joinField is None):
            t = t.options(joinedload(joinField))
        o = None
        if returnDataframe:
            o = cls.queryToDataframe(t)
        else:
            o = t.all()
        if close:
            session.close()
        return o

    @classmethod
    def findByArrayValues(cls,field,values,session=None,onlyOne=True):
        close = False
        if session is None:
            session = cls.database.Session()        
            close = True  
        o = None
        for value in values:     
            if o is None:
                o = session.query(cls)
            o = o.filter(field.any(value))
        if onlyOne:
            o = o.first()
        else:
            o = o.all()
        if close:
            session.close()
        return o
       
    @classmethod
    def findByFieldsValues(cls,fields,values,session=None,onlyOne=True,notNoneFields=None,orderByFields=None,ascending=True,operators=None,groupByFields=None,selectFieldsAndFunctions=None,nestedOperators=None,returnDataframe=False,distinct=False,printQuery=False):
        if operators is None:
            operators = [SQLOperator.equalOperator] * 1000
        close = False
        if session is None:
            session = cls.database.Session()        
            close = True  
        o = None
        if selectFieldsAndFunctions is None:
            o = session.query(cls)
        else:
            o = Query(selectFieldsAndFunctions, session=session)
        for field,value,operator in zip(fields,values,operators):
            operator.field = field
            operator.value = value
            o = operator.filter(o)
        if nestedOperators is not None:
            for operator in nestedOperators:
                o = operator.filter(o)
        if notNoneFields is not None:
            for f in notNoneFields:
                o = o.filter(f != None)
        if groupByFields is not None:
            for  f in groupByFields:
                o = o.group_by(f)
        if orderByFields is not None:
            for  f in orderByFields:
                if ascending:
                    o = o.order_by(f)
                else:
                    o = o.order_by(f.desc())
        if printQuery:
            print(o)
        if onlyOne:
            o = o.first()
        else:
            if distinct:
                o = o.distinct()
            if returnDataframe:
                o = cls.queryToDataframe(o)
            else:
                o = o.all()
        if close:
            session.close()
        return o
    @classmethod
    def findByFieldValue(cls,field,value,session=None,onlyOne=True,orderByField=None,ascending=True,operators=None,groupByFields=None,selectFieldsAndFunctions=None,nestedOperators=None,returnDataframe=False):
        return (cls.findByFieldsValues([field],[value],session,onlyOne,None,orderByField,ascending,operators,groupByFields,selectFieldsAndFunctions,nestedOperators,returnDataframe))

    @classmethod
    def tl(cls, CSVFile,saveIndex=False):
        df = cls.transform(CSVFile)
        cls.savePandasDataframe(df,saveIndex)
    @staticmethod        
    def printState(q):
        insp = inspect(q)
        if insp.transient:
            print('T')
        elif insp.persistent:
            print('P')
        elif insp.pending:
            print('Pending')
        elif insp.detached:
            print('detached')

    @classmethod
    def savePandasDataframe(cls,df,saveIndex=False):
        df.to_sql(name=cls.__tablename__, con=cls.database.engine, index=saveIndex, if_exists='append')

    @classmethod
    def createObject(cls):
        return None

    @classmethod
    def extract(cls, targetEnv,fields=None,values=None,operators=None):
        objects = None
        if fields is None:
            objects = cls.findAll()
        else:
            objects = cls.findByFieldsValues(fields=fields,values=values,operators=operators,onlyOne=False)
        TableObjectNoID.setDatabase(targetEnv)
        for o in objects:
            p = cls.createObject()
            p.copy(o,'id')
            p.insert()

    @classmethod
    def copyAndInsertObjects(cls, objects):
        for o in objects:
            p = cls.createObject()
            p.copy(o)
            p.insert()