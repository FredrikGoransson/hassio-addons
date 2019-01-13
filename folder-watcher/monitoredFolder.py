import os
from pid import PidFile
from os import listdir
import time
import threading
from threading import Lock

class MonitoredFolder():

    _lock = Lock()

    def __init__(self, folder, timerInterval):
        self._folder = folder
        self._timerInterval = timerInterval
        self._files = set([])
        self._hasContent = False

    @property
    def folder(self):
        return self._folder

    def OnStart(self):
        print "Starting from folder %s" % (self._folder)            

    def OnTimeout(self):
        print "Finished with %d files in folder %s" % (len(self._files), self._folder)
        for file in self._files:
            print "\t", file

    def OnTimer(self):
        with self._lock:
            timeDiff = time.time() - self._lastUpdate
            if (timeDiff > self._timerInterval) and (self._hasContent):
                self.OnTimeout()
                self._files = set([])
                self._hasContent = False

    def Add(self, filepath):
        self._folder = os.path.dirname(filepath)
        with self._lock:
            self._files.add(filepath)
            self._lastUpdate = time.time()
            if not self._hasContent:
                self._hasContent = True
                self.OnStart()
        
        timerThread = threading.Timer(self._timerInterval, self.OnTimer)
        timerThread.daemon = True
        timerThread.start()


    def Remove(self, filepath):
        self._folder = os.path.dirname(filepath)
        with self._lock:
            self._files.remove(filepath)
            self._lastUpdate = time.time()
            if not self._hasContent:
                self._hasContent = True
                self.OnStart()

        timerThread = threading.Timer(self._timerInterval, self.OnTimer)
        timerThread.daemon = True
        timerThread.start()