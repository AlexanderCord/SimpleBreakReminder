#!/usr/bin/env python3
"""
Simple Break Reminder

Author: Ershov Alexander 
Created: 09/11/2019

"""
import wx
import wx.adv
import time
import os
import configparser


TRAY_TOOLTIP = 'Simple Break Reminder'
TRAY_ICON = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'break_reminder_icon.png'
BREAK_IS_ON = False
CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'break_reminder.ini'

# create 
def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class BreakDialog(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(BreakDialog, self).__init__(*args, **kwargs)
        self.message = None
        self.InitUI()

    def setMessage(self, msg):
        self.message = msg
    def InitUI(self):

        # wx.CallLater(1000, self.ShowMessage)

        self.SetSize((300, 200))
        self.SetTitle('Time to make a break')
        
        panel = wx.Panel(self)
        
        btn1 = wx.Button(panel, label='I am done')
        btn1.Bind(wx.EVT_BUTTON, self.BreakIsOff)


        self.Centre()
        self.ToggleWindowStyle(wx.STAY_ON_TOP)

    def BreakIsOff(self, event):
        global BREAK_IS_ON
        BREAK_IS_ON = False
        self.Close()

    def ShowMessage(self):
        wx.MessageBox('Time to make a break, my friend!' + self.message, 'Info',
            wx.OK | wx.ICON_INFORMATION)

#from pprint import pprint

class TaskBarIcon2(wx.adv.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon2, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        
        
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        # pprint(config)
        timeout = int(config['settings']['timeout'])
        print(str(timeout))
        
        self.timer.Start(timeout * 1000)
        

    def update(self, event):
        global BREAK_IS_ON
        
        print("\nupdated: ")
        print(time.ctime())        
        if BREAK_IS_ON == True:
            return
            
        BREAK_IS_ON = True    
        ex = BreakDialog(None) #, style=wx.SIMPLE_BORDER | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)

        ex.setMessage( time.ctime() )
        ex.Show()    


    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'About', self.on_hello)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print('Tray icon was left-clicked.')

    def on_hello(self, event):
        print('Simple Break Reminder v1.0')

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)


def main():
    app = wx.App()
    
    
    TaskBarIcon2()
    
    app.MainLoop()
    
    

if __name__ == '__main__':
    main()
