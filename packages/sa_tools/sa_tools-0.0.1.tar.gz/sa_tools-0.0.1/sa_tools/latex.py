# coding=utf-8

""" Functions that can be used to generate latex documentation from
SA table definitions / mappers etc."""

import sys, re
import sqlalchemy
from zope.interface import implementedBy
from sa_tools.tools import read_sa_tables, read_sa_indexes, read_sa_classes,\
     get_tablenames

def tex_esc(s):
    """ Escape latex commands """
    s=unicode(s)
    if s:
        for c in '&%#_{}':
            s = re.sub(c,'\\'+c,s)
        for c in '<>':
            s = re.sub(c,'$%s$'%c,s)

    return s

def yesno(b):
    if b:
        return 'Y'
    else:
        return 'N'

def none2str(s):
    if s:
        return s
    else:
        return ''

def icol2str(cols):
    """ Convert eventual tuple to string """
    if isinstance(cols, basestring):
        return cols
    else:
        return (', '.join(cols))


def sa_type2str(t):
    """ Print SA type and certain attributes """
    s = t.__class__.__name__
    if isinstance(t, sqlalchemy.String):
        if t.length != None:
            s += u"(%s)" % t.length
    return s

def sa_default2str(t):
    """ Return Default value as string"""
    if t == None:
        return ''
    return str(t.arg)

def usage():
    print "Usage :: %s TABLE_MODULE" % sys.argv[0]
    sys.exit(0)

def latex_table_header(table, klassname, klass):
    """ Print Table header """
    tablename, realname = get_tablenames(table)
    tcode = []
    tcode.append(u"\\parskip6ex")
    tcode.append(u"\\parbox{15cm}{")
    buf = u"{\\bf Table  %s}" % tex_esc(tablename)
    if realname:
        buf = buf + u" (%s)" % tex_esc(realname)
    buf += u"\\\\"
    tcode.append(buf)
    if klass:
        tcode.append(u"Mapped to Class {\\bf %s} \\\\" % \
                     tex_esc(klassname))
    return tcode

def latex_table_desc(interface = None, table = None):
    # Table description
    if interface:
        if_description = getattr(interface, '__doc__', None)
    else:
        if_description = None
    db_description = table.info.get('description', None)

    description = ''
    if if_description:
        # Interface-related description
        description += tex_esc(if_description)
    if db_description:
        # Database-related description
        description += u"{\\bf DB: }" + tex_esc(db_description)
    return description

def latex_table_columns(table, interface = None):
    """ Write latex Code for columns """
    tcode = []
    for column in table.columns:
        # Create description
        if interface:
            field = interface.get(column.key, None)

        if interface and field:
            if_description = getattr(field, 'description', None)
        else:
            if_description = None
        db_description = column.info.get('description', None)
        description = ''
        if if_description:
            description += tex_esc(if_description)
        if column.key != column.name:
            crealname = u"(%s)" % column.name
        else:
            crealname = ""
        if db_description:
            description += u"{\\bf DB: }" + tex_esc(db_description)
        tcode.append(u"%s %s& " % (tex_esc(column.key),
                                   tex_esc(crealname)) +\
                     u"%s & " % tex_esc(sa_type2str(column.type)) +\
                     u"%s & " % yesno(column.primary_key) +\
                     u"%s & " % yesno(column.nullable) +\
                     u"%s &" % tex_esc(sa_default2str(column.default)) +\
                     u"%s" % description +\
                     u"\\\\")
        tcode.append(u"\\hline")
    return tcode


def latex_table_indexes(table, indexes):
    """ Output a table of indexes """
    tablename = get_tablenames(table)[0]
    tcode = []
    tcode.append(u"\\parskip2ex")
    tcode.append(u"\\parbox{9cm}{")
    tcode.append(u"Indexes for table %s:\\\\" % tablename)
    tcode.append(u"\\begin{tabular}{|l|l|l|}")
    tcode.append(u"\\hline")
    tcode.append(u"{\\bf Name} & {\\bf Columns} & {\\bf Unique}\\\\")
    tcode.append(u"\\hline")
    for index in indexes:
        colnames = []
        for c in index.columns:
            colnames.append(c.key)
        tcode.append(u"%s & " % tex_esc(index.name) +\
                     u"%s & " % tex_esc(', '.join(colnames)) +\
                     u"%s" % yesno(index.unique))
        tcode.append(u"\\\\")
        tcode.append(u"\\hline")
    tcode.append(u"\\end{tabular}")
    tcode.append(u"}")
    tcode.append(u"")
    return tcode

