import pygame
import time
from random import randint
import keyboard
import sys
from graphics.sprites.Sprites.spritesheets import Spritesheet

def move(x, y, is_player):
    """
    All sprite updates are done here.

    Checks if the player is currently colliding with anything and then returns coordinates, then passes them into
    the different update functions. depending on is_player, it will either update the player or the background.
    also animates any npc's at the end as well as the players animation counter.

    is called from Sprite.player_update() or Sprite.update_all().
    is_player is True if called from Sprite.player_update(). this will update the player
    is_player is False if called from Sprite.update_all(). this will update everything else

    Examples:
        is_player                                ||If the player is updated, move the player
        >>> player_group.update(-x,-y)

        not is_player                            ||If the background is updated, move the background
        update background elements

    todo:
        there will be many many more tiles onscreen at a time, so figure out how to call all instances in a class
        for animations.
    """
    from main import player_group, background_group, npc_group, animate, gate_group, obstacle_group#, player
    # checks if collided
    for player in player_group:
        player = player

    coords = player.check_for_collisions(x, y, obstacle_group, False)
    coords = player.check_for_collisions(coords[0], coords[1], npc_group, False)

    # updates the respective sprites
    if is_player:
        for player in player_group:
            player.update(-coords[0], -coords[1])
    if not is_player:
        background_group.update(coords[0], coords[1])
        npc_group.update(coords[0], coords[1])
        gate_group.update(coords[0], coords[1], True)
        """for obstacle in obstacles_list:
            obstacle.update(coords[0], coords[1], True)"""
        obstacle_group.update(coords[0], coords[1], True)

    # animates any npc's that animate regardless of where the player is.
    for npc in npc_group:
        npc.npc_update()

    # for the player walking animations
    if animate == 1:
        player.walk(-coords[0], -coords[1], player.last_x, player.last_y)
        player.last_x, player.last_y = -coords[0], -coords[1]

def update_all(input_x, input_y):
    """
    calls Sprite.move()for all elements on-screen except the player.

    is called from Window.movement() calls Sprite.move() and sets is_player to False.

    The reason why this is its own function (as well as player_update()) is because updating the background/player
    comprises of a number of functions that may need to be executed every frame and would cause extra lines with
    the return statements in Window.movement(). none are currently in use, but may be added later on.
    """
    move(input_x, input_y, False)

def player_update(input_x, input_y):
    """
    calls Sprite.move() for just the player and not the screen.

    is called from Window.movement(). basically calls Sprite.move() and sets is_player as True.
    """
    move(input_x, input_y, True)

def get_sprite_from_group(sprite_group):
    """
    retrieves a singular sprite from a group. useful when dealing with a sprite that exists on multiple maps such as the
    player or backdrop.

    Examples:

        Need the player sprite to draw/animate on a new screen

        Draw and maniulate the background on new screens
    """
    for sprite in sprite_group:
        return sprite

