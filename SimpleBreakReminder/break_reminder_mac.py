
#!/usr/bin/env python3
"""
Simple Break Reminder

Author: Ershov Alexander 
Created: 09/19/2019

"""
import wx
import wx.adv
import time
import os
import configparser


TRAY_TOOLTIP = 'Simple Break Reminder'
TRAY_ICON = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'break_reminder_icon.png'
CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'break_reminder.ini'



class SimpleBreakReminder(wx.adv.TaskBarIcon):
    TBMENU_RESTORE = wx.NewIdRef()
    TBMENU_CLOSE   = wx.NewIdRef()
    TBMENU_CHANGE  = wx.NewIdRef()
    TBMENU_REMOVE  = wx.NewIdRef()

    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame

        # Set the image
        icon = wx.Icon(wx.Bitmap(TRAY_ICON))
        self.SetIcon(icon, TRAY_TOOLTIP)
        
        self.SetIcon(icon, "Simple Break Reminder")
        self.imgidx = 1

        # bind some events
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate)
        self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=self.TBMENU_RESTORE)
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.MakeBreak, self.timer)
        self.StartTimer()

    def StartTimer(self):
        global CONFIG_FILE
        
        print("Trying to reset the time")
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        self.timeout = int(config['settings']['timeout'])
        print(str(self.timeout))
        
        self.timer.Start(1000*60*self.timeout)
        

        

    def MakeBreak(self, event):
        
        print("\nupdated: ")
        print(time.ctime())
        self.OnTaskBarActivate(event)




    def CreatePopupMenu(self):
        """
        This method is called by the base class when it needs to popup
        the menu for the default EVT_RIGHT_DOWN event.  Just create
        the menu how you want it and return it from this function,
        the base class takes care of the rest.
        """
        menu = wx.Menu()
        menu.Append(self.TBMENU_RESTORE, "Make a Break")
        menu.Append(self.TBMENU_CLOSE,   "Exit")
        return menu


    def MakeIcon(self, img):
        """
        The various platforms have different requirements for the
        icon size...
        """
        if "wxMSW" in wx.PlatformInfo:
            img = img.Scale(16, 16)
        elif "wxGTK" in wx.PlatformInfo:
            img = img.Scale(22, 22)
        # wxMac can be any size upto 128x128, so leave the source img alone....


        icon = wx.Icon(wx.Bitmap(img.ConvertToBitmap()) )
        return icon


    def OnTaskBarActivate(self, evt):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        
        self.frame.Raise()
        self.frame.SetParentWin(self)



    def OnTaskBarClose(self, evt):
        wx.CallAfter(self.frame.Close)



class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="SimpleBreakReminder")
        print("Showing main frame")
        self.tbicon = SimpleBreakReminder(self)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.InitUI()

    def SetParentWin(self, parentWin):
        self.parentWin = parentWin

    def OnCloseWindow(self, evt):
        self.tbicon.Destroy()
        evt.Skip()

    def InitUI(self):

        self.SetSize((300, 200))
        self.SetTitle('Time to make a break')
        
        panel = wx.Panel(self)        

        hbox = wx.BoxSizer()
        sizer = wx.GridSizer(2, 2, 2, 2)

        btn1 = wx.Button(panel, label='I am done')
        btn2 = wx.Button(panel, label='Reset time')

        sizer.AddMany([btn1, btn2])

        btn1.Bind(wx.EVT_BUTTON, self.BreakIsOff)
        btn2.Bind(wx.EVT_BUTTON, self.ResetTimer)

        hbox.Add(sizer, 0, wx.ALL, 15)
        panel.SetSizer(hbox)


        self.SetSize((300, 200))


        self.Centre()
        self.ToggleWindowStyle(wx.STAY_ON_TOP)
        
    def ResetTimer(self, event):
        self.parentWin.StartTimer()
        return



    def BreakIsOff(self, event):
        self.Hide()



app = wx.App(redirect=False)
frame = MainFrame(None)
#frame.Show(True)
app.MainLoop()

