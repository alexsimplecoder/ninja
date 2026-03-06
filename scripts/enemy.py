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
        self.damage = 15
        self.health = 100
        self.ml = True
        self.timer = random.randint(120, 264)
    def ai_move(self):
        if self.coll_right:
            self.mr = False
            self.ml = True
        if self.coll_left:
            self.mr = True
            self.ml = False
        if self.timer <= 0:
            self.timer = random.randint(120, 264)
            if self.mr == True or self.ml == True:
                self.ml = False
                self.mr = False
            else:
                if random.randint(1, 2) == 1:
                    self.mr = True
                else:
                    self.ml = True
        self.timer -= 1