class Static_Sprite(pygame.sprite.Sprite):
    """
    The sprite class for all non-animated sprites.

    in the future, most sprites will be animated so this will only be used for the given backdrop and certain sprites
    lacking an animation. this may or may not become obsolete.
    """

    def __init__(self, pos_x, pos_y, picture_path, scale=[1.0, 1.0]):
        super().__init__()
        """
        In the init method, we load the image file and then we can scale it to a certain percentage of its original size
        using the scale parameter. by default scale is set to [1,1] which loads the image at its base resolution.

        Examples:
            Sprite(0,0, picture.png, [0.5, 0.5])
            >> loads the sprite at the top left of the screen at 0.5 times the size in each dimension(4x smaller)

            Sprite(50, 50, picture.png)
            >> loads the sprite 50,50 at its default size
        """
        self.image = pygame.image.load(picture_path)  # loads the image
        self.size = self.image.get_rect().size;
        self.size = [self.size[0], self.size[1]]  # gets the size of the image and converts from tuple to array
        self.size[0] *= scale[0];
        self.size[1] *= scale[1]  # adjusts the scale depending on what size we want it to be
        self.size[0], self.size[1] = int(self.size[0]), int(self.size[1])
        self.image = pygame.transform.scale(self.image, self.size)  # sets the image to the scale we want

        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.step = 0
        self.last_x, self.last_y = 0, 0

    def update(self, input_x, input_y, is_obstacle=False):
        """
                Updates the sprite's location.

                if reaching the edge and not an obstacle(includes the backdrop) it will stop at the edges of the screen.
                Obstacles will move off-screen when reaching the edges because on a large-scale map, the screen can only
                capture so much while the player needs to be able to walk across the entire map. the only things that
                must remain on the screen at all times are the player sprite and the backdrop. everything else can go
                offscreen. also animates the player because this function executes while the player is on the inner edge
                of the screen.

                Examples:
                    (obstacle):
                        takes in x and y from inputs. then updates the x and y positions of the screen. then animates
                        the player walking and finally sets the image at the new given positions.

                    (Backdrop):
                        takes in the x and y inputs and checks if they are on the edges of the screen. if so, they stay
                        at the same positions. if not, update the x and y positions of the screen. then animates the
                        player walking and finally sets the image at the new given positions
        """
        from main import animate, sc_h, sc_w
        # keeps it from hitting the edges
        if (self.rect.left <= 0) and input_x < 0 and not is_obstacle: self.pos_x = self.pos_x  # if it hits the edge of the screen, it stays on screen
        if (self.rect.right >= sc_w) and input_x > 0 and not is_obstacle: self.pos_x = self.pos_x
        if (self.rect.top >= 0) and input_y > 0 and not is_obstacle: self.pos_y = self.pos_y
        if (self.rect.bottom <= sc_h) and input_y < 0 and not is_obstacle: self.pos_y = self.pos_y
        else:
            self.pos_x += input_x; self.pos_y += input_y

        # updates the actual position with the new x and y coordinates
        self.rect.center = [self.pos_x, self.pos_y]

