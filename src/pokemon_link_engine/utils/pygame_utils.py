"""
All pygame utilities that will be used by multiple programs
"""
import time
import pygame, sys, keyboard
from utils.directories import get_project_dir

get_project_dir()
pygame.init()
clock = pygame.time.Clock()
font = pygame.font

#MOUSE=================================================================================================================#
mouse = pygame.mouse

class Colours:
    """
    Basic colours.

    Mostly here so they can be imported instead of defined manually
    """
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    black = (0,0,0)
    white = (255,255,255)

class Fonts:
    """
    Object containing all the font objects.

    System fonts can work on all systems. however, some fonts are custom and will need to be installed into the correct
    folder to be used.

    todo:
        allow custom fonts.
        maybe make a json-style list and add each font to the list based on the name? or list the fonts as font[i]
        and add em to an array?
    """

    #defaults
    default_16 = pygame.font.SysFont("Arial", 16)
    default_32 = pygame.font.SysFont("Arial", 32)
    default_48 = pygame.font.SysFont("Arial", 48)
    default_64 = pygame.font.SysFont("Arial", 64)

    #Pokemon fonts
    dp_32 = pygame.font.Font("fonts/pkmndp.ttf", 32)
    dpbold_32 = pygame.font.Font("fonts/pkmndpb.ttf", 32)
    em = pygame.font.Font("fonts/pkmnem.ttf", 32)
    emn = pygame.font.Font("fonts/pkmnemn.ttf", 32)
    ems = pygame.font.Font("fonts/pkmnems.ttf", 32) #best font gonna keep this
    fl = pygame.font.Font("fonts/pkmnfl.ttf", 32)
    rs = pygame.font.Font("fonts/pkmnrs.ttf", 32)
    rsi = pygame.font.Font("fonts/pkmnrsi.ttf", 32)

    #Fun easter egg fonts
    mc = pygame.font.Font("fonts/minecraft.ttf", 32)
    dtm_mono = pygame.font.Font("fonts/DTM-Mono.otf",32)
    dtm_sans = pygame.font.Font("fonts/DTM-Sans.otf",32)
    hk = font.Font("fonts/Trajan Pro Regular.ttf", 32)

class Sprite:
    """
    Class with all sprite utils
    """

    class collide:

        @staticmethod
        def with_sprite(sprite1, sprite2, return_rect=False):
            """
            colliding
            colliding and side/details
            collide with group

            maybe have it return the difference in rects?
            if collided, return rect shit
            """
            collided = pygame.sprite.collide_rect(sprite1, sprite2)
            if collided == 1: collided = True
            else: collided = False

            if not return_rect: return collided #if we only care if its colliding and not how its colliding, return

            # if we actually care about how its colliding, return the positions of each sprite relative to the other
            if return_rect:
                if collided:
                    collided_rects = []
                    rect1 = sprite1.rect; rect2 = sprite2.rect
                    collided_rects.append(abs(rect1.left - rect2.right))
                    collided_rects.append(abs(rect1.right - rect2.left))
                    collided_rects.append(abs(rect1.top - rect2.bottom))
                    collided_rects.append(abs(rect1.bottom - rect2.top))
                    return collided_rects

                if not collided: return collided #but, if they arent colliding, we just return False

        @staticmethod
        def with_group(sprite1, *groups, return_rect=False, return_sprite=False, excluded=None):
            """
            Checks if a sprite is colliding with a group.

            Looks through each group and each sprite in said group and determines if it is colliding with the given sprite.
            if the sprite is colliding with a sprite in the given groups, it will return True or return the distance
            between the 2 sprites relative to eachother. if it is not colliding with any sprite in the given groups, it will
            return False.

            todo:
                maybe multithread this
                add in the ability to choose to use a sprite or a point
            """
            rects = []
            for group in groups:
                for sprite in group:
                    if sprite != excluded:
                        print("h")
                        rect = Sprite.collide.with_sprite(sprite1, sprite, return_rect=return_rect)
                        if rect is not False:
                            if return_sprite:
                                return sprite
                            rects.append(rect) #returns either True or the rect positions if its colliding

            if len(rects) >0: return rects
            return False #if the sprite isnt colliding with any groups, return False

        @staticmethod
        def group_with_point(point:tuple, *groups, return_sprite=False):
            """
            Checks if a point is colliding with a group.

            This functionally works the same as Sprite.with_group() but uses a point instead of a sprite.
            """
            for group in groups:
                for sprite in group:
                    colliding = Sprite.collide.with_point(sprite, point, return_sprite=return_sprite)
                    if colliding is not False: return colliding #can return either True or the sprite if colliding

            return False #if it aint colliding with anything, return False

        @staticmethod
        def with_point(sprite, point:tuple, return_sprite=False):
            rect = sprite.rect; left, right,top, bottom = rect.left, rect.right, rect.top, rect.bottom
            x, y= point
            if ((abs(left-x)+abs(right-x))<=abs(left-right)) and ((abs(top-y)+abs(bottom-y))<=abs(top-bottom)):
                if return_sprite:
                    return sprite
                if not return_sprite:
                    return True
            return False

    class group:
        @staticmethod
        def update(*groups):
            """
            Update all given sprite groups.

            Work on this. may require revamping the Static Sprite class
            """
            for group in groups:
                group.update()

        @staticmethod
        def draw(window, *groups):
            for group in groups:
                group.draw(window)

    @staticmethod
    def func(inputs, rects, col_tol=1):
        """rename this"""
        x, y = inputs
        for rect in rects:
            if rect[0] <= col_tol:
                if x<0: x=0
            if rect[1] <= col_tol:
                if x>0: x=0
            if rect[2] <= col_tol:
                if y<0: y=0
            if rect[3] <= col_tol:
                if y>0: y=0

        return [x,y]

    @staticmethod
    def delete(sprite):
        del sprite

