import pygame
import time

def display_text(message):
    disp_str = ""
    for char in message:
        disp_str += char
        pygame.mixer.music.play()
        if len(disp_str) == 10: disp_str+= "\n"
        print(disp_str)
        time.sleep(0.34)



#pygame.init()
#pygame.mixer.music.load("../audio/voices/sans1.mp3")
#display_text("monnnnnnnnnnnnnnnnnnnnnn")