class Animated_Sprite(pygame.sprite.Sprite):
    """
    Sprite class for all animated sprites.

    includes animated tiles,(obstacles, water), npc's and the player.
    """
    def __init__(self, pos_x, pos_y, picture_path):
        super().__init__()
        self.sprite = Spritesheet(picture_path)
        self.index = 0
        self.sheet = self.sprite.create_sprite_array()
        self.step = 0

        self.image = self.sheet[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.last_x, self.last_y = 0, 0
        self.counter = 0
        self.start_time = 0
        self.col_left, self.col_right, self.col_top, self.col_bottom = False, False, False, False

    #HELPER FUNCTIONS==================================================================================================#

    #might get rid of these. meant for player tile-based movement, but are kinda broken

    def is_walking(self):
        """
        returns true. if this is true, execute walk as False
        """
        delta = 0.25
        now = time.time()
        if now - self.start_time >= delta:
            return False
        return True

    def walk2(self, x, y):
        from main import player_group
        for player in player_group: player = player
        is_walking = player.is_walking() #cheks if the sprite is walking
        print(is_walking)
        if is_walking: #if they are in the loop, use the last x,y inputs as inputs
            x,y = self.last_x, self.last_y

        if x >0 and y>0:
            self.pos_x +=x; self.pos_y += y

            if not is_walking:
                self.start_time = time.time()
                player.last_x, player.last_y = x,y

    #==================================================================================================================#

    def update(self, input_x, input_y):
        """
                Updates the sprite's location.

                Works the same way as the update function. but is meant for animated sprites that have animated sprites,
                unlike the normal ones who's sprites are static. All sprites(except the player) in this class will be
                able to go offscreen and hence, when they approach the edges, they continue to move as normal. they also
                have a walking animation, but within this function, only the player is animated. npc's and animated
                tiles are animated in their animation functions.

                NPC's:
                    npc's are intended to not be able to pass through obstacles and have their own walking AI. they can
                    also be moved off-screen. also cannot enter or block "exit areas" which let the player enter new
                    areas. also executed through Animated_Sprite.npc_update(). the walking ai will be in npc_update()

                    Example:
                        Gets inputs from npc_update() and then passes them into Animated_Sprite.update(). will ignore
                        the edges and then check if colliding with any obstacles or animated tiles or the player. then
                        updates the x and y positions. does the walk animation and finally sets the image at the new
                        given coordinates.

                Player:
                    The player cannot pass through obstacles and move around directly by user input. the player cannot
                    move off-screen and is able to enter "exit areas"

                    Example:
                        Gets inputs from user input, they are inverted because when the screen is moving, the player
                        must stay stationary and smoothly switch to moving the player once it reaches the outer edges of
                        the map. checks for any collisions with npc's or animated tiles or static obstacles. then
                        updates the x and y positions. does the walk animation and finally sets the image at the new
                        given coordinates.

                Animated Tiles:
                    Animated tiles do not move, but move with the screen which will be reflected on in Sprite.move()
                    where they will be updated when the rest of the screen does. they can be moved off-screen and
                    animate every frame.

                    Example:
                        moves with the screen, using its inputs. checks if the player is colliding with it and animates
                        itself. finally, it sets the image at the new given coordinates.

        """
        from main import background_group
        backdrop = get_sprite_from_group(background_group)
        if (self.rect.left <= backdrop.rect.left) and input_x < 0 : self.pos_x = self.pos_x
        elif (self.rect.right >= backdrop.rect.right) and input_x > 0: self.pos_x = self.pos_x
        elif (self.rect.top <= backdrop.rect.top) and input_y < 0 : self.pos_y = self.pos_y
        elif (self.rect.bottom >= backdrop.rect.bottom) and input_y > 0: self.pos_y = self.pos_y
        else:
            self.pos_x += input_x; self.pos_y += input_y

        #changes the hitbox to the new coordinates
        self.rect.center = [self.pos_x, self.pos_y]

    def walk(self,x,y, last_x, last_y):
        """
        Controls the animations for animated tiles.

        For players and npc's that typically will have 16-32 different images per spritesheet, it currently works fine,
        but certain animated tiles will likely only have 2-4 hence this needs to be reworked for tiles with x amount of
        images. also needs to be worked for non-walking tiles and renamed to animate unless a seperate animate function
        is made.

        A counter is set for animating over multiple frames. and every x amount of frames, it will change the image
        rendered.
        Checks the last x and y coordinates, if they are different from the current inputs, reset the counter. also,
        only render the next image after x amount of frames. if a new image can be rendered, it checks the direction and
        then sets the index to the proper direction the player is walking in, then cycles through the animations for
        that direction. finally, it renders the new image.

        also, if the animated sprite is not moving, then it will reset the sprite image with the stationary image for
        that direction.
        """
        from main import base_speed, counter_limit

        # incrementaly increases the counter which is used for walking animations
        self.counter += 1
        if self.counter == counter_limit: self.counter = 0
        #print(f"{player.counter} {counter_limit}")

        if last_x != x or last_y != y: self.counter=0 #if you move in a new direction, reset the counter
        if self.counter % int(counter_limit/4) != 0: return #only runs if on 10th frame

        #the actual image switcher
        if x <0 and x >=-base_speed:
            if self.index < 4 or self.index > 8: self.index = 4
            self.index = (self.index + 1) % (len(self.sheet) + 1)
            if self.index == 8: self.index = 4
        if x <-base_speed:
            if self.index < 20 or self.index > 24: self.index = 20
            self.index = (self.index + 1) % (len(self.sheet) + 1)
            if self.index == 24: self.index = 20
        if x >0 and x <= base_speed:
            if self.index < 8 or self.index > 12: self.index = 8
            self.index = (self.index + 1) % (len(self.sheet) + 1)
            if self.index == 12: self.index = 8
        if x > base_speed:
            if self.index < 24 or self.index > 28: self.index = 24
            self.index = (self.index + 1) % (len(self.sheet) + 1)
            if self.index == 28: self.index = 24
        if y <0 and y >=-base_speed:
            if self.index < 12 or self.index > 16: self.index = 12
            self.index = (self.index + 1) % (len(self.sheet) + 1)
            if self.index == 16: self.index = 12
        if y < -base_speed:
            if self.index < 28 or self.index > 32: self.index = 28
            self.index = (self.index + 1) % (len(self.sheet) + 1)
            if self.index == 32: self.index = 28
        if y >0 and y <= base_speed:
            if self.index > 4: self.index = 0
            self.index = (self.index + 1) % (len(self.sheet) + 1)
            if self.index == 4: self.index = 0
        if y > base_speed:
            if self.index < 16 or self.index > 20: self.index = 16
            self.index = (self.index + 1) % (len(self.sheet) + 1)
            if self.index == 20: self.index = 16

        #if inputs are 0, then set the sprite to the stationary sprite image
        if x ==0 and y==0:
            if (self.index >=4 and self.index <8) or (self.index >= 20 and self.index < 24):
                self.index = 4; self.image = self.sheet[self.index]; return
            if (self.index >= 8 and self.index < 12) or (self.index >= 24 and self.index < 28):
                self.index = 8; self.image = self.sheet[self.index]; return
            if (self.index >= 12 and self.index < 16) or (self.index >= 28 and self.index < 32):
                self.index = 12; self.image = self.sheet[self.index]; return
            if (self.index < 4) or (self.index >= 16 and self.index < 20):
                self.index = 0; self.image = self.sheet[self.index]; return

        self.image = self.sheet[self.index] #switches the image to the new one

    def animate(self):
        """
        Animates a given sprite.

        meant to be a general purpose animation method. used for tiles such as grass, water, trees etc.
        Will cycle through the given animations it has in the spritesheet by changing the index to the next one every
        x amount of frames.
        """
        from main import counter_limit

        #incrementally increases the counter
        self.counter += 1
        if self.counter == counter_limit: self.counter = 0

        if self.counter % int(counter_limit/4) !=0: return #only animate the sprite if it is on a certain counter

        #updates the image with the new index
        self.index+=1
        if self.index == (len(self.sheet)-1): self.index =0
        self.image = self.sheet[self.index]

    def npc_update(self):
        """
        Basic NPC walking algorithm.

        incorporates tile-based movement. self.start_time is set to 0 by default and now will give time since the epoch
        in seconds. there is also a delta time which is how long we want the npc to walk for. while the npc is in a
        loop, it will continue moving in the direction it last moved in. this lasts for 1/4 of a second. after the loop
        ends, the player has a 1/100 chance of choosing new inputs and starting the loop over again, otherwise, it will
        stay still. and wait to try again. also sets the npc counter to incrementally increase. this is for the walk()
        method and allows for smooth animations.

        Examples:
            now = 1000, self.start_time = 0, delta = 0.25      || analogous to the initialization conditions
            now-self.start_time = 1000> 0.25
            >> Chooses what direction to move in and start the loop

            now = 1000, self.start = 999.5, delta = 0.25       || if the npc is out of the loop, it will do it again
            now-self.start_time = 0.5>0.25
            >> Chooses what direction to move in and start the loop

            now = 1000, self.start_time = 999.99, delta = 0.25 || npc is currently in the loop, the timer is still up
            now-self.start_time = 0.001 < 0.25
            >> Moves the player in the direction they moved last time.

        While in the loop, the npc will use the last given input, self.last_x and self.last_y as inputs. it runs
        them into check_if_collided() and then updates with the outputted coordinates from said function.

        Examples:
            coords = check_if_collided(self.last_x=-1 self.last_y =0)    || Uses tlast coordinates and is colliding
            >>> coords = [0,0]

            coords = check_if_collided(self.last_x=-1 self.last_y =0)    || Uses last coordinates and is not colliding
            >>> coords = [-1,0]

        While out of the loop, the npc will run a number between 1-100 and on a 1, it will move and assign x or y random
        inputs between -1->1. then checks for collisions, updates, sets the last variables and sets a start_time. if not
        a 1, it will do nothing and wait till the next frame.

        Examples(chance):
            chance = 50  || if chance != 1, do nothing
            >>> pass

            chance = 1   || if chance == 1, choose a random number to determine if we should move in the x/y direction
            >>> x, y = 0, 0; x_or_y = randint(0,1)
        """
        from main import base_speed, counter_limit, player_group, npc_group, obstacle_group
        delta = 0.25  # how long we walk for
        now = time.time()  # current time

        hit_box = self.rect
        if hit_box.right <= 0 or hit_box.left >= 1920 or hit_box.bottom <= 0 or hit_box.top >= 1080: return  # dosent walk offscreen

        if now - self.start_time >= delta:  # runs if you are not currently moving
            chance = randint(1, 100)  # there is a 1 in 100 chance of moving and restarting the loop(reset to 10)
            if chance == 1:
                x, y = 0, 0; x_or_y = randint(0, 1)  # determines if we move in the x or y direction
                if x_or_y == 0: x, y = randint(-base_speed, base_speed), 0
                if x_or_y == 1: x, y = 0, randint(-base_speed, base_speed)
                # replace the following with is_walking n walk

                # walking
                # checks if colliding then updates
                coords =self.check_for_collisions(x, y, obstacle_group,True) #colliding with obstacles
                coords = self.check_for_collisions(coords[0], coords[1], npc_group,True) #colliding with npc's
                coords = self.check_for_collisions(coords[0], coords[1], player_group,True) #colliding with player
                self.update(coords[0], coords[1])
                self.walk(coords[0], coords[1], self.last_x, self.last_y) #animates it
                self.last_x, self.last_y = coords[0], coords[1]  # sets the last variables
                self.start_time = time.time()  # sets the time we started walking

        else:
            # if in the loop, uses your last inputs and runs them into the collision function
            coords = self.check_for_collisions(self.last_x, self.last_y, obstacle_group, True)  # colliding with obstacles
            coords = self.check_for_collisions(coords[0], coords[1], npc_group, True)  # colliding with npc's
            coords = self.check_for_collisions(coords[0], coords[1], player_group, True)  # colliding with play
            self.update(coords[0], coords[1])
            self.walk(coords[0], coords[1], self.last_x, self.last_y) #animates it
            self.last_x, self.last_y = coords[0], coords[1]

    def check_for_collisions(self, x, y, group, independenty_moving = False):
        """
        checks if the given sprite has collided with any sprites onscreen.

        checks if the given sprite is colliding with any other sprites of the given groups, if so, set the input to 0,
        if it is moving in the same direction that is colliding with another sprite, set that input to 0. also, because
        the player's inputs are inverted on the edges, player = False normally and when it is set to true, it looks to
        see if the sprite is moving in the opposite direction to set it to 0.

        by default collided = False and collision_tol = 2(from the config file). collision_tol is the closest sprites can be before being
        considered collided and collided being set to True.
        if the given sprite is colliding with another, it will set the current inputs to 0 and return them.

        Examples:
            collided, x=1,y=0          ||self is colliding with the wall, return x/y as 0
            :return [0,0]

            not collided, x=1, y=0     ||self is not coliding with the wall, return x/y unchanged
            :return [1,0]
        """
        from main import col_tol
        collision_tol = col_tol #how close the sprites can get before colliding

        #checks if a sprite is colliding with any obstacles
        for sprite in group:
            collided = pygame.sprite.collide_rect(self, sprite); rect = sprite.rect
            if collided==1:
                left = rect.left; right = rect.right; top = rect.top; bottom = rect.bottom
                if (abs(self.rect.left-right)<=collision_tol):
                    if independenty_moving:
                        if x < 0: x = 0
                    else:
                        if x > 0: x = 0
                if (abs(self.rect.right-left)<=collision_tol):
                    if independenty_moving:
                        if x > 0: x = 0
                    else:
                        if x < 0: x = 0
                if (abs(self.rect.top-bottom)<=collision_tol):
                    if independenty_moving:
                        if y < 0: y = 0
                    else:
                        if y > 0: y = 0
                if (abs(self.rect.bottom-top)<=collision_tol):
                    if independenty_moving:
                        if y > 0: y = 0
                    else:
                        if y < 0: y = 0

        # puts the x and y coordinates into an array to be used in the move function
        coords = []; coords.append(x); coords.append(y)
        return coords

class Window:
    """
    Class with all the functions relating to the window or functions called in the main-game loop which lead to calling
    functions in other classes.

    also consists of other functions that can be grouped
    """
    @staticmethod
    def movement(x,y):
        """
        deals with all the movement.

        if you approach the edges of the screen, the player will be moved. the player also
        moves if off-centered on an axis and is moving along the same axis. if moving along an axis that is not
        offcenter, move the background. if the backdrop has not reached any edges of the screen, update the background.

        Examples:
            backdrop.pos_x ==0 and x== -1         ||backdrop has reached an edge, and player is moving in that direction
            >>> player_update(x,y)

            backdrop.pos_x == 200 and x== 1/-1        ||backdrop has not reached an edge and the player is moving around
            >>> update_all(x,y)

            player.pos_x == 600 and x ==1/-1          ||off-set on the x axis(pos_x!=960) and moving on the x axis(x!=0)
            >>> player_update(x,y)

            player.pos_y == 300 and y == 1/-1         ||off-set on the y axis(pos_y!=540) and moving on the y axis(y!=0)
            >>> player_update(x,y)

            player.pos_x == 40 and y == 1/-1           ||offset on the x axis, but is moving on the y axis, screen moves
            >>> update_all(x,y)
        """
        from main import background_group, player_group, mid_x, mid_y, sc_h, sc_w, base_speed
        player = get_sprite_from_group(player_group)
        backdrop = get_sprite_from_group(background_group)
        #moves the player if the backdrop reaches an edge and are moving towards that edge, making the player off-center
        if (backdrop.rect.left >= 0 and x>0) or (backdrop.rect.right <= sc_w and x<0) or (backdrop.rect.top >= 0 and y>0) or (backdrop.rect.bottom <= sc_h and y<0):
            player_update(x, y)
            return

        #if the player is off-center on an axis, but is not moving towards the edge of the screen
        if (backdrop.rect.left>=0 and x<=0) or (backdrop.rect.right<=sc_w and x>=0) or (backdrop.rect.top>=0 and y<=0) or (backdrop.rect.bottom<=sc_h and y>=0):
            #if the player is off-center on one axis, move the player if they move along that axis
            if (abs(player.pos_x-mid_x)>base_speed and x != 0) or (abs(player.pos_y-mid_y)>base_speed and y != 0):
                player_update(x, y)
                return

            update_all(x, y)
            return

        update_all(x,y)
        return

    @staticmethod
    def update_screen(x,y):
        """
        All the update commands.

        calls Window.movement(x,y,pressed) to process inputs.
        pygame.display.flip() draws the new frame
        Window.FPS_limit(FPs) limits to a maximum fps
        window.fill(colour) at the end of each frame, paint a black image that gets replaced when the new frame is drawn
        """
        from main import FPS, window
        Window.movement(x,y)
        pygame.display.flip()
        Window.FPS_limit(FPS)
        window.fill((0, 0, 0))

    @staticmethod
    def exit_conditions():
        """
        All the exit conditions.

        Currently consists of pressing escape or closing the window manually.

        todo:
            make it exit if holding enter for a period of time.
        """

        from main import exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keyboard.is_pressed(exit):
                pygame.quit()
                sys.exit()

    @staticmethod
    def draw_to_screen():
        """
        draws all the sprite groups to screen.

        Also currently draws hitboxes
        """
        from main import draw_hud, background_group, obstacle_group, player_group, npc_group, window,gate_group
        background_group.draw(window)
        obstacle_group.draw(window)
        player_group.draw(window)
        npc_group.draw(window)
        gate_group.draw(window)
        if draw_hud ==1:
            Window.show_FPS()
            Window.draw_hitboxes()

    @staticmethod
    def get_inputs():
        """
        Gets the inputs given by the user and appends them to an array to be used in Window.movement().

        Examples:
            Up arrow          ||an arrow key was pressed, set x and y to the corresponding direction
            :return x=0,y=1:

            Up arrow + Shift  ||arrow key and shift was pressed, set x and y to the corresponding directions at 2x speed
            :return x=0, y=2

            No keys pressed   ||No keys were pressed. return x,y = 0,0
            :return x=0,y=0
        """
        from main import base_speed, run_speed, up, down, right, left, dash, FPS, TARGET_FPS
        win_active = pygame.display.get_active()
        x,y = 0,0 #checks if an input is given
        inputs = []
        if win_active:
            if keyboard.is_pressed(up):     #moving upwards
                x,y = 0,base_speed #walk up
            if keyboard.is_pressed(up) and keyboard.is_pressed(dash):
                x,y = 0,run_speed #run up

            if keyboard.is_pressed(down):     #moving downwards
                x,y = 0,-base_speed #walk down
            if keyboard.is_pressed(down) and keyboard.is_pressed(dash):
                x,y = 0,-run_speed #run down

            if keyboard.is_pressed(left):     #moving left
                x,y = base_speed,0 #walk to the left
            if keyboard.is_pressed(left) and keyboard.is_pressed(dash):
                x,y = run_speed,0 #run left

            if keyboard.is_pressed(right):     #moving right
                x,y = -base_speed,0 # walk to the right
            if keyboard.is_pressed(right) and keyboard.is_pressed(dash):
                x,y = -run_speed,0 #run right

        x,y = (x/FPS)*TARGET_FPS, (y/FPS)*TARGET_FPS #multiplied by FPS and TARGET_FPS to achieve fps independence.
        inputs.append(x), inputs.append(y)
        return inputs

    #HUD BASED METHODS=================================================================================================#
    """
    Only are drawn if draw_HUD == 1
    """

    @staticmethod
    def toggle_hud():
        """
        toggles the hud when you press f3

        todo:
            add a delay onto keypresses in general
        """
        from main import debug, draw_hud
        if debug.toggle():
            if draw_hud ==1: draw_hud =0
            elif draw_hud ==0: draw_hud =1
        return draw_hud

    @staticmethod
    def draw_hitboxes():
        """
        draws hitboxes around each sprite
        """
        from main import hitbox_clr, obstacle_group, player_group, npc_group, window
        for sprite in obstacle_group:  # draws a red hit box around each obstacle
            rect =sprite.rect
            linetop = pygame.draw.line(window, hitbox_clr, (rect.left, rect.top),
                                       (rect.right, rect.top), width=2)
            lineleft = pygame.draw.line(window, hitbox_clr, (rect.left, rect.top),
                                        (rect.left, rect.bottom), width=2)
            lineright = pygame.draw.line(window, hitbox_clr, (rect.right, rect.top),
                                         (rect.right, rect.bottom), width=2)
            linebottom = pygame.draw.line(window, hitbox_clr, (rect.left, rect.bottom),
                                          (rect.right, rect.bottom), width=2)

        for sprite in player_group: #draws a hitbox for the player
            rect = sprite.rect
            linetop = pygame.draw.line(window, hitbox_clr, (rect.left, rect.top),
                                       (rect.right, rect.top), width=2)
            lineleft = pygame.draw.line(window, hitbox_clr, (rect.left, rect.top),
                                        (rect.left, rect.bottom), width=2)
            lineright = pygame.draw.line(window, hitbox_clr, (rect.right, rect.top),
                                         (rect.right, rect.bottom), width=2)
            linebottom = pygame.draw.line(window, hitbox_clr, (rect.left, rect.bottom),
                                          (rect.right, rect.bottom), width=2)

        for sprite in npc_group:
            rect = sprite.rect
            linetop = pygame.draw.line(window, hitbox_clr, (rect.left, rect.top),
                                       (rect.right, rect.top), width=2)
            lineleft = pygame.draw.line(window, hitbox_clr, (rect.left, rect.top),
                                        (rect.left, rect.bottom), width=2)
            lineright = pygame.draw.line(window, hitbox_clr, (rect.right, rect.top),
                                         (rect.right, rect.bottom), width=2)
            linebottom = pygame.draw.line(window, hitbox_clr, (rect.left, rect.bottom),
                                          (rect.right, rect.bottom), width=2)

    @staticmethod
    def FPS_limit(FPS):
        """
        gives framerate independance and sets it to the given limit.

        Will aim for vsync. gets the delta time between each frame and multiplies that with any inputs in get_inputs()
        this allows the game to mechanically act the same regardless of frame rate

        todo:
            check monitor's vsync and use that as TARGET_FPS.
            rewatch the video on fps independence
        """
        from main import prev_time, clock
        clock.tick(FPS)
        now = time.time()
        dt = now - prev_time
        prev_time = now

    @staticmethod
    def show_FPS():
        """
        Shows the current fps.
        """
        from main import clock, window, text_x, text_y, font
        current_fps = int(clock.get_fps())
        current_fps = font.render(f"FPS: {current_fps}", True, (0,0,0))
        window.blit(current_fps, (text_x,text_y))
