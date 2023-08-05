"""Exporting / Importing tools (dump/restore etc.)"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

FILENAME_PATTERN = "%s/BSPTBL_%s_%s"

def mkDSN(db_name, db_username, db_password, db_host, db_type='maxdb'):
    """Create database DSN out of DSN elements"""
    if db_type == 'maxdb':
        # Silly MaxDB can only handle upper case specifiers
        db_name = db_name.upper()
        db_username = db_username.upper()
        db_password = db_password.upper()
    userpass = ''
    if db_username:
        userpass += db_username
        if db_password:
            userpass += ':' + db_password
    if db_host == 'localhost':
        db_host = ''
    if db_host and userpass:
        db_host = userpass + '@' + db_host
    elif not db_host and userpass:
        db_host = userpass + '@localhost'
    return '%s://%s/%s' % (db_type, db_host, db_name)

def load_modules(dialect):
    """Load right modules according to database dialect"""
    if dialect == 'maxdb':
        global dbdump, dbload, db_connect, db_close
        from sa_tools.dump.maxdb import dbdump, dbload, db_connect, db_close
    else:
        raise NotImplementedError("Dialect %s not implemented!" % dialect)

def dump_table_data(metadata, database, user, 
                    password, host = None, filename = 'now', 
                    dirname = '.', dialect='maxdb'):
    """Dump table data into a file"""
    path = os.path.join(os.getcwd(), dirname)
    load_modules(dialect)
    # Connect to database
    conn = db_connect(database, user, password, host)
    # Dump table in reverse order to omit referential integrity problems
    # due to the possibility that data is added during the dump
    for table in reversed(metadata.sorted_tables):
        print "Dumping table %s" % table.name
        dbdump(conn, table, FILENAME_PATTERN % (path, table.name, filename))
    db_close(conn)    
    
def drop_tables(metadata, database, user, 
                password, host = None, dialect='maxdb', engine = None):
    """Drop all database tables"""
    if engine is None:
        engine = create_engine(mkDSN(database, user, password, host), 
                               echo=False)
    metadata.drop_all(bind=engine)
    
def create_tables(metadata, database, user, 
                  password, host = None, dialect='maxdb', engine = None):
    """Create database tables"""
    if engine is None:
        engine = create_engine(mkDSN(database, user, password, host), 
                               echo=False)
    metadata.create_all(bind=engine)

def create_indexes(metadata, database, user, 
                password, host = None, dialect='maxdb', engine = None):
    """Create indexes"""
    if engine is None:
        engine = create_engine(mkDSN(database, user, password, host), 
                               echo=False)
    
def load_table_data(metadata, database, user, 
              password, host = None, filename = 'now', 
              dirname = '.', dialect='maxdb', 
              recreate_tables = True, create_indexes = True, 
              engine = None, sql_commands = None, done_tables = None):
    """Delete/Recreate all tables and load data"""
    load_modules(dialect)
    # Make empty dict if sql_commands = None
    if sql_commands is None:
        sql_commands = {}
    if engine is None:
        engine = create_engine(mkDSN(database, user, password, host), 
                               echo=False)
    if done_tables is None:
        done_tables = []
    if done_tables:
        # Some tables are done, so don't recreate all tables
        recreate_tables = False
        tables = (table for table in metadata.sorted_tables if 
                  table.name not in done_tables)
    else:
        tables = (table for table in metadata.sorted_tables)
    if recreate_tables:
        # Drop and load tables
        print "Dropping/Creating tables"
        drop_tables(metadata, database, user, 
                    password, host = host, dialect=dialect, engine = engine)
        create_tables(metadata, database, user, 
                      password, host = host, dialect=dialect, engine = engine)
    # Connect to database
    conn = db_connect(database, user, password, host)
    path = os.path.join(os.getcwd(), dirname)
    
    for table in tables:
        print "Loading table %s" % table.name
        dbload(engine, conn, table, FILENAME_PATTERN % (
            path, table.name, filename), 
            sql_commands.get(table.name, []))
    db_close(conn)    
    
