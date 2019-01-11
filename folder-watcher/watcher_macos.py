import os
from threading import Lock
import time

class Watcher():

    _lock = Lock()
    _sub_paths = {}
 
    def __init__(self, path, timeout, createMonitoredFolder):
        self._path = path
        self._timeout = timeout
        self._createMonitoredFolder = createMonitoredFolder

    def listfiles(self, path):
        file_paths =[] 
        for root, _, files in os.walk(path):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths

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
        folder.Add(filepath)

    def watch(self):

        files = set(self.listfiles(self._path))

        while True:
            new_files = set(self.listfiles(self._path))
            diffAdd = new_files - files
            diffDel = files - new_files

            if (len(diffAdd) > 0) or (len(diffDel) > 0):
                for file in diffAdd:
                    self.added(file)
                for file in diffDel:                    
                    self.removed(file)
            files = new_files
            time.sleep(0.5)
