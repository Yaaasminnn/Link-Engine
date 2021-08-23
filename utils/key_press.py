import keyboard

class Key:
    """
    Class for all different types of keypresses and keystrokes.
    """
    def __init__(self, key):
        self.pressed = False #reports if the key is pressed or not
        self.key = key #what key we are working with
        self.init_time = 0 #the time you start pressing a key
        self.now = 0 #current time
        self.counter = 0 #the number of frames you have been holding a key down for

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
        checks if you are holding down a key and continues executing a function so long as it is pressed.

        todo:
            work on this
        """
        from utils.system.sys_info import FPS
        if keyboard.is_pressed(self.key):
            if self.counter != FPS: self.counter+=1; return self.counter
            if self.counter == FPS: self.counter = 0;return True
            print(self.counter)
        return False
