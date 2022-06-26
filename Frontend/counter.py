
import threading
import time
#from Frontend.scr.menu import *

class Counter():

    def __init__(self, menu, max_time):
        self.pause_loop = False
        self.reset_loop = False

        self.play_seconds = 0
        self.pause_seconds = 0
        self.max_time = max_time
        self.menu = menu

    def start_thread(self):
        t = threading.Thread(target=self.start)
        t.start()

    def start(self):
        self.pause_loop = False
        while self.play_seconds <= self.max_time and not self.reset_loop:

            while self.pause_loop:
                pass

            print(self.play_seconds)
            self.play_seconds += 1
            time.sleep(1)
            self.menu.horizontalSlider_Track.setValue(self.play_seconds)


        if self.reset_loop:
            self.play_seconds = 0
            self.reset_loop = False
            self.menu.horizontalSlider_Track.setValue(0)

    def reset(self):
        self.play_seconds = 0
        self.reset_loop = False
        self.menu.horizontalSlider_Track.setValue(0)




#test = Counter()