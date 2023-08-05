=========================
SQL Alchemy related tools
=========================

This package consists of several tools for reading / interpreting
SA-related Python modules. These tools can be basically grouped
in two application domains:

(1) Retrieving SA-related information

(2) Displaying / Prettifying this information.

In order to store additional information such as descriptions together
with database definitions, the "info" attribute of the
sqlalchemy.Table and sqlalchemy.Column can be used. This information
will be used by sa_tools.

 >>> from sqlalchemy import Table, Column, Index
 >>> from sqlalchemy import MetaData, Integer, String
 >>> metadata = MetaData()
 >>> mycol = Column('mypersonid', Integer, primary_key = True,\
 ...                info = {'description' : 'Identification key'})
 >>> myperson = Table( 'person', metadata, mycol,
 ...                   info = {'description' : 'Person Table',
 ...                           'key' : 'myperson',
 ...                           'order' : 1})
 >>>

The items in the info dictionaries are used as follows

Table:
- description (For describing database-related issues)
- order (For specifying the order in display-related functions but
  also for table/index creation)
- key (For giving the table an alternate name)

Column:
- description( For describing database-related issues)

In order to successfully parse table and mapper modules, several
conventions have to be made in the table/index and mapper 
declarations:

- Indexes must be prefixed with "index_" and postfixed with a unique
  identifier of the index, such as "_i1". In order to relate an index
  with a table, it has to be named in the index, e.g. "index_person_i1".

Indexes are defined as SQLAlchemy Index objects as follows:

 >>> person_i1 = Index ('person_i1',            # Index name
 ...                    myperson.c.mypersonid,  # Columns
 ...                    unique = True)          # Unique

(For testing purposes, a module with two sample tables and according
interfaces and mappers have been placed in the tests directory. This
module is the base for all further tests.)


 >>> from sa_tools.tools import read_sa_tables, read_sa_indexes, read_sa_classes

Tables are read into a list via read_sa_tables

 >>> tables = read_sa_tables('sa_tools.tests.tables')
 >>> for table in tables:
 ...   print table.name 
 person
 address

Indexes are read via read_sa_indexes

 >>> index_dict = read_sa_indexes('sa_tools.tests.tables')
 >>> print index_dict
 {'myperson': [Index("myperson_i1", Column('personid', Integer(), table=<person>, key='mypersonid', primary_key=True, nullable=False), Column('name1', String(length=30, convert_unicode=False, assert_unicode=None), table=<person>, nullable=False), unique=True), Index("myperson_i2", Column('name1', String(length=30, convert_unicode=False, assert_unicode=None), table=<person>, nullable=False))]}

If classes are mapped to the tables, they can also be retrieved.
sa_tools provide the function read_sa_classes for that:

 >>> class_dict = read_sa_classes('sa_tools.tests.tables')
 >>> for key, value in class_dict.items():
 ...   print key
 myperson
 address
 >>> class_dict['myperson'][0]
 'Person'
 >>> class_dict['myperson'][1]
 <class 'sa_tools.tests.tables.Person'>
 >>> class_dict['myperson'][2].keys()
 ['addresses']

This information can then be used to create tables and indexes. First
an SQLAlchemy engine has to be created

 >>> from sqlalchemy import create_engine
 >>> engine = create_engine('sqlite:///:memory:', echo = False)

Now, the tables can be easily created with the load_db function:

 >>> from sa_tools.tools import load_db
 >>> load_db(engine, 'sa_tools.tests.tables')

 >>> load_db(engine, 'sa_tools.tests.tables', drop_tables = True)

Any indexes will also be created along with the tables.

It is also possible to load data in this stage:

FIXME, FIXME!!!


The second part is the conversion of the above information into latex
code, which can then be included in the documentation. This is documented
and tested in the doctest "latex.txt". The basic usage is as follows:

 >>> from sa_tools.latex import sa2latex
 >>> dummy = sa2latex(tables, index_dict, class_dict)
