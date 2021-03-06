
#!/usr/bin/env python3
"""
Simple Break Reminder

Author: Ershov Alexander 
Created: 09/19/2019

"""
import wx
import darkMode
import wx.adv
import time
import os
import configparser
import datetime


TRAY_TOOLTIP = 'Simple Break Reminder'
TRAY_ICON = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'break_reminder_icon.png'
CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'break_reminder.ini'

LOGS_DIR = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'logs' + os.sep

BREAK_STARTED = 1
BREAK_ENDED = 0
BREAK_POSTPONED = 2

DEBUG_OUTPUT=False

# @todo: refactor. Class structure redisgn with SOLID principles
class SimpleBreakReminder(wx.adv.TaskBarIcon):
    TBMENU_RESTORE = wx.NewIdRef()
    TBMENU_CLOSE   = wx.NewIdRef()
    TBMENU_CHANGE  = wx.NewIdRef()
    TBMENU_REMOVE  = wx.NewIdRef()

    def GetIcon(self):
        icon = wx.Icon(wx.Bitmap(TRAY_ICON))
        return icon
        
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame

        # Set the image

        icon = self.GetIcon()
        self.SetIcon(icon, "Simple Break Reminder")
        self.imgidx = 1

        # bind some events
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate)
        self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=self.TBMENU_RESTORE)
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.MakeBreak, self.timer)
        self.StartTimer()

        

    def StartTimer(self, timeout = None):
        DEBUG_OUTPUT and print("Trying to reset the time")
        if timeout is None:
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            self.timeout = int(config['settings']['timeout'])
        else:
            self.timeout = timeout
        DEBUG_OUTPUT and print(str(self.timeout))
        
        self.timeStarted = time.time()
        self.timer.Start(1000*60*self.timeout)

        self.showTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.ShowTime, self.showTimer)
        self.showTimer.Start(1000)

    def StopTimer(self):
        DEBUG_OUTPUT and print("Timers are stopped")
        self.timer.Stop()
        self.showTimer.Stop()
        
    def ShowTime(self, event):
        DEBUG_OUTPUT and print("Current time")
        DEBUG_OUTPUT and print(time.ctime())

        DEBUG_OUTPUT and print("Minutes left before break")
        timeLeft = str( int( ( self.timeout*60 +  int(self.timeStarted) - time.time())/60 ) )
        DEBUG_OUTPUT and print(timeLeft)
        icon = self.GetIcon()
        self.SetIcon(icon, "Simple Break Reminder [" + timeLeft + " min before break]")

        
    def IsLoggingOn(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        logging = int(config['settings']['logs'])
        if logging == 1:
            DEBUG_OUTPUT and print("Logging is on")
            return True
        else:
            DEBUG_OUTPUT and print("Logging is off")
            return False
        
            
        

    def MakeBreak(self, event):
        
        DEBUG_OUTPUT and print("\nupdated: ")
        DEBUG_OUTPUT and print(time.ctime())
        
        
        
        self.OnTaskBarActivate(event)




    def CreatePopupMenu(self):
        """
        This method is called by the base class when it needs to popup
        the menu for the default EVT_RIGHT_DOWN event.  Just create
        the menu how you want it and return it from this function,
        the base class takes care of the rest.
        """
        menu = wx.Menu()
        menu.Append(self.TBMENU_RESTORE, "Take a Break")
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


    def LogBreak(self, breakStarted = BREAK_STARTED, breakLength = -1):
    
        if self.IsLoggingOn() == False:
            return 
            
        now = datetime.datetime.now()
        DEBUG_OUTPUT and print("Current date and time : ")
        
        currentMoment = now.strftime("%Y-%m-%d %H:%M:%S")
        DEBUG_OUTPUT and print(currentMoment)
        fileName = LOGS_DIR + now.strftime("%Y-%m-%d") + '.log'
        
        if os.path.exists(fileName):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
            
            
        log = open(fileName,append_write)
        # datetime;1}0 - 1 if break started, 0 if break ended
        log.write(currentMoment + ";" + str(breakStarted) + ";" + str(breakLength) +  "\n")
        log.close()    

    def OnTaskBarActivate(self, evt):
        DEBUG_OUTPUT and print("Taking a break");
        self.StopTimer()
        self.LogBreak( BREAK_STARTED )
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        
        self.frame.Raise()
        self.frame.SetParentWin(self)
        self.frame.StartTimeoutTimer()


    def OnTaskBarClose(self, evt):
        wx.CallAfter(self.frame.Close)



class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="SimpleBreakReminder")
        DEBUG_OUTPUT and print("Showing main frame")
        self.tbicon = SimpleBreakReminder(self)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.InitUI()

    def SetParentWin(self, parentWin):
        self.parentWin = parentWin

    def OnCloseWindow(self, evt):
        self.tbicon.Destroy()
        evt.Skip()

    def StartTimeoutTimer(self):
        self.timeoutTimer = wx.Timer(self)
        self.timeoutStarted = time.time()
        self.Bind(wx.EVT_TIMER, self.UpdateTimeoutLabel, self.timeoutTimer)
        self.timeoutTimer.Start(1000)
                

    def UpdateTimeoutLabel(self, event):
        DEBUG_OUTPUT and print("Current time")
        DEBUG_OUTPUT and print(time.ctime())

        timePassed =  int( ( time.time() - int(self.timeoutStarted) ) ) 
        self.timePassed = timePassed
        
        self.displayTimeoutLabel.SetLabel("Minutes passed since the break began: %d" % int(timePassed/60))
        DEBUG_OUTPUT and print("Minutes after break started: %d" % int(timePassed/60))

        
    def StopTimeoutTimer(self):
        self.timeoutTimer.Stop()
    

    def InitUI(self):

        self.SetSize((400, 200))
        self.SetTitle('Time to take a break')
        
        panel = wx.Panel(self)        
        self.defaultColor = self.GetBackgroundColour()
        
        hbox = wx.BoxSizer()
        sizer = wx.GridSizer(2, 3, 10, 10)

        btn1 = wx.Button(panel, label='End the break')
        btn2 = wx.Button(panel, label='Remind in 5 min')
        btn3 = wx.Button(panel, label='Exit')
        
        # Showing how much time has passed since the break has begun
        self.displayTimeoutLabel = wx.StaticText(panel, -1, "Timeout has just started", style=wx.ALIGN_CENTRE)

        sizer.AddMany([btn1, btn2, btn3, self.displayTimeoutLabel])

        btn1.Bind(wx.EVT_BUTTON, self.BreakIsOff)
        btn2.Bind(wx.EVT_BUTTON, self.RemindLater)
        btn3.Bind(wx.EVT_BUTTON, self.QuitApp)

        
        hbox.Add(sizer, 0, wx.ALL, 15)
        panel.SetSizer(hbox)


        self.SetSize((400, 200))
        

        self.Centre()
        self.ToggleWindowStyle(wx.STAY_ON_TOP)
        self.onToggleDark(self)
        
    def onToggleDark(self, event):
        darkMode.darkMode(self, self.defaultColor)
        
    def QuitApp(self, event):
        exit()

    def RemindLater(self, event):
        self.StopTimeoutTimer()
        self.parentWin.LogBreak(BREAK_POSTPONED, self.timePassed)
        self.parentWin.StartTimer(5)

        self.Hide()


    def BreakIsOff(self, event):
        self.StopTimeoutTimer()
        self.parentWin.LogBreak(BREAK_ENDED, self.timePassed)
        self.parentWin.StartTimer()

        self.Hide()



app = wx.App(redirect=False)
frame = MainFrame(None)
#frame.Show(True)
app.MainLoop()

