
import threading
import time
#from Frontend.scr.menu import *

class Counter_O():

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
            self.menu.horizontalSlider_Original.setValue(self.play_seconds)


        if self.reset_loop:
            self.play_seconds = 0
            self.reset_loop = False
            self.menu.horizontalSlider_Original.setValue(0)

    def reset(self):
        self.play_seconds = 0
        self.reset_loop = False
        self.menu.horizontalSlider_Original.setValue(0)

class Counter_E():

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
            self.menu.horizontalSlider_Encrypt.setValue(self.play_seconds)


        if self.reset_loop:
            self.play_seconds = 0
            self.reset_loop = False
            self.menu.horizontalSlider_Encrypt.setValue(0)

    def reset(self):
        self.play_seconds = 0
        self.reset_loop = False
        self.menu.horizontalSlider_Encrypt.setValue(0)



class Counter_E2():

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
            self.menu.horizontalSlider_Encrypt2.setValue(self.play_seconds)


        if self.reset_loop:
            self.play_seconds = 0
            self.reset_loop = False
            self.menu.horizontalSlider_Encrypt2.setValue(0)

    def reset(self):
        self.play_seconds = 0
        self.reset_loop = False
        self.menu.horizontalSlider_Encrypt2.setValue(0)


class Counter_D():

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
            self.menu.horizontalSlider_Desencrypt.setValue(self.play_seconds)


        if self.reset_loop:
            self.play_seconds = 0
            self.reset_loop = False
            self.menu.horizontalSlider_Desencrypt.setValue(0)

    def reset(self):
        self.play_seconds = 0
        self.reset_loop = False
        self.menu.horizontalSlider_Desencrypt.setValue(0)

#test = Counter()