class Show_Text:
    pass

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

def exit_conditions(exit=None):
    """
    All the exit conditions.

    Currently consists of pressing escape or closing the window manually.

    todo:
        make it exit if holding enter for a period of time.
    """
    for event in pygame.event.get():
        if exit is not None:
            if event.type == pygame.QUIT or keyboard.is_pressed(exit):
                pygame.quit()
                sys.exit()
        if exit is None:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def get_img():
    """
    Gets an image from user input.

    meant to use the system's file manager as a prompt. work on this

    might need to be in an os function folder of sorts
    """
    img = input("Type in the directory of the image you want")
    return img

def show_fps(window, coords=(10,10), rounded = True):
    if rounded: fps = int(clock.get_fps())
    if not rounded: fps = round(clock.get_fps(), 4)

    render_text(f"FPS: {fps}", window, coords)

def show_memory(pid, window, coords=(10,40)):
    mem_usage = memory_info(pid)

    render_text(f"Memory Usage: {mem_usage} Mib", window, coords)

def render_text(text, window, coords, colour=Colours.white, font = Fonts.ems):
    message = font.render(f"{text}", True, colour)
    window.blit(message, (coords))

def show_text(text, window, coords, color=Colours.white, font = Fonts.ems, duration=0.5):
    render_text(text, window, coords)
    init = time.time()
    return duration

def draw_hitboxes(sprite_group, window, colour=Colours.red, width=2):
    """
    Draws hitboxes around all sprites in a given sprite group.

    todo:
        Generalize this
        make it clearer
    """

    for sprite in sprite_group:
        draw_hitbox(sprite, window, colour, width)

def draw_hitbox(sprite, window, colour=Colours.red, width=2):
    rect = sprite.rect
    left = rect.left; right = rect.right; top = rect.top; bottom = rect.bottom
    linetop = pygame.draw.line(window, colour, (left, top), (right, top), width=width)
    lineleft = pygame.draw.line(window, colour, (left, top), (left, bottom), width=width)
    lineright = pygame.draw.line(window, colour, (right, top), (right, bottom), width=width)
    linebottom = pygame.draw.line(window, colour, (left, bottom), (right, bottom), width=width)

def update_screen(window, fps, colour):
    pygame.display.flip()
    clock.tick(fps)
    window.fill(colour)

