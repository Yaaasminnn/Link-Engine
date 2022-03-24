"""
dialogue display:
Developer: MON-Emperor / Loona
Date:2021-07-20

Issue:
    make sure the lines dont end in the middle of a word but rather make sure the last character was a space" "
    so, it should break line 1 if its len >= line_limit and the last character in the string is a space and
    dialogue2 should add on messages from message not based on line_limit but from len(dialogue1)
"""
import time
import keyboard
import sys
import pygame

#GLOBAL VARIABLES======================================================================================================#
line1 = ""  # empty string for line 1
line1_chckr = ""
line2 = ""  # empty string for line 2
line_limit = 90  # max number of characters per line
#PYGAME STUFF==========================================================================================================#
x,y = 1920,1080 #display sizes
pygame.init() #initializes pygame
clock = pygame.time.Clock() #sets the clock so we can set an fps
window = pygame.display.set_mode((x,y), pygame.RESIZABLE) #creates a window
colour = (255,255,255)
x1,y1 = 100, 850
x2,y2 = 100,900
font_size = 32
font = pygame.font.Font("fonts/blockgame.ttf",font_size) # make this use a game font instead.

def exit_cond():
    """
    Exit conditions.

    if you close the window, it exits pygame
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if you close the window, exit
            pygame.quit()
            sys.exit()

#FUNCTIONS=============================================================================================================#

def show_line1(line1, message):
    global line_limit

    # if the str is empty, add the first character from message to it
    if line1 == "":
        line1 += message[0]; return line1

    # if the line limit is greater than or equal to the line limit and not in the middle of a word, dont modify it
    if len(line1) >= line_limit and line1[len(line1) - 1] == " ": return line1

    # otherwise, just add the next character from message
    line1 += message[len(line1)]; return line1

def show_line2(line2, message):
    global line1, line1_chckr

    # if the first line is not yet completed, do not fill this line
    if line1 != line1_chckr: return line2

    # if dialogue2 is empty, add on the first element
    if line2 == "":
        line2 += message[len(line1)]; return line2

    line2 += message[(len(line1)) + len(line2)]; return line2

def line_checker(dialogue):
    """
    Takes in a dialogue and returns the value.
    """

    return dialogue

#MAIN STUFF============================================================================================================#

def show_lines():
    from main import conf, conversation
    textbox = conf.textbox
    global prev, line1,line2, line1_chckr
    globvars = globals()

    dialogue = conversation[str(i)]  # GETS THE SPECIFIC DIALOGUE
    message = dialogue["line"]  # THE ACTUAL SPOKEN LINE
    window.blit(textbox, (60, 800))

    now = time.time()
    if now - prev >= 0.05 and line1+line2!=message:  # UPDATES THE DIALOGUE ONLY EVERY SET AMOUNT OF TIME so long as the message isnt complete
        # Creates the fonts and lines
        line1 = show_line1(line1, message); text_box1 = font.render(line1, True, colour)  # LINE 1
        line2 = show_line2(line2, message); text_box2 = font.render(line2, True, colour)  # LINE 2
        globvars['line1_chckr'] = line_checker(line1)  # MEANT TO CHECK LINE1 SO THAT LINE 2 ONLY FILLS AFTER LINE 1
        prev = now

        window.blit(text_box1, (x1, y1));window.blit(text_box2, (x2, y2))  # displays the lines onscreen

        #return line1_chckr #returns line 1 so we can check it later

    else: # If we arent adding new text onscreen, redraw the previous text. otherwise it flashes a lot
        text_box1 = font.render(line1, True, colour)  # LINE 1
        text_box2 = font.render(line2, True, colour)  # LINE 2
        window.blit(text_box1, (x1, y1)); window.blit(text_box2, (x2, y2))  # displays the lines onscreen

def clear_lines():
    global i,line1,line2
    from main import conf, conversation
    select = conf.select

    dialogue = conversation[str(i)]; message = dialogue["line"]
    # WHAT TO DO WHEN ITS DONE PRINTING THE MESSAGE
    if line1 + line2 == message:
        if keyboard.is_pressed(select):
            line1, line2 = "", ""  # resets lines to empty strings
            #print(f"{i}/{len(conversation)}")
            i += 1
            if i > len(conversation): i = 1
            #time.sleep(2)
        pass

#MAIN GAME LOOP
i=1

prev = 0
if __name__ == "__main__":
    while True:
        exit_cond() #checks for exit conditions every frame

        show_lines()
        #pygame.display.flip()  # updates display

        clear_lines()
        clock.tick(75) #sets the fps
        window.fill((0,0,0)) #fills the screen with black every frame to move to the next frame
