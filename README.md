# utils

## SimpleBreakReminder 
### About
Simple app that runs in your tray icon, reminding you to make a break.

It also shows, how much time you have before the break, in the tooltip for tray icon.
<img src="https://raw.githubusercontent.com/AlexanderCord/SimpleBreakReminder/master/screenshot2.png" width="400">




Config is simple ini file, timeout should be set in minutes

When time comes, it shows small always-on-top window with a message to make a pause from you work.

<img src="https://raw.githubusercontent.com/AlexanderCord/SimpleBreakReminder/master/screenshot1.png" width="550">


Works on Python 3.7.4+
and wxPython 4.0.6 (phoenix)

Tested on
- MacOs Monterey 
- Windows 10 (laptop)

### Installation for MacOs
- in terminal run 

```
./install.sh
```

### Running
- Clone to a specific directory
- Set the variables in settings.ini - timeout (in minutes), and whether you want to log breaks or not. If you want to log taking breaks, create empty logs directory in the folder containing the app
- Run terminal
- Run 
```
./run.sh
```






