import random

import pygame
import sys

from graphics.effects.Particles import Particle
from random import randint, choice

clock = pygame.time.Clock()
pygame.init()
window = pygame.display.set_mode((500,500))

particles = [] # particle list
coords = [250, 250]
white = (255,255,255)
#g=[0,0.1]
#d=[0,-1]
red =(235, 64, 52)
orange = (222, 81, 20)
yellow = (227, 191, 14)
colours = (red, yellow, orange, white)
count = 5


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    # code goes here ----------------------------------------------------------- # CREATES A FLAMETHROWER

    if count >0:
        particles.append(Particle(coords, choice(colours), 7, direction=[1,-1], g=[0,0], decay_rate=0.1))                       # center
        particles.append(Particle([coords[0]+10, coords[1]-20], choice(colours), 5, direction=[1,-1], g=[0,0], decay_rate=0.1)) # top left
        particles.append(Particle([coords[0]+15, coords[1]-15], choice(colours), 6, direction=[1,-1], g=[0,0], decay_rate=0.1))# diagonal
        particles.append(Particle([coords[0]+20, coords[1]-20], choice(colours), 5, direction=[1,-1], g=[0,0], decay_rate=0.1)) # diagonal
        particles.append(Particle([coords[0]+20, coords[1]-10], choice(colours), 5, direction=[1,-1], g=[0,0], decay_rate=0.1)) # bottom right




    for i in range(len(particles)-1, 0, -1):
        p=particles[i]
        p.move()
        p.decay()
        pygame.draw.circle(window,p.colour, p.pos, p.r)
        if p.r<=0: particles.remove(p) # remove the particle

    count -=0.1

    # --------------------------------------------------------------------------

    pygame.display.flip()
    window.fill((0,0,0))
    clock.tick(60)
    #print(clock.get_fps())