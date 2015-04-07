from datetime import datetime, timedelta
import time
from Tkinter import END

class Timer:
    def __init__(self, timelbl):
        self.timelbl = timelbl
        self.fmt = "%H:%M:%S"
        self.startTime = time.strftime(self.fmt)

    def updateClock(self):
        #calculate delta since start
        tdelts = datetime.strptime(time.strftime(self.fmt), self.fmt) - datetime.strptime(self.startTime, self.fmt) 

        #clear time label and repopulate with updated elapsed time
        self.timelbl.delete(1.0, END)
        self.timelbl.insert(1.0, str(tdelts))
