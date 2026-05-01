import pygame
import math
import random
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
    def if_hit(self, player, camera_x, camera_y, dir):
        if self.get_hitbox().colliderect(pygame.Rect(player.x, player.y, 42, 54)):
            player.health -= 10
            projectiles.remove(self)
            for i in range(5):
                particles.append(Particle((player.x + 42, player.y + 40), dir))
                return True
    def get_hitbox(self):
        hitbox = pygame.Rect(self.x, self.y, projectile.get_width(), projectile.get_height())
        return hitbox

class Particle:
    def __init__(self, coords, dir, color="red"):
        self.x = coords[0]
        self.y = coords[1]
        self.color = color
        if dir == "right":
            self.angle = random.randint(-90, 90) * (math.pi/180)
            self.v = 3
            self.vx = self.v * math.cos(self.angle)
            self.vy = self.v * math.sin(self.angle)
        else:
            self.angle = random.randint(90, 270) * (math.pi/180)
            self.v = 3
            self.vx = self.v * math.cos(self.angle)
            self.vy = self.v * math.sin(self.angle)
        self.timer = 210
    def render(self, screen, camera_x, camera_y):
        pygame.draw.circle(screen, self.color, (self.x - camera_x, self.y - camera_y), 3)
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        if self.timer == 0:
            particles.remove(self)
        self.timer -= 1

projectiles:list[Projectile] = []
particles = []