import pygame
import random

class enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.right = False
        self.left = False
    def update(self):
        number = random.randint(1, 2)
        if number == 1:
            self.right = True
        else:
            self.left = True
        if self.right == True:
            pass
        if self.left == True:
            pass