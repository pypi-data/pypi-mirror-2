#!/usr/bin/env python
# coding=utf-8

# Convert SQLAlchemy table definitions into nicely formatted LaTeX code.

from sa_tools.tools import read_sa_tables, read_sa_indexes, read_sa_classes
from sa_tools.latex import sa2latex
import sys, re, sqlalchemy
from os import path

def usage():
    print "Usage :: sa2latex.py <table_module> [mapper_module]"
    sys.exit(0)

if __name__ == '__main__':

    if len(sys.argv) not in (2,3):
        usage()
        
    table_mod = index_mod = sys.argv[1]

    if len(sys.argv) == 3:
        mapper_mod = sys.argv[2]
    else:
        mapper_mod = None
        
    tables = read_sa_tables(table_mod)
    index_dict = read_sa_indexes(index_mod)
    
    if mapper_mod:
        classes_dict = read_sa_classes(mapper_mod)
    else:
        classes_dict = None
        
    buf = sa2latex(tables, index_dict, classes_dict).encode('utf-8')
    print buf
    
