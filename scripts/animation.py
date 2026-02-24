import pygame
from scripts import utils

class Animation:
    def __init__(self, dir_path, scale, period):
        self.timer = self.period = period
        self.images = utils.load_images(f"{dir_path}", scale, color_key=(0, 0, 0))
        self.index = 0
    def render(self, coords, dir, screen):
        if dir == "right":
            screen.blit(self.images[self.index], coords)
        if dir == "left":
            reversed_image = pygame.transform.flip(self.images[self.index], True, False)
            reversed_image.set_colorkey((0, 0, 0))
            screen.blit(reversed_image, coords)

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.index += 1
            self.timer = self.period
        if self.index > len(self.images) - 1:
            self.index = 0