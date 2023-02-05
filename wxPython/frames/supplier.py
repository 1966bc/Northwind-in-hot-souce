# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Northwind in hot souce
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
# -----------------------------------------------------------------------------
import wx


class UI(wx.Dialog):
    def __init__(self, parent, index=None):
        wx.Dialog.__init__(self,
                           parent,
                           wx.ID_ANY,
                           name="supplier")

        self.parent = parent
        self.index = index
        self.Bind(wx.EVT_CLOSE, self.on_cancel)
        icon = wx.GetApp().engine.get_file("northwind.ico")
        self.SetIcon(wx.Icon(icon,wx.BITMAP_TYPE_ICO))
        self.init_ui()

    def init_ui(self):

        self.panel = wx.Panel(self)
        
        st_category = wx.StaticText(self.panel, wx.ID_ANY, "Company:")
        self.txtCompany = wx.TextCtrl(self.panel, wx.ID_ANY, "",size=((wx.GetApp().engine.get_font() * 20, -1)))

        st_enable = wx.StaticText(self.panel, wx.ID_ANY, "Enable")
        self.ckEnable = wx.CheckBox(self.panel, wx.ID_ANY,)

        sb_buttons = wx.StaticBox(self.panel,wx.ID_ANY,"")

        bts = [(wx.ID_ANY, "&Save", self.on_save),
               (wx.ID_ANY, "&Cancel", self.on_cancel),]

        for btn in bts:
            b = wx.Button(self.panel, btn[0], btn[1],)
            b.Bind(wx.EVT_BUTTON, btn[2])

        #do layout
        box_main = wx.BoxSizer(wx.HORIZONTAL)
        box_left = wx.FlexGridSizer(cols = 2, hgap = 5, vgap = 5)
        box_right = wx.StaticBoxSizer(sb_buttons, wx.VERTICAL)

        items = (st_category, self.txtCompany,
                 st_enable, self.ckEnable,)
        for item in items:
            box_left.Add(item, 0, wx.EXPAND|wx.ALL, 1)

        for item in self.panel.GetChildren():
            if type(item) == wx.Button:
                box_right.Add(item, 0, wx.EXPAND|wx.ALL, 5)

        boxes = (box_left, box_right)
        for box in boxes:
            box_main.Add(box, 0, wx.ALL, 10)

        self.panel.SetSizer(box_main)
        box_main.Fit(self)
        box_main.SetSizeHints(self)

    def on_open(self):

        if self.index is not None:
            msg = "Edit Supplier"
            self.set_values()
        else:
            msg = "Add Supplier"
            self.ckEnable.SetValue(True)

        self.SetTitle (msg)
        self.txtCompany.SetFocus()

    def set_values(self,):

        self.txtCompany.SetValue(self.parent.selected_item[1])
        self.ckEnable.SetValue(self.parent.selected_item[2])        

    def get_values(self,):

           return [self.txtCompany.GetValue(),
                   self.ckEnable.GetValue(),]

    def on_save(self,event):

        if wx.GetApp().engine.on_fields_control(self.panel,
                                                wx.GetApp().GetAppDisplayName()) == 0:return

        if wx.MessageDialog(self,
                             wx.GetApp().engine.ask_to_save,
                             wx.GetApp().GetAppDisplayName(),
                             wx.YES_NO|wx.ICON_QUESTION).ShowModal() == wx.ID_YES:

            args = self.get_values()

            if self.index is not None:

                sql = wx.GetApp().engine.get_update_sql(self.parent.table, self.parent.primary_key)

                args.append(self.parent.selected_item[0])

            else:

                sql = wx.GetApp().engine.get_insert_sql(self.parent.table, len(args))

            last_id = wx.GetApp().engine.write(sql, args)
            self.parent.set_values()
            
            self.on_cancel()

        else:
            wx.MessageBox(wx.GetApp().engine.abort,
                          wx.GetApp().GetAppDisplayName(),
                          wx.OK | wx.ICON_INFORMATION)                    

    def on_cancel(self, event=None):
        self.Destroy()                                   
    
