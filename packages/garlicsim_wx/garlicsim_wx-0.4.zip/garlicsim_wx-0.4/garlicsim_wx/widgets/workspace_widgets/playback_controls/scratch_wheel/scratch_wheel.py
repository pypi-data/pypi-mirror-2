# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the ScratchWheel class.

See its documentation for more info.
'''

from __future__ import division

import wx
import math
import time

from garlicsim_wx.widgets import WorkspaceWidget
from garlicsim_wx.general_misc import cursor_collection
from garlicsim_wx.general_misc import thread_timer
from garlicsim.general_misc import math_tools
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser

import garlicsim, garlicsim_wx
import images


__all__ = ["ScratchWheel"]


class ScratchWheel(wx.Panel):
    '''Widget for visualizing playback and browsing small time intervals.'''
    def __init__(self, parent, gui_project, *args, **kwargs):
        
        if 'style' in kwargs:
            kwargs['style'] |= wx.SUNKEN_BORDER
        else:
            kwargs['style'] = wx.SUNKEN_BORDER
            
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)
        self.Unbind(wx.EVT_ERASE_BACKGROUND) # Good or bad?
        
        self.SetCursor(cursor_collection.get_open_grab())
        
        self.gui_project = gui_project
        '''The gui project that this scratch wheel is attached to.'''
        
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        self.frame_number_that_should_be_drawn = 0
        '''Serial number of the frame that should be drawn.'''
        
        self.current_frame_number = -1
        '''Serial number of the frame that is currently drawn.'''
        # Set to -1 to make sure first drawing won't fuck up
        
        self.image_size = images.get_image_size()
        '''The size of the gear image.'''
        
        self.clock_factor = 0.05 # todo: maybe rename
        '''
        Factor for converting from simulations seconds to radians in the gear.
        '''
        
        self.being_dragged = False
        '''Flag that says whether the gear is currently being dragged.'''
        
        self.grabbed_angle = None
        '''The angle that the user grabbed when starting to drag.'''
        
        self.grabbed_pseudoclock = None
        '''The pseudoclock that the user grabbed when starting to drag.'''
        
        self.angle_while_dragging = None
        
        self.d_angle_while_dragging = None
        
        self.desired_clock_while_dragging = None
                
        self.last_tracked_time_and_angle = (0, 0)
        '''A tuple of (time, angle) that was recorded for velocity tracking.'''
        
        self.current_velocity_estimate = 0
        '''
        The current estimate of the gear's velocity.
        
        The units are radian per second, and that's a real world second, not in
        the simulation.
        '''
        
        self.velocity_for_maximal_motion_blur = 10
        '''Velocity in which the scratch wheel will get maximal motion blur.'''
        
        self.current_motion_blur_bitmap = None
        '''The current bitmap to use for motion blur.'''
        
        self.velocity_time_sampling_minimum = 0.05
        '''The minimum interval over which we can measure the gear's velocity.'''
        
        self.was_playing_before_drag = None
        '''Flag saying if playback was active before user grabbed the gear.'''
            
        self.motion_blur_update_timer = thread_timer.ThreadTimer(self)
        '''
        Timer to use for updating the motion blur bitmap.
        
        The motion blur bitmap must get updated periodically as long as its last
        value was non-zero, even if the user doesn't touch anything. This is
        because we don't want to have a situtation where the user dragged fast,
        got a high motion blur, left the scratch wheel, and then the wheel is
        frozen with a high motion blur.
        '''
        
        self.Bind(thread_timer.EVT_THREAD_TIMER,
                  self.on_motion_blur_update_timer,
                  self.motion_blur_update_timer)
        
        # todo: I don't think ThreadTimer should be used here. But for some
        # reason wx.Timer didn't work.
        
        self.recalculation_flag = False
        '''Flag saying whether the scratch wheel needs to recalculate.'''
        
        self.needs_recalculation_emitter = \
            self.gui_project.emitter_system.make_emitter(
                inputs=(
                    self.gui_project.pseudoclock_modified_emitter,
                    self.gui_project.active_node_changed_emitter # todo: needed?
                ),
                outputs=(
                    FlagRaiser(self, 'recalculation_flag',
                               function=self._recalculate, delay=0.03),
                ),
                name='needs_recalculation',
            )
        
        
        self.needs_recalculation_emitter.emit()
        
        
    """
    @staticmethod
    def _pos_to_angle(pos):
        return -math.acos(-1 + 2*pos)
    
    @staticmethod
    def _angle_to_pos(angle):
        return (1 + math.cos(-angle)) / 2
    """
    
    @staticmethod
    def _expanded_pos_to_angle(pos):
        '''Convert from pos to angle, expanded.'''
        pos = (pos * 0.8) + 0.1
        return -math.pi * (1 - pos)
    
    
    @staticmethod    
    def _expanded_angle_to_pos(angle):
        '''Convert from angle to pos, expanded.'''
        pos = 1 - (angle / (-math.pi))
        return (pos - 0.1) / 0.8

    
    def get_current_angle(self):
        '''Get the angle that the scratch wheel should be in.'''
        return self.gui_project.pseudoclock * self.clock_factor
                    
    
    def _recalculate(self, possibly_refresh=True):
        '''
        Recalculate the scratch wheel.
        
        If `possibly_refresh` is True, and this function sees that the image on
        the scratch wheel should change, then it will trigger a `Refresh`.
        '''
        angle = self.get_current_angle()
        frame_number = int(
            ((angle % ((2/3) * math.pi)) / (2 * math.pi)) * 3 * images.N_FRAMES
        )
        if frame_number == images.N_FRAMES:
            frame_number =- 1
        
        if self.frame_number_that_should_be_drawn != frame_number:
            self.frame_number_that_should_be_drawn = frame_number
            if possibly_refresh:
                self.Refresh()
            
        
        self.__update_motion_blur_bitmap(possibly_refresh)
        
        self.recalculation_flag = False
    
    def __update_motion_blur_bitmap(self, possibly_refresh):
        '''
        Check the speed and update the motion blur bitmap if necessary.
        
        If `possibly_refresh` is True, and this function sees that the image on
        the scratch wheel should change, then it will trigger a `Refresh`.
        '''

        current = (time.time(), self.get_current_angle())
        last = self.last_tracked_time_and_angle

        d_time = current[0] - last[0]
        d_angle = current[1] - last[1]
        
        if d_time < self.velocity_time_sampling_minimum:
            return
            # This protects us from two things: Having a grossly inaccurate
            # velocity reading because of tiny sample, and having a division by
            # zero.
        
        self.current_velocity_estimate = velocity = d_angle / d_time

        r_velocity = velocity / self.velocity_for_maximal_motion_blur

        alpha = min(abs(r_velocity), 1)
        
        alpha = min(alpha, 0.8)
        # I'm limiting the alpha, still want to see some animation
        
        new_motion_blur_image = images.get_blurred_gear_image_by_ratio(alpha)
        
        if self.current_motion_blur_bitmap != new_motion_blur_image:
            self.current_motion_blur_bitmap = new_motion_blur_image
            if possibly_refresh:
                self.Refresh()
        
        if new_motion_blur_image is not \
           images.get_blurred_gear_image_by_ratio(0):
            # We have a non-zero visible motion blur
            
            self.motion_blur_update_timer.Start(30)
        
        else:
            
            self.motion_blur_update_timer.Stop()
            
        self.last_tracked_time_and_angle = current
            
    def on_paint(self, event):
        '''EVT_PAINT handler.'''
        # todo: optimization: if motion blur is (rounded to) zero, don't draw
        
        event.Skip()
        
        if self.recalculation_flag:
            self._recalculate(possibly_refresh=False)
            # We make sure `_recalculate` won't refresh, because that would make
            # an infinite loop
            
        bw, bh = self.GetWindowBorderSize()
        
        ox, oy = ((4 - bw) / 2 , (4 - bh) / 2)
        
        bitmap = images.get_image(self.frame_number_that_should_be_drawn)
        dc = wx.PaintDC(self)
        dc.DrawBitmap(bitmap, ox, oy)
        dc.DrawBitmap(self.current_motion_blur_bitmap, ox, oy, useMask=True)
        # todo: Is the way I draw the bitmap the fastest way?
        self.current_frame_number = self.frame_number_that_should_be_drawn
            
    def on_mouse_event(self, e):
        '''EVT_MOUSE_EVENTS handler.'''
        # todo: possibly do momentum, like in old shockwave carouselle.
        # todo: right click should give context menu with 'Sensitivity...' and
        # 'Disable'
        # todo: make check: if left up and has capture, release capture

        self.Refresh()
        
        (w, h) = self.GetClientSize()
        (x, y) = e.GetPositionTuple()
        (rx, ry) = (x/w, y/h)
        
        if e.LeftDown():
            self.angle_while_dragging = self.grabbed_angle = self._expanded_pos_to_angle(rx)
            self.d_angle_while_dragging = 0
            self.desired_clock_while_dragging = self.grabbed_pseudoclock = \
                self.gui_project.pseudoclock
            self.was_playing_before_drag = self.gui_project.is_playing
            self.gui_project.stop_playing()
            self.being_dragged = True
            
            self.SetCursor(cursor_collection.get_closed_grab())
            # SetCursor must be before CaptureMouse because of wxPython/GTK
            # weirdness
            self.CaptureMouse()
            
            return
        
        if e.LeftIsDown():
            if not self.HasCapture():
                return
            self.angle_while_dragging = self._expanded_pos_to_angle(rx)
            self.d_angle_while_dragging = (self.angle_while_dragging - self.grabbed_angle)
            
            desired_pseudoclock = self.grabbed_pseudoclock + \
                (self.d_angle_while_dragging / self.clock_factor)
            
            self.gui_project.set_pseudoclock(desired_pseudoclock)
            
            if self.gui_project.pseudoclock != desired_pseudoclock:
                # Means we got an edge node
                
                edge_clock = self.gui_project.active_node.state.clock
                direction = cmp(self.gui_project.pseudoclock,
                                desired_pseudoclock)
                # direction that we bring back the cursor to if it goes too far
                d_clock = (edge_clock - self.grabbed_pseudoclock)
                d_angle = d_clock * self.clock_factor
                edge_angle = self.grabbed_angle + d_angle
                edge_rx = self._expanded_angle_to_pos(edge_angle)
                edge_x = edge_rx * w
                is_going_over = \
                    (edge_x - x > 0) if direction == 1 else (edge_x - x < 0)
                if is_going_over:
                    self.WarpPointer(edge_x, y)
            
                
        if e.LeftUp(): #or e.Leaving():
            # todo: make sure that when leaving entire app, things don't get
            # fucked
            if self.HasCapture():
                self.ReleaseMouse()
            # SetCursor must be after ReleaseMouse because of wxPython/GTK
            # weirdness
            self.SetCursor(cursor_collection.get_open_grab())
            self.being_dragged = False
            self.grabbed_angle = None
            self.grabbed_pseudoclock = None
            self.angle_while_dragging = None
            self.d_angle_while_dragging = None
            self.desired_clock_while_dragging = None
            
            if self.was_playing_before_drag:
                self.gui_project.start_playing()
                
            self.gui_project.round_pseudoclock_to_active_node()
                
            self.was_playing_before_drag = None
            

    def on_size(self, event):
        '''EVT_SIZE handler.'''
        self.Refresh()
        if event is not None:
            event.Skip()
    
    def on_motion_blur_update_timer(self, event):
        '''Handler for when the motion blur timer goes off.'''
        self.recalculation_flag = True
        self.Refresh()
        
        
        
