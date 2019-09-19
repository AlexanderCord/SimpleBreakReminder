# utils

## SimpleBreakReminder 

Simple app that runs in your tray icon, reminding you to make a break.

It also shows, how much time you have before the break, in the tooltip for tray icon.
<img src="https://raw.githubusercontent.com/AlexanderCord/SimpleBreakReminder/master/screenshot3.png" width="400">




Config is simple ini file, timeout should be set in minutes

When time comes, it shows small always-on-top window with a message to make a pause from you work.

<img src="https://raw.githubusercontent.com/AlexanderCord/SimpleBreakReminder/master/screenshot1.png" width="600">


Works on Python 3.7.4
and wxPython 4.0.6 (phoenix)

Tested on
- MacOs (MBP)
- Windows 10 (laptop)

Windows 10 installation
- Download Python 3.7.4 https://www.python.org/downloads/
- In cmd / terminal run

```
pip3 install wxPython
```

- Check wxPython version

```
python3
```

then
```
import wc
```

then
```
wx.version()
```

should be at least 4.0.6 

