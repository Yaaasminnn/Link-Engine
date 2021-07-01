import keyboard
import time

class Key:
    def __init__(self, key):
        self.pressed = False
        self.key = key
        self.init_time = 0
        self.now = 0
        self.counter = 0

    def toggle(self):
        """
        Checks if you are pressing a key. if you have just pressed it, it will return True. but if you have
        been pressing it for some time or not pressing at all, it will return False
        """
        if keyboard.is_pressed(self.key):
            if not self.pressed: self.pressed = True; return True

            if self.pressed: return False
        self.pressed = False
        return False

    def hold(self):
        """

        :return:
        """
        from main import FPS
        if keyboard.is_pressed(self.key):
            self.counter+=1
            if self.counter == FPS: self.counter = 0;return True
            if self.counter == 75: self.counter = 0
            print(self.counter)
        return False
