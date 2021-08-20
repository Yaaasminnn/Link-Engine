import pygame

arial = pygame.font.SysFont("Arial", 32)


def get_font(source, size):
    """
    generates a font

    todo:
        maybe make this utilize jsons and support any custom font
    """
    font = pygame.font.SysFont(source, size); return font