import os; os.environ["SDL_AUDIODRIVER"] = "dsp"
import pygame
from pygame import mixer
import time
import sys
#import pyaudio
import wave

x,y = 1000,1000 #display sizes
midx, midy = x/2,y/2
pygame.init() #initializes pygame
#pygame.mixer.init()
clock = pygame.time.Clock() #sets the clock so we can set an fps
window = pygame.display.set_mode((x,y)) #creates a window

font = pygame.font.SysFont("Arial", 20)

def play_sound(file):
    pass

def display_text(message):
    disp_str = ""

    pygame.mixer.music.load("./voices/sanssound.wav")
    pygame.mixer.music.play(loops=-1)

    if len(message) > 100:
        #sets a substring to the first 90 characters and then looks for a "."
        section = message[:90] #gets the first substring of 90 characters

        #gets all the indexes of the ends of sentences
        ends = []
        next_period = message.find(".", 90); ends.append(next_period)
        next_quesmrk = message.find("?",90); ends.append(next_quesmrk)
        next_exclmrk = message.find("!", 90); ends.append(next_exclmrk)

        ends.sort()
        for end in ends: #if any of those ends arent in the ends array, remove them
            if end <0: ends.remove(end)

        section += message[90:ends[0]+1] #add on the substring of the remaining end to the main substring

    for char in section: #displays it
        disp_str += char

        if len(disp_str) % 45 == 0: disp_str+= "\n" #if it reaches a certain length, move to the next line. will change to letter position in gui
        print(disp_str)
        print("\n\n")
        time.sleep(0.05)#delay

def exit_cond():
    """
    Exit conditions.

    if you close the window, it exits pygame
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if you close the window, exit
            pygame.quit()
            sys.exit()

def add_text(displayed, message):
    if displayed =="":
        displayed = message[0]; print(displayed);return displayed

    displayed += message[len(displayed):len(displayed)+1]
    if len(displayed)% 50 ==0: displayed+="\n"    #make it display the text on a new line somehow
    #maybe draw the first bit then a second. 2 at a time?
    print(displayed)
    return displayed


message = "hey there buddy chum pal friend buddy pal chum bud friend fella bruther amigo pal buddy friend chummy chum " \
          "chum pal i don't mean to be rude my friend pal home slice bread slice dawg but i gotta warn ya if u take one " \
          "more diddly darn step right there im going to have to diddly darn snap ur neck and wowza wouldn't that be a " \
          "crummy juncture, huh?"

#MAIN GAME LOOP
displayed = ""
pygame.init()
pygame.mixer.music.load("./voices/sans.wav")
pygame.mixer.music.set_volume(0.4)
#mixer.music.play()
while True:
    exit_cond() #checks for exit conditions every frame

    #==================================================================================================================#

    displayed = add_text(displayed, message)
    displayed_text = font.render(displayed, True, (255,255,255))
    window.blit(displayed_text, (0,midy))
    mixer.music.play()

    #==================================================================================================================#

    pygame.display.flip() #updates display
    clock.tick(75) #sets the fps
    window.fill((0,0,0)) #fills the screen with black every frame to move to the next frame