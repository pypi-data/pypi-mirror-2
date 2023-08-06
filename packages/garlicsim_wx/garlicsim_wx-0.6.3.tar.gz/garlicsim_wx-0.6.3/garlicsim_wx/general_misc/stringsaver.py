# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A little module for cataloging strings.
'''

stringsaver_catalog = []

def s2i(string):
    '''
    If the string isn't cataloged already, catalog it.
    
    In any case, returns the number associated with the string.
    '''
    global stringsaver_catalog
    if string in stringsaver_catalog:
        return stringsaver_catalog.index(string) + 1
    else:
        stringsaver_catalog.append(string)
        return stringsaver_catalog.index(string) + 1


def i2s(integer):
    '''
    Return the string cataloged under the given integer.
    '''
    return stringsaver_catalog[integer - 1]
