"""MaxDB specific load/dump functions"""

import re
import sdb.loader
from sqlalchemy.types import Binary
from sqlalchemy.orm import sessionmaker


def db_connect(database, user, password, host):
    session = sdb.loader.Loader ()
    cmd = "USE USER %s %s SERVERDB %s" % (
        user.upper(), password.upper(), database.upper())
    if host not in (None, '', 'localhost'):
        cmd += " ON %s" % host.upper()
    session.cmd(cmd)
    return session
def db_close(session):
    session.release()
    
def dbdump(session, table, fn):
    # Create export commands for binary columns, which will be exported in
    # extra files
    bin_cmd = []
    for i, column in enumerate(table.columns):
        if isinstance(getattr(column.type, 'impl', None), Binary):
            bin_cmd.append("LOB OUTSTREAM %s '%s_bincol-%s.dat'" % (
                column.name, fn, column.name))
    cmd = "EXPORT COLUMNS %s FROM %s DATA OUTSTREAM '%s.csv' %s" % (
        ','.join(column.name for column in table.columns),
        table.name, fn, " ".join(bin_cmd))
    #print cmd
    session.cmd(cmd)

def dbload(engine, loader_session, table, fn, sql_commands):
    # Create load commands for binary columns, which will be imported from
    # extra files
    bin_cmd = []
    for i, column in enumerate(table.columns):
        if isinstance(getattr(column.type, 'impl', None), Binary):
            bin_cmd.append("LOB INSTREAM %s '%s_bincol-%s.dat'" % (
                column.name, fn, column.name))
    cmd = "IMPORT TABLE %s DATA INSTREAM '%s.csv' %s" % (
        table.name, fn, " ".join(bin_cmd))
    # First drop autoincrement serial for primary key, as
    # In this case the IDs are not kept
    loader_session.cmd("ALTER TABLE %s COLUMN %s DROP DEFAULT" % (
        table.name, table.name+'id'))
    for cmds in sql_commands:
        print "SQL before load: %s" % cmds[0]
        loader_session.cmd(cmds[0])
    
    # Load data
    #print cmd
    loader_session.cmd(cmd)

    # Now create serial again
    # First get max id, the base for the new serial
    loader_session.cmd("export columns max(%s) from %s "
                       "data outstream '/tmp/bsploader.tmp'" % (
                           table.name+'id', table.name))
    fd = open("/tmp/bsploader.tmp", "r")
    buf = fd.read()
    fd.close()
    m = re.search('"(.*?)"', buf)
    if m:
        try:
            maxid = int(m.group(1))
        except ValueError:
            maxid = 0
    else:
        # No rows
        maxid = 0
    # Now set new serial (with maxid + 1)
    loader_session.cmd("ALTER TABLE %s COLUMN %s ADD DEFAULT SERIAL(%s)" % (
        table.name, table.name+'id', maxid+1))
    # Now execute various other SQL Commands that are given
    for cmds in sql_commands:
        print "SQL after load: %s" % cmds[1]
        loader_session.cmd(cmds[1])
