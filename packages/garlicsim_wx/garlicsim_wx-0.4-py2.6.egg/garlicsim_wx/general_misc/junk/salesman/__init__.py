from salesman import *

wx_installed=False
try:
    import wx
    wx_installed=True
except ImportError:
    pass

if wx_installed:
    from salesmangui import *
