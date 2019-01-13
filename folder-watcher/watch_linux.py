import sys
import os
from os import listdir
from pid import PidFile
import time
import threading
from threading import Lock
from monitoredFolder import MonitoredFolder
from watcher_linux import Watcher

path = './data'
timeout = 5.0

def createMonitoredFolder(monitorPath, monitorTimout):
    folder = MonitoredFolder(monitorPath, monitorTimout)
    return folder

print "Starting ", sys.argv[0]

if __name__ == "__main__":
    pidfile = os.path.join("/", "tmp", "pywatcher.pid")

    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            path = sys.argv[1]
    if len(sys.argv) > 2:
        if str.isdigit(sys.argv[2]):
            timeout = float(sys.argv[2])/1000

    with PidFile(piddir=pidfile) as p:
        print("Starting watcher for %s with detection timeout %ds" % (path, timeout)) # -> 'foo'
        watcher = Watcher(path, timeout, createMonitoredFolder)
        watcher.watch()
