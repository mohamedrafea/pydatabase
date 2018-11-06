from tests import BaseTestCase
from sqlalchemy import Column,String,Boolean,Integer
from pydatabase.table.tableobject import TableObject
from pydatabase.env.environment import Environment
from .person import Person
from pydatabase.env.dbenvironment import DBEnvironment
from pydatabase.table.tableobjectnoid import TableObjectNoID
from pydatabase.table.sqloperator import SQLOperator
class TableObjectTest(BaseTestCase):

    def test_1_create_table(self):
        Person.createTable()
        self.assertTrue('person' in set(Person.getTables()))

    def test_2_delete(self):
        Person.cleanAll()
        self.assertTrue(len(Person.findAll()) == 0)

    def test_3_add(self):
        p = Person()
        p.name = 'john'
        p.gender = Person.GENDER_MALE
        p.insert()
        self.assertTrue(Person.find(p.id).name==p.name)
        p = Person()
        p.name = 'angela'
        p.gender = Person.GENDER_FEMALE
        p.insert()
        self.assertTrue(Person.find(p.id).gender == p.gender)

    def test_4_search(self):
        #if you use more than one field, they are anded
        fields = [Person.gender]
        values = [Person.GENDER_FEMALE]
        females = Person.findByFieldsValues(fields,values,onlyOne=False)
        for f in females:
            self.assertTrue(Person.GENDER_FEMALE == f.gender)

    def test_5_update(self):
        session = Person.createSession()
        persons = Person.findAll(session=session)
        for p in persons:
            p.optedInPush = True
            p.update(session)
        session.close()
        persons = Person.findAll(session=session)
        for p in persons:
            self.assertTrue(p.optedInPush == True)
