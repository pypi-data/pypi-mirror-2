# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied or
# distributed without explicit written permission from Ram Rachum.

'''
This module defines the FoldableWindowContainer class. See its documentation
for more info.
'''

import wx
import wx.calendar
import wx.lib.buttons


class FoldableWindowContainer(wx.Panel):
    '''
    This joins two windows, making a button that makes the auxilary window fold.
    '''
    def __init__(self, parent, id, main_window, foldable_window,
                 where=wx.RIGHT, folded=False, **kwargs):
        wx.Panel.__init__(self, parent, id, **kwargs)

        self.main_window = main_window
        self.foldable_window = foldable_window

        assert where in [wx.TOP, wx.BOTTOM, wx.LEFT, wx.RIGHT]
        
        self.orientation = wx.VERTICAL if where in [wx.TOP, wx.BOTTOM] \
            else wx.HORIZONTAL
        
        sizer = wx.BoxSizer(self.orientation)
        self.SetSizer(sizer)
        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        main_window.Reparent(self.splitter)
        foldable_window.Reparent(self.splitter)

        self.splitter.Split = self.splitter.SplitVertically if \
            self.orientation == wx.HORIZONTAL else \
            self.splitter.SplitHorizontally

        self.main_one_first = where in [wx.BOTTOM, wx.RIGHT]
        self.windows_tuple = (main_window,foldable_window) if \
            self.main_one_first else (foldable_window,main_window)
        self.splitter.SetSashGravity(int(self.main_one_first))

        self.splitter.Split(*self.windows_tuple)
        self.splitter.SetMinimumPaneSize(50)
        self.sash_pos = self.splitter.SashPosition
        if self.main_one_first:
            sizer.Add(self.splitter, 1, wx.EXPAND)

        button_size = (-1,10) if self.orientation == wx.VERTICAL \
                    else (10,-1)
        fold_button = wx.lib.buttons.GenButton(self, -1, size=button_size)
        fold_button.SetBackgroundColour('#668866')
        fold_button.Bind(wx.EVT_BUTTON, self.on_fold_toggle)
        sizer.Add(fold_button, 0, wx.EXPAND)
        if not self.main_one_first:
            sizer.Add(self.splitter, 1, wx.EXPAND)

        sizer.Fit(self)

        if folded:
            self.on_fold_toggle()

    def on_fold_toggle(self, event=None):
        '''
        Toggle the fold status.
        
        If the window is folded, unfold it. If it's not folded, fold it.
        '''
        if self.splitter.IsSplit():
            self.sash_pos = self.splitter.SashPosition
            self.splitter.Unsplit(toRemove=self.foldable_window)
        else:
            self.splitter.Split(self.windows_tuple[0], self.windows_tuple[1],
                                sashPosition=self.sash_pos)


if __name__ == "__main__":
    
    # Testing the foldable window container.
    
    class FoldTest(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            
            left = wx.ScrolledWindow(self, style=wx.BORDER_SUNKEN)
            right = wx.ScrolledWindow(self, style=wx.BORDER_SUNKEN)
            
            left_sizer = wx.BoxSizer(wx.VERTICAL)
            left.SetSizer(left_sizer)
            left_sizer.Add(wx.calendar.CalendarCtrl(left), 1, wx.EXPAND | wx.ALL, 5)
            left_sizer.Add(wx.Button(left, label="Act"), 0, wx.EXPAND | wx.ALL, 5)
            
            right_sizer = wx.BoxSizer(wx.VERTICAL)
            right.SetSizer(right_sizer)
            right_sizer.Add(
                wx.StaticText(right, label="Fold panel", style=wx.BORDER_RAISED),
                1, wx.EXPAND | wx.ALL, 5
            )

            FoldableWindowContainer(self, -1, left, right, wx.RIGHT)

    app = wx.PySimpleApp()
    app.TopWindow = FoldTest()
    app.TopWindow.Show()
    app.MainLoop()
