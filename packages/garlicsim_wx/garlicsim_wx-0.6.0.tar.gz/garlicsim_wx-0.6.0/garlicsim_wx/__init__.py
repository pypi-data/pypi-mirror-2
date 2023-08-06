# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
A wxPython-based GUI for garlicsim.

The final goal of this project is to become a fully-fledged application for
working with simulations, friendly enough that it may be used by
non-programmers.

This program is intended for Python versions 2.5, 2.6 and 2.7, using wxPython
version 2.8.10.1 and upwards. (But not including 2.9.x, which is a development
release.)
'''

from . import bootstrap

import sys
import os.path

import wx

import garlicsim.general_misc.version_info

import garlicsim


from . import misc
from .frame import Frame
from .gui_project import GuiProject
from .app import App


__all__ = ['Frame', 'GuiProject', 'start']


__version_info__ = garlicsim.general_misc.version_info.VersionInfo(0, 6, 0)
__version__ = '0.6.0'


def start():
    '''Start the GUI.'''
    
    # The first argument is the path of the script (or the executable if we're
    # frozen), and that should be cut off:    
    args = sys.argv[1:]
    
    # todo: Consider removing the args we can understand from sys.argv, so
    # program inside will not be confused by them.
        
    new_gui_project_simpack_name = None
    load_gui_project_file_path = None
    
    if args:
        arg = args[0]        
        if arg.startswith('__garlicsim_wx_new='):
            new_gui_project_simpack_name = arg[19:]
        elif os.path.isfile(arg):
            load_gui_project_file_path = arg
    
    app = App(new_gui_project_simpack_name=new_gui_project_simpack_name,
              load_gui_project_file_path=load_gui_project_file_path)
    
    app.MainLoop()
    
    
if __name__ == "__main__":
    
    start()