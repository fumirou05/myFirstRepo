import pygame
from pygame.locals import *

pygame.init()

def load_image(target):
    return pygame.image.load(target).conver_alpha()
