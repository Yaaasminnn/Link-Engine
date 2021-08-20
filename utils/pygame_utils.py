"""
All pygame utilities that will be used by multiple programs
"""
import pygame, sys, keyboard
from utils.monitor import *

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

def create_window(x,y, resizable=True, fullscreen=False, icon=None, caption=None):
    """
    Creates a window.

    Creates and returns a pygame window with selected properties such as a resizable window or fullscreen. Additionally,
    captions and icons can be set.

    Examples:

        >>> create_window(1920,1080, resizable=True, icon="path/to/icon.png", caption="Game window")
        Creates a 1920x1080 window that is resizable with an icon and caption

        >>> create_window(1920,1080, fullscreen=True, icon="path/to/icon.png", caption="Fullscreen")
        Creates a fullscreen window

        >>> create_window(1920,1080, resizable=True)
        Creates a window with the default pygame captions and icon

    todo:
        fullscreen isnt working proerly

    """
    #if we set the window to be resizable and/or fullscreen, is_resizable and/or is_fullscreen will be turned on
    is_resizable, is_fullscreen = 0, 0
    if resizable: is_resizable = pygame.RESIZABLE
    if fullscreen: is_fullscreen = pygame.FULLSCREEN

    window = pygame.display.set_mode((x,y), is_resizable, is_fullscreen) # creates the window

    if icon is not None: # if an icon is given, it will create the display with an icon
        icon = pygame.image.load(icon)
        pygame.display.set_icon(icon)

    if caption is not None: # if a caption is given, it will create the display with a caption
        pygame.display.set_caption(caption)

    return window

def exit_conditions(exit):
    """
    All the exit conditions.

    Currently consists of pressing escape or closing the window manually.

    todo:
        make it exit if holding enter for a period of time.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keyboard.is_pressed(exit):
            pygame.quit()
            sys.exit()

def get_img():
    """
    Gets an image from user input.

    meant to use the system's file manager as a prompt. work on this
    """
    img = input("Type in the directory of the image you want")
    return img

def show_fps(window, font = font, rounded = True):
    x,y = 10, 10
    if rounded: fps = int(clock.get_fps())
    if not rounded: fps = round(clock.get_fps(), 4)
    fps = font.render(f"FPS: {fps}", True, (255,255,255))
    window.blit(fps, (x, y))

def show_memory(pid, window, x=10, y=40, font=font):
    mem_usage = memory_info(pid)
    mem_usage = font.render(f"Memory Usage: {mem_usage} Mib", True, (255,255,255))
    window.blit(mem_usage,(x, y+20))

def draw_hitboxes(sprite_group, window, colour, width=2):
    """
    Draws hitboxes around all sprites in a given sprite group.

    todo:
        Generalize this
        make it clearer
    """

    for sprite in sprite_group:
        rect = sprite.rect
        left = rect.left; right = rect.right; top = rect.top; bottom = rect.bottom
        linetop = pygame.draw.line(window, colour, (left, top), (right, top), width=2)
        lineleft = pygame.draw.line(window, colour, (left, top), (left, bottom), width=2)
        lineright = pygame.draw.line(window, colour, (right, top), (right, bottom), width=2)
        linebottom = pygame.draw.line(window, colour, (left, bottom), (right, bottom), width=2)
