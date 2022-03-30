import pygame
import sys
from random import randint

class Particle(): # consider making math functions with this?
    def __init__(self, pos:list[int],colour:tuple[int,int, int], r:int, direction:list[int], g:list[float]=(0.0,0.0), decay_rate:float=0.1):
        """
        Initializes a particle.

        A particle is an entity that is spawned in a location, given a randomized velocity in a given direction,
        and has a radius that decays over time. when the particle's radius reaches 0, it is deleted.

        Upon initialization, we determine the position the particle spawns in, its gravity, radius and decay rate
        and colour based on the parameters. we then determine velocity.
        """
        self.pos = [pos[0], pos[1]]
        self.colour = colour
        self.g = g
        self.r = randint(r-1, r+1)
        self.decay_rate = decay_rate
        self.v = []
        self.determine_velocity(direction)

    def determine_velocity(self, directions):
        """
        Determines the velocity of the particle.

        Uses the direction to determine the velocity. direction has a domain of [-1,1] inclusively. (make float)
        the value of the direction is multiplied by 2.
        if the direction is 0 for any dimension, we generate a random number between [-1,1] inclusively.
        """
        for i,direction in enumerate(directions):
            v=0
            v+=randint(0,20)/10-1 # random integer from [1,-1]
            if direction !=0: # if direction !=0, we add a magnitude and then a direction
                v += abs(direction)*2 # magnitude
                v*=direction # direction
            self.v.append(v)

    def move(self):
        """
        Moves the particle.

        Adds
        """
        for i in range(len(self.v)):
            self.pos[i] += self.v[i]
            self.v[i] += self.g[i]

    def decay(self):
        """
        decays the particle.

        reduces the radius by the decay rate every frame. once it hits 0, we remove it from te array
        """
        self.r -= self.decay_rate
        # if self.r <=0: del self

# example usage
if __name__ == '__main__':
    clock = pygame.time.Clock()
    pygame.init()
    window = pygame.display.set_mode((500,500))

    particles = [] # the list of particles

    while True: # main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        # creates a white particle with a radius of 5 moving upwards, feeling a downward gravitational force every frame
        particles.append(Particle([250,250], (255,255,255), r=5, direction=[0,-1], g=[0,0.05]))

        for i in range(len(particles)-1, 0, -1): # simulates every particle in particles
            p=particles[i]
            p.move()
            p.decay()
            pygame.draw.circle(window, p.colour, p.pos, p.r)
            if p.r<=0: particles.remove(p) # removes it if it's size <=0

        pygame.display.flip()
        window.fill((0,0,0))
        clock.tick(60)