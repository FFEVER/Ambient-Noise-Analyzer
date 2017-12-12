class HistoryItem(object):
    def __init__(self,time,dba,duration):
        self.time = time
        self.dba = dba
        self.duration = duration

    def getTime(self):
        return self.time

    def getdba(self):
        return self.dba

    def getDuration(self):
        return self.duration

    def setTime(self,time):
        self.time = time

    def setdba(self,dba):
        self.dba = dba

    def setDuration(self,duration):
        self.duration = duration
