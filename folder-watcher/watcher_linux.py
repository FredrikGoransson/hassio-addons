import os
import asyncore
import pyinotify
import time
from threading import Lock

class EventHandler(pyinotify.ProcessEvent):

    def __init__(self, watcher):
        self._watcher = watcher

    def process_IN_CREATE(self, event):
         print("+ %s" % (event.pathname))
         self._watcher.added(event.pathname)

    def process_IN_DELETE(self, event):
         print("- %s" % (event.pathname))
         self._watcher.removed(event.pathname)

class Watcher():

    _lock = Lock()
    _sub_paths = {}

    def __init__(self, path, timeout, createMonitoredFolder):
        self._path = path
        self._timeout = timeout
        self._createMonitoredFolder = createMonitoredFolder

    def getMonitoredFolder(self, filepath):
        sub_path = os.path.dirname(filepath)
        with self._lock:
            if sub_path in self._sub_paths:
                monitoredFolder = self._sub_paths[sub_path]
            else:

                monitoredFolder = self._createMonitoredFolder(sub_path, self._timeout)
                self._sub_paths[sub_path] = monitoredFolder
        
        return monitoredFolder

    def added(self, filepath):
        folder = self.getMonitoredFolder(filepath)
        folder.Add(filepath)

    def removed(self, filepath):
        folder = self.getMonitoredFolder(filepath)
        folder.Remove(filepath)

    def watch(self):

        wm = pyinotify.WatchManager()  # Watch Manager
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

        evthdl = EventHandler(self)
        pyinotify.AsyncNotifier(wm, evthdl)
        wm.add_watch(self._path, mask, rec=True)

        asyncore.loop()