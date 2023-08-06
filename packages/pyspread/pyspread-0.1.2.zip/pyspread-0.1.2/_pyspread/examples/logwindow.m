import wx 

class LogWindow(wx.Frame):
	def __init__(self, parent, ID, title):

		wx.Frame.__init__ (self, None, ID, title)

		sizer = wx.BoxSizer(wx.VERTICAL)

		self.textbox = wx.TextCtrl(self, -1, "", size=(-1, -1), style=wx.TE_MULTILINE)
		sizer.Add(self.textbox, 1, wx.GROW)

		self.SetSizer(sizer)
		sizer.Fit(self)

logwin = LogWindow(None, -1, "LogWindow")
logwin.Show()

def log(msg):
	logwin.textbox.SetValue(logwin.textbox.GetValue() + msg)