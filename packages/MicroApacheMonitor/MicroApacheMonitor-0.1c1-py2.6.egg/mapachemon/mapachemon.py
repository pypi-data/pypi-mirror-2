"""Control MicroApache from the Windows notification area.

This application is designed to be analogous to ApacheMonitor.exe that ships
with the standard Apache server.  ApacheMonitor runs in the Windows notification
area (commonly referred to as the System Tray), and allows you to start, stop,
and restart the Apache server via a context menu.  MicroApacheMonitor provides
the same functionality for Micro-Apache, and it's portable, just like Micro-
Apache.

"""

from subprocess import Popen, PIPE, STDOUT
import os.path
import re
import ConfigParser
import time
from optparse import OptionParser

from win32con import SW_HIDE, SW_SHOW
from win32console import GetConsoleWindow
from win32gui import ShowWindow
from pkg_resources import resource_filename

from SysTrayIcon import *

class MicroApache():
    def __init__(self, serverpath, logpath):
        self.mapache = serverpath
        self.p = None
        self.logpath = logpath
        self.logfile = None
    def start(self):
        if not findPidsByName(os.path.split(self.mapache)[1]):
            self.logfile = open(self.logpath,'a')
            Popen(self.mapache,
                  cwd=os.path.split(self.mapache)[0],
                  stdout=self.logfile,
                  stderr=STDOUT,
                  )
    def stop(self):
        pidList = findPidsByName(os.path.split(self.mapache)[1])
        if pidList:
            for pid in pidList:
                killProcess(pid)
            if self.logfile:
                self.logfile.close()
    def restart(self):
        self.stop()
        time.sleep(0.5)
        self.start()

def hideConsole():
    hWnd = GetConsoleWindow()
    if not hWnd:
        return
    ShowWindow(hWnd, SW_HIDE)

def showConsole():
    hWnd = GetConsoleWindow()
    if not hWnd:
        return
    ShowWindow(hWnd, SW_SHOW)

def findPidsByName(processName):
    p = Popen(('tasklist /FI "IMAGENAME eq ' +
               processName +
               '" /NH /FO CSV'), stdout=PIPE, stderr=PIPE)
    if p.stderr.read():
        return []
    pattern = re.compile('^"([^"]*)","([^"]*)')
    nameList = []
    pidList = []
    for line in p.stdout:
        m = pattern.match(line)
        if m:
            nameList.append(m.groups()[0])
            pidList.append(int(m.groups()[1]))
    return [pid for name, pid in zip(nameList, pidList) if name == processName]

def killProcess(pid):
    p = Popen('taskkill /PID {0} /F'.format(pid), stdout=PIPE, stderr=PIPE)
    if p.stderr.read():
        return False
    return True
