import wx
from wx.stc import *


class WedNESday(wx.Frame):

  def __init__(self,parent,id):
    WINDOW_SIZE = (wx.DisplaySize()[0],wx.DisplaySize()[1]-40)
    wx.Frame.__init__(self,parent,id,"wedNESday",size=(WINDOW_SIZE),pos=(30,100))
    p = wx.Panel(self)
    self.Centre()


    self.textctrl = StyledTextCtrl(p,-1,
        pos=(0,0),
        size=(wx.DisplaySize()[0]-20,wx.DisplaySize()[1]-100),
        style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)

    # style=wx.NO_FULL_REPAINT_ON_RESIZE)
    self.textctrl.StyleSetFont(STC_STYLE_DEFAULT, wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))


    index = self.textctrl.GetFirstVisibleLine()

    self.textctrl.SetLexer(STC_LEX_ASM)
    # self.textctrl.SetLexer(STC_LEX_PYTHON)
    text = 'a =1 \n if a:'
    # self.textctrl.SetLexerLanguage("cpp")
    self.textctrl.SetText(text)

    self.textctrl.SetProperty("fold", "1")

    self.textctrl.SetMarginType(1, STC_MARGIN_NUMBER)

    # TODO: self.textctrl.SetMarginType(2, STC_MARGIN_TEXT)


    # self.textctrl.SetMarginType(2, STC_MARGIN_SYMBOL)
    # self.textctrl.SetMarginMask(2, STC_MASK_FOLDERS)
    # self.textctrl.SetMarginSensitive(2, True)
    self.textctrl.SetMarginWidth(2, 70)

    # TODO: self.textctrl.MarginSetText(1, '4A 40')

    self.textctrl.SetMargins(0,10)
    self.textctrl.Colourise(0, len(text))

    self.textctrl.StyleSetSpec(STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")
    self.textctrl.SetCaretForeground("BLUE")
    self.textctrl.SetSelBackground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT))
    self.textctrl.SetSelForeground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))



if __name__=='__main__':
  app = wx.App()
  wednesday = WedNESday(None,-1)
  wednesday.Show()
  app.MainLoop()
