import pygame
import os
from src.pokemon_link_engine.utils import get_project_dir

#arial = pygame.font.SysFont("Arial", 32)
get_project_dir()

class fonts:
    pass
    #default = pygame.font.SysFont("Arial", 32)

    #dp fonts
    print(os.curdir)
    dp_32 = pygame.font.Font("./fonts/pkmndp.ttf", 32)


def get_font(source, size):
    """
    generates a font

    todo:
        maybe make this utilize jsons and support any custom font
    """
    font = pygame.font.SysFont(source, size); return font