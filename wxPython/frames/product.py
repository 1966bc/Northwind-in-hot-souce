# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Northwind in hot souce
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
# -----------------------------------------------------------------------------
import wx
from wx.lib import masked
from validator import Validator


class UI(wx.Dialog):
    def __init__(self, parent, index=None):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, name = "product")

        self.parent = parent
        self.index = index
        self.Bind(wx.EVT_CLOSE, self.on_cancel)
        self.init_ui()

    def init_ui(self):

        self.panel = wx.Panel(self)

        st_product = wx.StaticText(self.panel, wx.ID_ANY, "Product:")
        self.txProduct = wx.TextCtrl(self.panel,
                                     wx.ID_ANY,
                                     size=(wx.GetApp().engine.get_font() * 15, -1))
        self.txProduct.SetForegroundColour((0, 0, 255))

        st_supplier = wx.StaticText(self.panel, wx.ID_ANY, "Suppliers:")
        self.cbSuppliers = wx.ComboBox(self.panel,
                                       wx.ID_ANY,
                                       style=wx.CB_READONLY,
                                       size=(wx.GetApp().engine.get_font() * 15, -1))

        st_categories = wx.StaticText(self.panel, wx.ID_ANY, "Categories:")
        self.cbCategories = wx.ComboBox(self.panel,
                                        wx.ID_ANY,
                                        style=wx.CB_READONLY,
                                        size=(wx.GetApp().engine.get_font() * 15, -1))

        st_package = wx.StaticText(self.panel, wx.ID_ANY, "Package:")
        self.txPackage = wx.TextCtrl(self.panel,
                                     wx.ID_ANY,
                                     size=(wx.GetApp().engine.get_font() * 15, -1))
        self.txPackage.SetForegroundColour((255, 0, 0))

        st_price = wx.StaticText(self.panel, wx.ID_ANY, "Price:")
        self.txPrice = masked.NumCtrl(self.panel,
                                      wx.ID_ANY,
                                      integerWidth=4,
                                      fractionWidth=2)
         
        st_stock = wx.StaticText(self.panel, wx.ID_ANY, "Stock:")
        self.txStock = wx.TextCtrl(self.panel,
                                   wx.ID_ANY,
                                   validator=Validator(2),
                                   style=wx.TE_CENTRE)

        st_enable = wx.StaticText(self.panel, wx.ID_ANY, "Enable:")
        self.ckEnable = wx.CheckBox(self.panel,wx.ID_ANY)

        if self.index is not None:
            bts = [(wx.ID_ANY, "&Save", self.on_save),
                   (wx.ID_ANY, "&Delete", self.on_delete),
                   (wx.ID_ANY, "&Cancel", self.on_cancel)]
        else:
            bts = [(wx.ID_ANY, "&Save", self.on_save),
                   (wx.ID_ANY, "&Cancel", self.on_cancel)]
            
            
        for (id, label, event) in bts:
            b = wx.Button(self.panel, id, label,)
            b.Bind(wx.EVT_BUTTON, event)

        #manage layout
        s0 = wx.BoxSizer(wx.HORIZONTAL)
        s1 = wx.FlexGridSizer(cols=2, hgap=5, vgap=8)
        s2 = wx.BoxSizer(wx.VERTICAL)
        
        items = (st_product,self.txProduct,
                 st_supplier,self.cbSuppliers,
                 st_categories,self.cbCategories,
                 st_package,self.txPackage,
                 st_price, self.txPrice,
                 st_stock, self.txStock,
                 st_enable,self.ckEnable)
        
        for i in items:
            s1.Add(i,0,wx.ALL, 1)

        for i in self.panel.GetChildren():
            if type(i) == wx.Button:
                s2.Add(i,0,wx.EXPAND|wx.ALL, 5)

        w = (s1,s2)
        for i in w:
            s0.Add(i, 0, wx.ALL, 10)

        self.panel.SetSizer(s0)
        s0.Fit(self)
        s0.SetSizeHints(self)

    def on_open(self):

        self.set_categories()
        self.set_suppliers()

        if self.index is not None:
            msg = "Update Product"
            self.set_values()
        else:
            msg = "Insert Product"
            self.ckEnable.SetValue(True)

        self.SetTitle(msg)
        self.txProduct.SetFocus()

    def set_values(self,):

        self.txProduct.SetValue(self.parent.selected_item[1])
        #set value on cbSuppliers
        key = next(key
                   for key, value
                   in self.dict_suppliers.items()
                   if value == self.parent.selected_item[2])
        self.cbSuppliers.SetSelection(key)
        
        #set value on cbCategories
        key = next(key
                   for key, value
                   in self.dict_categories.items()
                   if value == self.parent.selected_item[3])
        self.cbCategories.SetSelection(key)
        
        self.txPackage.SetValue(self.parent.selected_item[4])
        self.txPrice.SetValue(str(self.parent.selected_item[5]))
        self.txStock.SetValue(str(self.parent.selected_item[6]))
        self.ckEnable.SetValue(self.parent.selected_item[7])

    def get_values(self):

        return [self.txProduct.GetValue(),
                self.dict_suppliers[self.cbSuppliers.GetSelection()],
                self.dict_categories[self.cbCategories.GetSelection()],
                self.txPackage.GetValue(),
                self.txPrice.GetValue(),
                self.txStock.GetValue(),
                self.ckEnable.GetValue(),]        

    def on_save(self, evt):

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

            product_id = wx.GetApp().engine.write(sql, args)
            
            self.parent.on_reset()
            
            self.on_cancel()

        else:
            wx.MessageBox(wx.GetApp().engine.abort,
                          wx.GetApp().GetAppDisplayName(),
                          wx.OK | wx.ICON_INFORMATION)                  

    def on_delete(self, evt=None):

        sql = "DELETE FROM products WHERE product_id=?;"

        if wx.MessageDialog(self,
                             wx.GetApp().engine.ask_to_delete,
                             wx.GetApp().GetAppDisplayName(),
                             wx.YES_NO|wx.ICON_QUESTION).ShowModal() == wx.ID_YES:

            args = (self.parent.selected_item[0],)
            wx.GetApp().engine.write(sql, args)
            self.parent.get_selected_combo_item()
            self.on_cancel()
        else:
            wx.MessageBox(wx.GetApp().engine.abort,
                          wx.GetApp().GetAppDisplayName(),
                          wx.OK | wx.ICON_INFORMATION)           

    def set_categories(self):

        index = 0
        self.dict_categories = {}
        values = []
        
        sql = "SELECT category_id, category FROM categories ORDER BY category ASC;"
        rs = wx.GetApp().engine.read(True, sql, ())

        for i in rs:
            self.dict_categories[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbCategories.SetItems(values)            
                
    def set_suppliers(self,):

        index = 0
        self.dict_suppliers = {}
        values = []

        sql = "SELECT supplier_id, company FROM suppliers ORDER BY company ASC;"
        rs = wx.GetApp().engine.read(True, sql, ())

        for i in rs:
            self.dict_suppliers[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbSuppliers.SetItems(values)

    def on_cancel(self, evt=None):
        self.Destroy()
                