def latex_table_props(prop_dict, interface = None):
    """ Return SA Properties """
    tcode = []
    tcode.append(u"\\parskip2ex")
    tcode.append(u"\\parbox{15cm}{")
    tcode.append(u"Properties: \\\\")
    tcode.append(u"\\begin{tabular}{|l|l|l|l|l|p{5cm}|}")
    tcode.append(u"\\hline")
    tcode.append(u"{\\bf Name} & {\\bf RelClass} & {\\bf Lazy} & "\
                 u"{\\bf Sec}"\
                 u"& {\\bf BRef} & {\\bf Description}\\\\")
    tcode.append(u"\\hline")
    for propname, prop in prop_dict.items():
        # Create description
        if interface:
            field = interface.get(propname, None)
        if interface and field:
            if_description = getattr(field, 'description', '')
        else:
            if_description = ''
        # Get eventual secondary tables
        if prop.secondary:
            secondary = prop.secondary.key
        else:
            secondary = ''
        # Find out if property is from a backref or direct
        from sqlalchemy.orm.mapper import Mapper
        if isinstance(prop.argument, Mapper):
            # It's backreferenced
            mapclass = prop.argument.class_.__name__
            backref = ' $\\leftarrow$ ' + prop.backref.key
        else:
            # It is not, check if it has a backref
            mapclass = prop.argument.__name__
            if prop.backref:
                backref = ' $\\rightarrow$ ' + prop.backref.key
            else:
                backref = ''
        
        tcode.append(u"%s & " % tex_esc(prop.key) +\
                     u"%s & " % tex_esc(mapclass) +\
                     u"%s & " % yesno(prop.lazy) +\
                     u"%s &" % tex_esc(secondary) +\
                     u"%s &" % tex_esc(backref) +\
                     u"%s" % tex_esc(if_description))
        tcode.append(u"\\\\")
        tcode.append(u"\\hline")
    tcode.append(u"\\end{tabular}")
    tcode.append(u"}")
    tcode.append(u"")
    return tcode

def latex_table_classprops(sa_class, interface=None):
    """ Retrieve / display class properties """
    tcode = []
    properties = []
    for name, attr in sa_class.__dict__.items():
        if isinstance(attr, property):
            properties.append((name, attr))
    # Display properties in case there are any
    if properties:
        tcode.append(u"\\parskip2ex")
        tcode.append(u"\\parbox{15cm}{")
        tcode.append(u"Properties in class {\\bf %s}: \\\\" % \
                     sa_class.__name__)
        tcode.append(u"\\begin{tabular}{|l|l|}")
        tcode.append(u"\\hline")
        tcode.append(u"{\\bf Name} & {\\bf Description} \\\\")
        tcode.append(u"\\hline")
        for name, attr in properties:
            # Create description
            if interface:
                field = interface.get(name, None)
            if interface and field:
                if_description = getattr(field, 'description', '')
            else:
                if_description = ''
            tcode.append(u"%s & " % tex_esc(name) +\
                         u"%s" % if_description)
            tcode.append(u"\\\\")
            tcode.append(u"\\hline")
        tcode.append(u"\\end{tabular}")
        tcode.append(u"}")
        tcode.append(u"")
    return tcode

def sa2latex(tables, index_dict = None, class_dict = None):
    """ Read tables / indexes and mappers and return
    nicely formatted LaTeX tables """

    tcode = []

    if index_dict == None:
        index_dict = {}
    if class_dict == None:
        class_dict = {}
    for table in tables:
        tablename, realname = get_tablenames(table)
        klassname, klass, prop_dict = class_dict.get(tablename, (None,
                                                                 None,
                                                                 None))
        if klass:
            # Try to get an interface
            interfaces = list(implementedBy(klass))
            if interfaces:
                interface = interfaces[0]
            else:
                interface = None
        else:
            interface = None
        # Now let's talk LaTeX !!!
        # Add header
        tcode.extend(latex_table_header(table, klassname, klass))
        # Add table description
        table_description = latex_table_desc(interface, table)
        if table_description:
            tcode.append(u"%s \\\\" % table_description)

        # Add column headers
        tcode.append(u"\\begin{tabular}{|p{2.8cm}|l|l|l|l|p{7cm}|}")
        tcode.append(u"\\hline")
        tcode.append(u"{\\bf Name} & {\\bf Type} & {\\bf P} & {\\bf N} & "\
                     u"{\\bf D} & {\\bf Description}\\\\")
        tcode.append(u"\\hline \\hline")

        # Add Columns
        tcode.extend(latex_table_columns(table, interface))

        # Add column footer
        tcode.append(u"\\end{tabular}")
        tcode.append(u"}")
        tcode.append(u"")

        # Add Indexes
        indexes = index_dict.get(tablename)
        if indexes:
            tcode.extend(latex_table_indexes(table, indexes))

        # Add SA Properties
        if prop_dict:
            tcode.extend(latex_table_props(prop_dict, interface))

        # Add Class Properties
        if class_dict:
            buf = class_dict.get(tablename)
            if buf:
                sa_class = buf[1]
                if sa_class:
                    tcode.extend(latex_table_classprops(sa_class, interface))

        
    return u"\n".join(tcode)
