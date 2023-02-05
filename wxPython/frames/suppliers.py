#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  Northwind in hot souce
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
# -----------------------------------------------------------------------------
import wx
import frames.supplier as ui

SQL = "SELECT * FROM suppliers ORDER BY company ASC;"


class UI(wx.Frame ):
    def __init__(self,parent):
        wx.Frame.__init__(self,
                          parent,
                          wx.ID_ANY,
                          title = "Suppliers",
                          style = wx.GetApp().engine.frame_style(),
                          name  ="suppliers")
        
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.on_cancel)
        self.table = "suppliers"
        self.primary_key = "supplier_id"
        self.init_ui()
        
    def init_ui(self):
        
        self.panel = wx.Panel(self)
        
        self.stItems = wx.StaticText(self.panel, wx.ID_ANY, "Suppliers")

        self.lstItems = wx.ListBox(self.panel, size=(wx.GetApp().engine.get_font() * 15,
                                                     wx.GetApp().engine.get_font() * 20),
                                   style=wx.LB_OWNERDRAW)

        self.Bind(wx.EVT_LISTBOX, self.on_item_selected, self.lstItems)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_item_activated, self.lstItems)

        sb_buttons = wx.StaticBox(self.panel, wx.ID_ANY, "")

        bts = [(wx.ID_ANY, "&Add", self.on_add),
               (wx.ID_ANY, "&Edit", self.on_item_activated),
               (wx.ID_ANY, "&Close", self.on_cancel)]

        for btn in bts: 
             b = wx.Button(self.panel, btn[0], btn[1],) 
             b.Bind(wx.EVT_BUTTON, btn[2])

        #do layout
        box_main = wx.BoxSizer(wx.HORIZONTAL)
        box_left = wx.BoxSizer(wx.VERTICAL)
        box_right = wx.StaticBoxSizer(sb_buttons, wx.VERTICAL)

        items = ((self.stItems, 0, 5),(self.lstItems, 4, 5),)
        for item in items:
            box_left.Add(item[0], item[1], wx.EXPAND|wx.ALL, item[2])
        
            
        for item in self.panel.GetChildren():
            if type(item) == wx.Button:
                box_right.Add(item, 0, wx.EXPAND|wx.ALL, 5)

        boxes = ((box_left, 1),(box_right, 0))
        for box in boxes:
            box_main.Add(box[0], box[1], wx.EXPAND|wx.ALL, 5)   

        self.panel.SetSizer(box_main)
        box_main.Fit(self)
        box_main.SetSizeHints(self)

    def on_open(self,):
        
        self.set_values()

    def set_values(self,):

        self.lstItems.Clear()
        index = 0
        self.dict_items = {}

        rs = wx.GetApp().engine.read(True, SQL, ())

        for i in rs:
            s = "{:}".format(i[1])
            self.lstItems.Append(s)
            if i[2] != 1:
                # this semms not working...
                self.lstItems.SetItemForegroundColour(index, wx.Colour(219, 112, 219))
            self.dict_items[index] = i[0]
            index += 1

        msg = "Items: {0}".format(self.lstItems.GetCount())
        self.stItems.SetLabel(msg)            

    def on_add(self, event=None):

        obj = ui.UI(self)
        obj.on_open()
        obj.Center()
        obj.ShowModal()
        
    def on_item_selected(self, evt):

        index = self.lstItems.GetSelection()
        if index != -1:
            pk = self.dict_items.get(index)
            self.selected_item = wx.GetApp().engine.get_selected(self.table,
                                                                 self.primary_key,
                                                                 pk)
                
    def on_item_activated(self,evt):

        index = self.lstItems.GetSelection()
        if index != -1:
            obj = ui.UI(self, index)
            obj.on_open()
            obj.Center()
            obj.ShowModal()

        else:
            wx.MessageBox(wx.GetApp().engine.no_selected,
                          wx.GetApp().GetAppDisplayName(),
                          wx.OK | wx.ICON_WARNING)              
        
    def on_cancel(self, event):
        self.Destroy()
