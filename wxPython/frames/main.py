# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Northwind in hot souce
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
# -----------------------------------------------------------------------------
""" This is the main module of Northwind in hot souce."""
import sys
import wx
import wx.adv
import time

import frames.product
import frames.categories
import frames.suppliers

from engine import Engine

__author__ = "1966bc"
__copyright__ = "Copyleft"
__credits__ = "hal9000"
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "1.816"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "hiems MMXXI"
__status__ = "production"
__description__ = """Northwind in hot sauce is an application developed to show the differences in programming and rendering, for example in layout, between wxPython and Tkinter platforms.
                     It is based on Microsoft's famous Northwind database, hence the name of the project."""


class Main(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        self.SetTitle(wx.GetApp().GetAppDisplayName())
        icon = wx.GetApp().engine.get_file("northwind.ico")
        self.SetIcon(wx.Icon(icon,wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, wx.GetApp().on_exit)
        
        self.parent = parent
        self.table = "products"
        self.primary_key = "product_id"

        self.init_menu()
        self.init_toolbar()
        self.init_status_bar()
        self.init_ui()

    def init_menu(self):

        m_main = wx.MenuBar()

        m_file = wx.Menu()
        m_tools = wx.Menu()
        m_about = wx.Menu()
        s_databases = wx.Menu()
        
        m_main.Append(m_file, '&File')
        m_main.Append(m_tools, '&Tools')
        m_main.Append(m_about, "?")

        s_databases = wx.Menu()
        item = s_databases.Append(wx.ID_ANY, "D&ump")
        self.Bind(wx.EVT_MENU, self.on_dump, item)
        vacuum = s_databases.Append(wx.ID_ANY, "&Vacuum")
        self.Bind(wx.EVT_MENU, self.on_vacuum, vacuum)
        
        m_file.Append(wx.ID_ANY, "&Database", s_databases)

        item = m_file.Append(wx.ID_ANY, "&Log")
        self.Bind(wx.EVT_MENU, self.on_log, item)

        m_file.AppendSeparator()
        
        item = m_file.Append(wx.ID_ANY, "E&xit")
        self.Bind(wx.EVT_MENU, wx.GetApp().on_exit, item)

        items = ((wx.ID_ABOUT, "About", self.on_about),
                 (wx.ID_ANY, "Python", self.on_python_version),
                 (wx.ID_ANY, "wxPython", self.on_wxpython_version),)

        for i in items:
            item = m_about.Append(i[0], i[1])
            self.Bind(wx.EVT_MENU, i[2], item)
            
        item = m_tools.Append(wx.ID_ANY, "&Categories")
        self.Bind(wx.EVT_MENU, self.on_categories, item)

        item = m_tools.Append(wx.ID_ANY, "&Suppliers")
        self.Bind(wx.EVT_MENU, self.on_suppliers, item)
        
        self.SetMenuBar(m_main)

    def init_toolbar(self):

        img_exit = wx.GetApp().engine.get_image(wx.GetApp().engine.get_icon("exit"))
        img_info = wx.GetApp().engine.get_image(wx.GetApp().engine.get_icon("info"))
        toolbar = self.CreateToolBar()
        exitButton = toolbar.AddTool(wx.ID_ANY, "", wx.Bitmap(img_exit))
        infoButton = toolbar.AddTool(wx.ID_ANY, "", wx.Bitmap(img_info))

        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, wx.GetApp().on_exit, exitButton)
        self.Bind(wx.EVT_TOOL, self.on_about, infoButton)

    def init_status_bar(self):

        self.status = self.CreateStatusBar(1,wx.STB_SIZEGRIP)

        self.on_clock(None)
        self.timer = wx.Timer(self)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.on_clock)
        
    def init_ui(self):
        
        self.panel = wx.Panel(self)
        
        self.stProducts = wx.StaticText(self.panel, wx.ID_ANY, "Products")
        self.lstProducts = wx.ListCtrl(self.panel,
                                       wx.ID_ANY,
                                       style = wx.LC_REPORT|wx.LC_HRULES,)
        
        self.lstProducts.InsertColumn(0, 'id', width = 0)
        self.lstProducts.InsertColumn(1, 'Product', wx.LIST_FORMAT_LEFT,
                                      width = 150)
        self.lstProducts.InsertColumn(2, "Description", wx.LIST_FORMAT_LEFT,
                                      width = 150)
        self.lstProducts.InsertColumn(3, "Stock", wx.LIST_FORMAT_CENTER,
                                      width = 100)
        self.lstProducts.InsertColumn(4, "Price", wx.LIST_FORMAT_CENTER,
                                      width = 100)

        self.lstProducts.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_prduct_selected)
        self.lstProducts.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_prduct_activated)

        self.sb_categories = wx.StaticBox(self.panel, wx.ID_ANY, "Categories")
        self.sb_categories.SetMinSize(wx.Size(-1, 40))
        
        self.cbCombo = wx.ComboBox(self.sb_categories,
                                        wx.ID_ANY,
                                        size=(wx.GetApp().engine.get_font() * 45,-1),
                                        style = wx.CB_READONLY|wx.CB_DROPDOWN)
        self.cbCombo.Bind(wx.EVT_COMBOBOX, self.get_selected_combo_item)
        
        bts = [(wx.ID_ANY,'&Reset', self.on_reset),
               (wx.ID_ANY,'&New', self.on_add),
               (wx.ID_ANY,'&Edit', self.on_prduct_activated),
               (wx.ID_ANY,'&Close', wx.GetApp().on_exit)]

        for (id, label, comand) in bts:
             b = wx.Button(self.panel, id, label,)
             b.Bind(wx.EVT_BUTTON, comand)

        voices = ["Categories", "Suppliers"]

        self.rbOptions = wx.RadioBox(self.panel,wx.ID_ANY,"Combo data",
                                     wx.DefaultPosition,
                                     wx.DefaultSize,
                                     voices,
                                     1,
                                     wx.RA_SPECIFY_COLS)

        self.rbOptions.Bind(wx.EVT_RADIOBOX, self.set_combo_values)             

        box_main = wx.BoxSizer(wx.HORIZONTAL)
        box_left = wx.BoxSizer(wx.VERTICAL)
        box_right = wx.BoxSizer(wx.VERTICAL)

        items = ((self.stProducts, 0, 5),
                 (self.lstProducts, 4, 5),
                 (self.sb_categories, 1, 5))
        for item in items:
            box_left.Add(item[0], item[1], wx.EXPAND|wx.ALL, border = item[2])

        for i in self.panel.GetChildren():
            if type(i) in(wx.Button,wx.RadioBox):
                box_right.Add(i,proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        box_main.Add(box_left, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        box_main.Add(box_right, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        
        self.panel.SetSizer(box_main)
        box_main.SetSizeHints(self)
        self.Layout()

    def on_open(self,):
        self.on_reset()

    def on_reset(self, evt=None):

        sql = "SELECT * FROM {0} ORDER BY product ASC;".format(self.table)
        self.set_values(sql,())
        self.set_combo_values()

    def set_values(self, sql, args):

        self.lstProducts.DeleteAllItems()

        rs = wx.GetApp().engine.read(True, sql, args)

        if rs:

            for i in rs:
                
                index = self.lstProducts.InsertItem(self.lstProducts.GetItemCount(), i[0])
                self.lstProducts.SetItem(index, 0, str(i[0]))
                self.lstProducts.SetItem(index, 1, str(i[1]))
                self.lstProducts.SetItem(index, 2, str(i[4]))
                self.lstProducts.SetItem(index, 3, str(i[6]))
                self.lstProducts.SetItem(index, 4, str(i[5]))
                
                if int(i[7]) == 0:
                    self.lstProducts.SetItemBackgroundColour(index, (211, 211, 211))
                elif int(i[6])<1:
                     self.lstProducts.SetItemBackgroundColour(index, (255, 160, 122))

        s = "{0} {1}".format("Products", self.lstProducts.GetItemCount())

        self.stProducts.SetLabel(s)

    def set_combo_values(self, event=None):

        self.cbCombo.SetValue("")
        self.cbCombo.Clear()

        if self.rbOptions.GetSelection() != 1:
            sql = "SELECT category_id, category\
                   FROM categories\
                   WHERE enable =1\
                   ORDER BY category;"
            text = "Categories"
        else:
            sql = "SELECT supplier_id, company\
                   FROM suppliers\
                   WHERE enable =1\
                   ORDER BY company;"
            text = "Suppliers"

        self.sb_categories.SetLabel(text)
        
        rs = wx.GetApp().engine.read(True, sql, ())

        for i in rs:
                pk_id = i[0]
                showed = str(i[1])
                self.cbCombo.Append(showed, (pk_id, showed))

    def get_selected_combo_item(self, evt=None):

        idx = self.cbCombo.GetSelection()
        if idx != -1:

            self.cb_categories = idx

            selected_id = self.cbCombo.GetClientData(idx)[0]

            if self.rbOptions.GetSelection() != 1:
                field = "category_id"
                
            else:
                field = "supplier_id"
                
            sql = "SELECT * FROM products WHERE  {0}=? ORDER BY product;".format(field)
            args = (selected_id,)

            self.set_values(sql, args)
        else:
            self.on_open()
        
    def on_add(self, evt=None):

        obj = frames.product.UI(self)
        obj.on_open()
        obj.Center()
        obj.ShowModal()
    
    def on_prduct_selected(self, evt):
        
        if evt.Index != -1:
            pk = self.lstProducts.GetItem(evt.Index, 0).GetText()
            self.selected_item = wx.GetApp().engine.get_selected(self.table,
                                                                 self.primary_key,
                                                                 pk)
            
    def on_prduct_activated(self, evt=None):

        index = self.lstProducts.GetFirstSelected()
        if index != -1:
            obj = frames.product.UI(self, index)
            obj.on_open()
            obj.Center()
            obj.ShowModal()

    def on_categories(self, event=None):
        obj = frames.categories.UI(self)
        obj.on_open()
        obj.Center()
        obj.Show()

    def on_suppliers(self, event=None):
        obj = frames.suppliers.UI(self)
        obj.on_open()
        obj.Center()
        obj.Show()

    def on_python_version(self, event=None):
        s = wx.GetApp().engine.get_python_version()
        wx.MessageBox(s,
                      wx.GetApp().GetAppDisplayName(),
                      wx.OK|wx.ICON_INFORMATION)
        

    def on_wxpython_version(self, event=None):
        s = "wxPython version\n{0}".format(wx.version())
        wx.MessageBox(s,
                      wx.GetApp().GetAppDisplayName(),
                      wx.OK|wx.ICON_INFORMATION)
        
    def on_about(self,event):

        description = """Northwind in hot sauce is an application developed to show the differences
                         in programming and rendering, for example in layout, between wxPython and Tkinter platforms.
                         It is based on Microsoft's famous Northwind database, hence the name of the project."""

        info = wx.adv.AboutDialogInfo()
        
        icon = wx.GetApp().engine.get_file("northwind.ico")
        info.SetIcon(wx.Icon(icon, wx.BITMAP_TYPE_PNG))
        info.SetName(wx.GetApp().GetAppDisplayName())
        info.SetDescription(description)
        info.SetVersion("Version: {0}".format(__version__))
        info.SetCopyright(__copyright__)
        info.SetLicence(wx.GetApp().engine.get_license())
        info.AddDeveloper(__author__)
        info.SetDevelopers([__author__, __credits__])
        
        wx.adv.AboutBox(info)
        
    def on_info(self, event=None):
        pass

    def on_clock(self, evt):
        
        t = time.localtime(time.time())
        sbTime = time.strftime("Atral date: %d-%m-%Y %H:%M:%S", t)
        self.status.SetStatusText(sbTime,0)

    def on_dump(self, event=None):
        self.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        wx.GetApp().engine.dump()
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        wx.MessageBox("Dump executed.",
                      wx.GetApp().GetAppDisplayName(),
                      wx.OK|wx.ICON_INFORMATION)
        

    def on_vacuum(self, event=None):
        sql = "VACUUM;"
        self.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        wx.GetApp().engine.write(sql)
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        wx.MessageBox("Vacuum executed.",
                      wx.GetApp().GetAppDisplayName(),
                      wx.OK|wx.ICON_INFORMATION)
        
    def on_log(self,evt=None):
        wx.GetApp().engine.get_log_file()

        
class App(wx.App):
    """Application start here"""
    def OnInit(self):

        wx.GetApp().engine = Engine()
        
        self.SetAppDisplayName("Northwind in hot sauce")        
        
        w = Main(None)
        wx.GetApp().SetTopWindow(w)
        w.on_open()
        w.Show()

        return True
    
    def on_exit(self, evt=None):
        
        if wx.MessageBox("Do you want to quit?",
                         self.GetAppDisplayName(),
                         wx.YES_NO |wx.ICON_QUESTION| wx.CENTRE |wx.NO_DEFAULT) == 2:

            wx.GetApp().engine.con.close()
            wx.Exit()
            #self.Close()#do nothing apparent on linux...
           #self.Destroy()#segmentation fault on linux
            

def main():
    app = App(redirect=True, filename = "log.txt")
    app.MainLoop()

if __name__ == "__main__":
    main()
