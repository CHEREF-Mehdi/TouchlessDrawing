import time
import threading


class setInterval:
    def __init__(self, interval, action, *args):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        self.args = args
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime += self.interval
            self.action(*self.args)

    def cancel(self):
        print('canceled')
        self.stopEvent.set()
