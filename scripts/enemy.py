import pygame
import random
from scripts import animation
class Enemy:
    def __init__(self, x, y):
        self.dir = "right"
        self.x = x
        self.y = y
        self.right = False
        self.left = False
        self.animations = {
            "idle" : animation.Animation("graph/entities/enemy/idle", 3, 6),
            "run" : animation.Animation("graph/entities/enemy/run", 3, 6)
        }
        self.state = "idle"
    def render(self, screen, camera_x, camera_y):
        self.animations[self.state].render((self.x - camera_x, int(self.y - camera_y)), f"{self.dir}", screen)
    def update(self):
        number = random.randint(1, 3)
        if number == 1:
            self.right = True
            self.state = "run"
            self.dir = "right"
            self.left = False
        elif number == 2:
            self.left = True
            self.state = "run"
            self.dir = "left"
            self.right = False
        elif number == 3:
            self.state = "idle"
        if self.right == True:
            self.x += 7
        if self.left == True:
            self.x -= 7
