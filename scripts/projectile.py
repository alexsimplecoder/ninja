import pygame
from scripts import utils

projectile = utils.load_image("graph/images/projectile.png", 3, color_key=(0, 0, 0))
class Projectile:
    def __init__(self, coords, dir):
        self.x = coords[0]
        self.y = coords[1]
        self.dir = dir
    def render(self, screen, camera_x, camera_y):
        screen.blit(projectile, (self.x - camera_x, self.y - camera_y))
    def update(self):
        if self.dir == "right":
            self.x += 12
        else:
            self.x -= 12
    def if_hit(self, player, camera_x, camera_y):
        if pygame.Rect(self.x - camera_x, self.y - camera_y, 24, 12).colliderect(pygame.Rect(player.x - camera_x, player.y - camera_y, 42, 54)):
            player.health -= 10
projectiles = []