# coding = utf-8

""" Several functions that can be used to parse table / index and
mapper definition files """

import sys, re
import sqlalchemy
import sqlalchemy.types
from sqlalchemy.orm.properties import PropertyLoader

def file_import(pymod_file):
    """ Try to import a given file as a Python module and return its
    local dictionary
    OBSOLETE - NOT NEEDED ANY MORE"""
    d = path.dirname(pymod_file)
    if d not in sys.path:
        sys.path.insert(0, d)

    # And now import the module
    modname = path.splitext(path.basename(pymod_file))[0]
    mod =  __import__(modname)
    return modname, mod, mod.__dict__
    
def mod_import(modname):
    """ Try to import a given python module and return its local
    dictionary """

    mod = __import__(modname, None, None, [''])

    return mod, mod.__dict__

def get_tablenames(table):
    tablename = table.info.get('key', None)
    if tablename:
        # The realname differs from the application-table name
        realname = table.name
    else:
        tablename = table.name
        realname = None
    return tablename, realname

def read_sa_tables(modname):
    """ Read in table and index definitions of a Python/SQLAlchemy-Table
    module and return a data structure that holds all this information """
    
    mod, moddict = mod_import(modname)

    tables = []
    # Now read one after each table
    for name, table in moddict.items():
        if isinstance(table, sqlalchemy.Table):
            # Yes, it's a table, retrieve order
            order = table.info.get('order', 0)
            tables.append((order, table))
            
    # Sort tables
    tables.sort()
    otables = []
    for table in tables:
        otables.append(table[1])
    return otables

def read_sa_indexes(modname):
    """ Read in index definitions of a Python/SQLAlchemy Index module
    and return a dictionary holding these indexes """

    mod, moddict = mod_import(modname)

    # Search for indexes
    index_dict = {}
    for indexname, index in moddict.items():
        if isinstance(index, sqlalchemy.Index):
            tablename, realname = get_tablenames(index.table)
            idx = index_dict.get(tablename, None)
            if idx == None:
                index_dict[tablename] = [index]
            else:
                idx.append(index)

    return index_dict

def read_sa_classes(modname):
    """ Read mapped class definitions from a Python/SQLAlchemy module
    and return a mapped class dictionary holding these mappers/classes """

    from sqlalchemy.orm import class_mapper
    from sqlalchemy.exceptions import InvalidRequestError
    from sqlalchemy.orm.attributes import InstrumentedAttribute
    from sqlalchemy.orm.properties import PropertyLoader
    mod, moddict = mod_import(modname)

    # Search for classes
    class_dict = {}
    for klassname, klass in moddict.items():
        if isinstance(klass, type):
            try:
                table = class_mapper(klass).mapped_table
            except InvalidRequestError:
                pass
            else:
                prop_dict = {}
                for name in dir(klass):
                    attr = getattr(klass, name)
                    if isinstance(attr, InstrumentedAttribute):
                        prop = attr.property
                        if isinstance(prop, PropertyLoader):
                            prop_dict[name] = prop
                # The dictionary key should be the translated name
                tname = table.info.get('key', None)
                if tname == None:
                    tname = table.name
                class_dict[tname] = (klassname,
                                     klass,
                                     prop_dict)
    return class_dict
                                          




def load_db(engine, table_mod, drop_tables = False):
    """ Load tables, data and indexes into a given database.  Data
    files are in CSV format in the given dir 'data_dir', are postfixed
    by 'data_prefix', have either the name of the database table or
    the SA-name (attribute data_tablenames) and have the suffix
    'data_suffix':

    data_dir/tablename+'-'+data_postfix+'.'+data_suffix

    Data is delimited by 'data_delimiter'

    The strategy is to first create the table/indexes, then load data.
    """
    
    from bsp.db.tables import metadata
    # First check if metadata is available in the table module
    mod, moddict = mod_import(table_mod)
    metadata = moddict.get('metadata', None)
    if metadata is not None:
        if drop_tables:
            metadata.drop_all(bind=engine)
        metadata.create_all(bind=engine)
    else:
        tables = read_sa_tables(table_mod)
    
        for table in tables:
            tablename, realname = get_tablenames(table)
    
            # Drop/Create Table (Indexes will also be created in this step)
            if drop_tables:
                table.drop(bind=engine, checkfirst = True)
            table.create(bind=engine, checkfirst = True)

def load_data(conn, table, csv_file, delete_data = False,
              null = '?NULL?', data_delimiter = ','):
    """Load data from CSV-file into database table"""

    cols = [c for c in table.columns]
    cols_keys = [c.key for c in table.columns]
    cols_len = len(cols)

    for line in file(csv_file):
        values = line.strip().split(data_delimiter)
        if len(values) != cols_len:
            raise ValueError(
                "len(CSV-Data)!= len(table.columns): %s != %s, data: %s" % (
                    len(values), cols_len, line))

        # Convert values to correct datatype
        cvalues = []
        for i, value in enumerate(values):
            data_type = type(cols[i].type)
            # NULL
            if value == null:
                cvalues.append(None)
            # Integer            
            elif data_type == sqlalchemy.types.Integer:
                cvalues.append(int(value))
            else:
                # String
                cvalues.append(value)

        valdict = dict(zip(cols_keys, cvalues))
        ins = table.insert(values = valdict)
        conn.execute(ins)

def mk_likestr(buf):
    """Wildcard conversion tool"""
    # First test, if SQL-like should be applied or not
    like = False
    # Test, if the unescaped characters "*" or "?" are in the string
    if re.search('.*(?<!\\\)[\*\?].*', buf):
        like = True
    if like:
        # Escape SQL wildcards
        buf = buf.replace('%', '\%')
        buf = buf.replace('_', '\_')
        # Replace non-escaped wildcards with SQL wildcards
        buf = re.sub('(?<!\\\)\*', '%', buf)
        buf = re.sub('(?<!\\\)\?', '_', buf)
    # Remove escape characters
    buf = buf.replace('\*', '*')
    buf = buf.replace('\?', '?')
    return buf, like


if __name__ == '__main__':

    if len(sys.argv) not in (2,3):
        raise AttributeError("wrong number of arguments")
    else:
        table_mod = index_mod = sys.argv[1]

    if len(sys.argv) == 3:
        mapper_mod = sys.argv[2]
    else:
        mapper_mod = None
        

    tables = read_sa_tables(table_mod)
    indexes = read_sa_indexes(index_mod)
    classes = read_sa_classes(mapper_mod)
    for key, value in classes.items():
        print key, value
        print

    
