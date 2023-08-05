from sqlalchemy import Table, Column, Integer, String, ForeignKey,\
     MetaData, Index
from sqlalchemy.orm import mapper, relation
from zope.interface import Interface, implements
from zope.schema import TextLine, Int

metadata = MetaData()

################ Interfaces ######################

class IMyPerson(Interface):
    """ This is a person """

    mypersonid = Int(
        title = u"PersonID",
        description = u"ID of the person"
        )

    name1 = TextLine(
        title = u"Name_1",
        description = u"First name"
        )

    testprop = TextLine(
        title = u"TestProp",
        description = u"Test Property")
    
class IAddress(Interface):

    addressid = Int()
    street = TextLine()
    mypersonid = Int()

################ Tables #######################

table_myperson = Table(
    'person', metadata,
    Column('personid', Integer, primary_key = True, key='mypersonid'),
    Column('name1', String(30), nullable = False,
              info = {'description' : u"DB-Specifics"}),
    info = {'description' : u"Important Table",
            'order' : 1,
            'key' : 'myperson'})

myperson_i1 = Index('myperson_i1',
                    table_myperson.c.mypersonid, table_myperson.c.name1,
                    unique = True) 


myperson_i2 = Index('myperson_i2',
                    table_myperson.c.name1,
                    unique= False)

table_address = Table(
    'address', metadata,
    Column('addressid', Integer, primary_key = True),
    Column('street', String(50), nullable = False),
    Column('mypersonid', Integer, ForeignKey("person.mypersonid")),
    info = {'order' : 2})

################ Classes / Mappers #####################

class Person(object):
    implements(IMyPerson)

    testprop = property()


class Address(object):
    implements(IAddress)

mapper_myperson = mapper(Person, table_myperson,
                       properties = {
    'addresses' : relation(Address, cascade="all, delete-orphan")})

mapper_address = mapper(Address, table_address)

