import pygame
from scripts import utils

utils.load_image("graph/images/projectile.png", 3, color_key=(0, 0, 0))
class Projectile:
    def __init__(self, coords, dir):
        self.x = coords[0]
        self.y = coords[1]
        self.dir = dir
    def render(self, screen):
        