import pygame
import random
from scripts import animation, player, utils, projectile
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
        self.gun_timer = 0
        self.gun = utils.load_image("graph/images/gun.png", 3, color_key=(0, 0, 0))
        self.lgun = pygame.transform.flip(self.gun, True, False)
        self.lgun.set_colorkey((0, 0, 0))
    def render(self, screen, camera_x, camera_y, player_hitbox):
        self.animations[self.state].render((self.x - camera_x, int(self.y - camera_y)), f"{self.dir}", screen)
        self.seeing_sight.x -= camera_x 
        self.seeing_sight.y -= camera_y
        if self.dir == "right":
            screen.blit(self.gun, (self.x + 30 - camera_x, self.y + 30 - camera_y))
        else:
            screen.blit(self.lgun, (self.x - camera_x, self.y + 30 - camera_y))
    def ai_move(self, player_hitbox:pygame.Rect, camera_x, camera_y):
        if not player_hitbox.colliderect(self.seeing_sight):
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
        else:
            if self.gun_timer == 0:
                p = projectile.Projectile((int(self.x) + 30 if self.dir == "right" else int(self.x), self.y + 23), self.dir)
                projectile.projectiles.append(p)
                self.gun_timer = random.randint(120, 300)
            self.gun_timer -= 1
    def in_sight(self):
        if self.dir == "right":
            self.seeing_sight = pygame.Rect(self.x + 30, self.y - 200, 500, 300)
        else:
            self.seeing_sight = pygame.Rect(self.x - 500, self.y - 200, 500, 300)
        return self.seeing_sight