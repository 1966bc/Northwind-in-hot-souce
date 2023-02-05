# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  Northwind in hot souce
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
#------------------------------------------------------------------------------

import sys
import time
from PIL import Image
from io import BytesIO
import base64
import wx

class Tools:
    """
    Tools is a class to set, get some usefull things about app widgets.
    """

    def __str__(self):
        return "class: {0}".format((self.__class__.__name__, ))

    def get_image(self, file):

        decode_data = base64.b64decode(file)
        bio = BytesIO(decode_data)
        img = wx.Image(bio)
        
        return img.ConvertToBitmap()

    def get_font(self):
        try:    
            font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPointSize()+1
        except:
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT).GetPointSize()+1

        return font

    def frame_style(self):
        return (wx.DEFAULT_FRAME_STYLE^
               (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)|
               wx.FRAME_FLOAT_ON_PARENT)

    def on_fields_control(self,panel, title):

        msg = "Please fill all fields."

        for i in panel.GetChildren():
            if type(i) in(wx.TextCtrl,wx.ComboBox):
                if len(i.GetValue())==0:
                    wx.MessageBox(msg, title, wx.OK|wx.ICON_INFORMATION)
                    i.SetFocus()
                    return 0
