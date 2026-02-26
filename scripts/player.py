from scripts import animation, physics
import pygame

class Player:
    def __init__(self, coords, grid_tiles):
        self.dir = "right"
        self.mr, self.ml = False, False
        self.in_the_air = False
        self.x, self.y = coords
        self.jumps_done = 0
        self.ay = physics.gravity
        self.vy = 0
        self.vx = 0
        self.colliding = False
        self.animations = {
            "idle" : animation.Animation("graph/entities/player/idle", 3, 6),
            "run" : animation.Animation("graph/entities/player/run", 3, 6),
            "jump" : animation.Animation("graph/entities/player/jump", 3, 6),
            "wall slide" : animation.Animation("graph/entities/player/wall_slide", 3, 6)
        }
        self.state = "idle"
        self.grid_tiles = grid_tiles
    def render(self, screen, camera_x, camera_y):
        self.animations[self.state].render((self.x - camera_x, int(self.y - camera_y)), f"{self.dir}", screen)
    def update(self, tile_size):
        global jumps_done
        self.colliding = False
        if self.state == "wall slide":
            self.vy += self.ay / 4
        else:
            self.vy += self.ay
        self.y += self.vy
        self.collsion_y(tile_size)
        self.animations[self.state].update()
        if self.ml == True:
            self.x -= 7
            self.state = "run"
            self.dir = "left"
        if self.mr == True:
            self.x += 7
            self.state = "run"
            self.dir = "right"
        dx = self.vx
        if self.ml == True:
            dx -= 7
        if self.mr == True:
            dx += 7
        self.x += self.vx
        self.vx *= 0.9
        self.collision_x(tile_size, dx)
        if self.mr == False and self.ml == False and self.in_the_air == False:
            self.state = "idle"
        if self.in_the_air == True:
            self.state = "jump"
        if self.in_the_air == False:
            self.jumps_done = 0
        if self.in_the_air and self.colliding:
            self.state = "wall slide"
    def collision_x(self, tile_size, dx):
        for i in self.grid_tiles:
            if self.grid_tiles[i]["solid"]:
                hitbox = pygame.Rect(self.x, self.y, 42, 54).inflate(-20, 0)
                tile_hitbox = pygame.Rect(i[0] * tile_size, i[1] * tile_size, tile_size, tile_size)
                if hitbox.colliderect(tile_hitbox):
                    if dx < 0:
                        self.x = tile_hitbox.x + tile_size - 10
                    elif dx > 0:
                        self.x = tile_hitbox.x - 32
                    elif hitbox.centerx < tile_hitbox.centerx:
                        self.x = tile_hitbox.x - 32
                    else:
                        self.x = tile_hitbox.x + tile_size - 10
                    self.colliding = True
    def collsion_y(self, tile_size):
        for i in self.grid_tiles:
            if self.grid_tiles[i]["solid"]:
                hitbox = pygame.Rect(self.x, self.y, 42, 54).inflate(-20, 0)
                tile_hitbox = pygame.Rect(i[0] * tile_size, i[1] * tile_size, tile_size, tile_size)
                if hitbox.colliderect(tile_hitbox):
                    if self.vy > 0:
                        self.y = tile_hitbox.y - 54
                        self.vy = 0
                        self.in_the_air = False
                    if self.vy < 0:
                        self.y = tile_hitbox.y + tile_size
                        self.vy = 0
    # def is_touching_solid(self, tiles, tile_size):
    #     self.hitbox = pygame.Rect(self.x, self.y, 42, 54)
    #     result = False
    #     tiles_collided_with = []
    #     top = False 
    #     bottom = False 
    #     left = False
    #     right = False
    #     for i in tiles[0]:
    #         if self.hitbox.colliderect(tiles[0][i]["x"] * tile_size, tiles[0][i]["y"] * tile_size, tile_size, tile_size):
    #             result = True
    #             if self.x + 14 < tiles[0][i]["x"] * tile_size:
    #                 right = True
    #             if self.x > tiles[0][i]["x"] * tile_size:
    #                 left = True
    #             if self.y + 18 < tiles[0][i]["y"] * tile_size:
    #                 bottom = True
    #             if self.y > tiles[0][i]["y"] * tile_size:
    #                 top = True
    #             tiles_collided_with.append(i)
    #     for i in tiles[1]:
    #         if self.hitbox.colliderect(i["x"], i["y"], tile_size, tile_size):
    #             result = True
    #             if self.x < i["x"]:
    #                 right = True
    #             if self.x > i["x"]:
    #                 left = True
    #             if self.y < i["y"]:
    #                 bottom = True
    #             if self.y > i["y"]:
    #                 top = True
    #             tiles_collided_with.append(i)
        
    #     return result, tiles_collided_with, right, left, bottom, top
        
