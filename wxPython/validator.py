import wx
import string

class Validator(wx.PyValidator):

    """Get it from wxPython in Action the old testament;)"""
    def __init__(self, flag=None, pyVar=None):
        wx.Validator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.alpha_only = 1
        self.digit_only = 2

    def Clone(self):
        return Validator(self.flag)

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        #print tc,val
        if self.flag == self.alpha_only:
            for x in val:
                if x not in string.letters:
                    return False

        elif self.flag == self.digit_only:
            for x in val:
                if x not in string.digits:
                    return False

        return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        #print key
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255 or key == 32:
            event.Skip()
            return

        if self.flag == self.alpha_only and chr(key) in string.letters:
            event.Skip()
            return

        if self.flag == self.digit_only and chr(key) in string.digits:
            event.Skip()
            return

        #if not wx.Validator_IsSilent():
        #    wx.Bell()

        return
