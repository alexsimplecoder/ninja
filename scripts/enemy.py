import pygame
import random
from scripts import animation, player
class Enemy(player.Player):
    def __init__(self, x, y, grid_tiles):
        super().__init__((x, y), grid_tiles)
        self.animations = {
            "idle" : animation.Animation("graph/entities/enemy/idle", 3, 6),
            "run" : animation.Animation("graph/entities/enemy/run", 3, 6)
        }