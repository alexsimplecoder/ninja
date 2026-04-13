#main.py

import pygame
import os
screen = pygame.display.set_mode((1000, 800))
from scripts import utils, animation, player, level, enemy, projectile, menu, share

ground = 800
FPS = 60
clock = pygame.time.Clock()
coords = (100, 746)
index = 0
holding = False
jump_limit = 2
gravity = 0.3
camera_x = 0
camera_y = 0

def respawn():
    global main_player
    main_player = player.Player(coords, level_map.grid_tiles)
    share.player = main_player
    share.state = "game"
    print(enemy_coords)
    enemies.clear()
    print(enemy_coords)
    for cds_2 in enemy_coords:
        enemies.append(enemy.Enemy(cds_2[0], cds_2[1], level_map.grid_tiles))
    projectile.projectiles.clear()
    print(0)


share.respawn = respawn

level_map = level.Map()

coords = level_map.get_player_coords()


main_player = player.Player(coords, level_map.grid_tiles)
share.player = main_player
enemies = []
enemy_coords = list(level_map.get_enemies_coords())
for cds in enemy_coords:
    enemies.append(enemy.Enemy(cds[0], cds[1], level_map.grid_tiles))

while True:
    clock.tick(FPS)
    screen.fill((255, 255, 255))
    pygame.display.set_caption(str(main_player.y))
    events = pygame.event.get()
    for i in events:
        if i.type == pygame.QUIT:
            pygame.quit()
            exit()
    if share.state == "game":
        for i in events:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_d:
                    main_player.mr = True
                if i.key == pygame.K_a:
                    main_player.ml = True
                if i.key == pygame.K_e and main_player.energy > 10:
                    main_player.state = "slide attack"
                    main_player.timer = 40
                if i.key == pygame.K_SPACE:
                    if main_player.state == "wall slide":
                        if main_player.dir == "right":
                            main_player.vy = -12
                            main_player.vx = -15
                            main_player.mr = False
                        if main_player.dir == "left":
                            main_player.vy = -12
                            main_player.vx = 15
                            main_player.ml = False
                    else:
                        if main_player.jumps_done < jump_limit:
                            main_player.vy = -10
                            main_player.in_the_air = True
                            main_player.jumps_done += 1
            if i.type == pygame.KEYUP:
                if i.key == pygame.K_d:
                    main_player.mr = False
                if i.key == pygame.K_a:
                    main_player.ml = False
        if main_player.vy > 0.3:
            main_player.in_the_air = True
        level_map.render(screen, camera_x, camera_y, events)
        camera_x += ((main_player.x - 500) - camera_x) / 10
        camera_y += ((main_player.y - 400) - camera_y) / 10
        camera_y = int(camera_y)
        main_player.render(screen, camera_x, camera_y)
        main_player.update(level_map.tile_size)
        main_player.check_for_death(level_map)
        for i in enemies:
            i.in_sight()
            i.render(screen, camera_x, camera_y, (main_player.x - camera_x, main_player.y - camera_y, 30, 30))
            i.update(level_map.tile_size)
            i.ai_move(pygame.Rect(main_player.x - camera_x, main_player.y- camera_y, 42, 54).inflate(-20, 0), camera_x, camera_y)
            i.in_sight()
        for p in projectile.projectiles:
            p.render(screen, camera_x, camera_y)
            p.update()
            if p.x > main_player.x:
                p.if_hit(main_player, camera_x, camera_y, "right")
            else:
                p.if_hit(main_player, camera_x, camera_y, "left")
        for particle in projectile.particles:
            particle.render(screen, camera_x, camera_y)
            particle.update()
    if share.state == "menu":
        level_map.menu.render(screen)
        level_map.menu.update(events)
    if share.state == "death menu":
        level_map.death_menu.render(screen)
        level_map.death_menu.update(events)
    pygame.display.update()

 #editor.py

import pygame
import math
from scripts.utils import load_images
import pickle

pygame.init()

screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()
FPS = 60
camera_x, camera_y = 0, 0
tile_size = 16
font = pygame.font.Font(None, 32)
resources = {}
resource_names = ("decor", "grass", "large_decor", "spawners", "stone")
current_resource_pack = 0
current_resource_index = 2
grid_on = True
grid_tiles = {

}
non_grid_tiles = []
k = 1

def save():
    f = open("data file", "wb")
    data = {
        "non grid tiles": non_grid_tiles,
        "grid tiles": grid_tiles
    }
    pickle.dump(data, f)

def load():
    try:
        global non_grid_tiles, grid_tiles
        f = open("data file", "rb")
        data = pickle.load(f)
        non_grid_tiles = data["non grid tiles"]
        grid_tiles = data["grid tiles"]
        f.close()
    except:
        pass

def transform():
    for coords in grid_tiles:
        x, y = coords
        if grid_tiles[(x, y)]["resource_name"] in ("stone", "grass"):
            top = False
            left = False
            right = False
            down = False
            if (x, y - 1) in grid_tiles and grid_tiles[(x, y - 1)]["resource_name"] == grid_tiles[(x, y)]["resource_name"]:
                top = True
            if (x - 1, y) in grid_tiles and grid_tiles[(x - 1, y)]["resource_name"] == grid_tiles[(x, y)]["resource_name"]:
                left = True
            if (x + 1, y) in grid_tiles and grid_tiles[(x + 1, y)]["resource_name"] == grid_tiles[(x, y)]["resource_name"]:
                right = True
            if (x, y + 1) in grid_tiles and grid_tiles[(x, y + 1)]["resource_name"] == grid_tiles[(x, y)]["resource_name"]:
                down = True
            if not left and not top and right:
                grid_tiles[(x, y)]["variant"] = 0
            if left and not top and not right:
                grid_tiles[(x, y)]["variant"] = 2
            if left and not top and right:
                grid_tiles[(x, y)]["variant"] = 1
            if left and top and right:
                grid_tiles[(x, y)]["variant"] = 5
            if not left and top and right:
                if down:
                    grid_tiles[(x, y)]["variant"] = 7
                if not down:
                    grid_tiles[(x, y)]["variant"] = 6
            if left and top and not right:
                if down:
                    grid_tiles[(x, y)]["variant"] = 3
                if not down:
                    grid_tiles[(x, y)]["variant"] = 4
        

def render_selected_tile():
    if grid_on:
        image = resources[resource_names[current_resource_pack]][current_resource_index]
        x, y = pygame.mouse.get_pos()
        x = (x + camera_x)// tile_size * tile_size - camera_x
        y = (y + camera_y)// tile_size * tile_size - camera_y
        screen.blit(image, (x, y))
    else:
        image = resources[resource_names[current_resource_pack]][current_resource_index]
        x, y = pygame.mouse.get_pos()
        screen.blit(image, (x - image.get_width()/2, y - image.get_height()/2))

def resize():
    for i in resource_names:
        resources[i] = load_images(f"graph/resources/{i}", tile_size/16, color_key=(0, 0, 0)) 

def render_grid():
    k_start = math.ceil(camera_x / tile_size)
    x_start = k_start * tile_size - camera_x
    y_start = math.ceil(camera_y / tile_size) * tile_size - camera_y
    for x in range(int(x_start), 1000 + tile_size, tile_size):
        pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, 800))
    for y in range(int(y_start), 800 + tile_size, tile_size):
        pygame.draw.line(screen, (20, 20, 20), (0, y), (1000, y))

def render_grid_tile():
    for coords in grid_tiles:
        tile = grid_tiles[coords]
        image = resources[tile["resource_name"]][tile["variant"]]
        screen.blit(image, (coords[0] * tile_size - camera_x, coords[1] * tile_size - camera_y))

def render_non_grid_tile():
    for tile in non_grid_tiles:
        image = resources[tile["resource_name"]][tile["variant"]]
        screen.blit(image, (tile["x"] * tile_size / 16 - camera_x, tile["y"] * tile_size / 16 - camera_y))
        

resize()
load()

while True:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    events = pygame.event.get()
    for i in events:
        if i.type == pygame.QUIT:
            pygame.quit()
            exit()
        if i.type == pygame.KEYDOWN:
            if i.mod & pygame.KMOD_SHIFT:
                if i.key == pygame.K_EQUALS:
                    tile_size += 3
                    resize()
                    camera_x = camera_x * tile_size / (tile_size - 3)
                    camera_y = camera_y * tile_size / (tile_size - 3)
                if i.key == pygame.K_0:
                    tile_size = 16
            if i.key == pygame.K_MINUS:
                tile_size = max(tile_size - 3, 4)
                resize()
                camera_x = camera_x * tile_size / (tile_size + 3)
                camera_y = camera_y * tile_size / (tile_size + 3)
            if i.key == pygame.K_1:
                current_resource_pack = 0
                if current_resource_index >= len(resources[resource_names[current_resource_pack]]):
                    current_resource_index = len(resources[resource_names[current_resource_pack]]) - 1
            if i.key == pygame.K_2:
                current_resource_pack = 1
                if current_resource_index >= len(resources[resource_names[current_resource_pack]]):
                    current_resource_index = len(resources[resource_names[current_resource_pack]]) - 1
            if i.key == pygame.K_3:
                current_resource_pack = 2
                if current_resource_index >= len(resources[resource_names[current_resource_pack]]):
                    current_resource_index = len(resources[resource_names[current_resource_pack]]) - 1
            if i.key == pygame.K_4:
                current_resource_pack = 3
                if current_resource_index >= len(resources[resource_names[current_resource_pack]]):
                    current_resource_index = len(resources[resource_names[current_resource_pack]]) - 1
            if i.key == pygame.K_5:
                current_resource_pack = 4
                if current_resource_index >= len(resources[resource_names[current_resource_pack]]):
                    current_resource_index = len(resources[resource_names[current_resource_pack]]) - 1
            if i.key == pygame.K_q:
                if current_resource_index != 0:
                    current_resource_index -= 1
                else:
                    current_resource_index = len(resources[resource_names[current_resource_pack]]) - 1
            if i.key == pygame.K_e:
                if current_resource_index != len(resources[resource_names[current_resource_pack]]) - 1:
                    current_resource_index += 1
                else:
                    current_resource_index = 0
            if i.key == pygame.K_g:
                grid_on = not grid_on
            if i.key == pygame.K_KP_ENTER:
                grid_tiles.clear()
                non_grid_tiles.clear()
        if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
            if grid_on:
                solid = False
                if resource_names[current_resource_pack] == "stone" or resource_names[current_resource_pack] == "grass":
                    solid = True
                x, y = pygame.mouse.get_pos()
                x = (x + camera_x)// tile_size
                y = (y + camera_y)// tile_size
                tile = {
                    "x": x,
                    "y": y,
                    "resource_name": resource_names[current_resource_pack],
                    "variant": current_resource_index,
                    "solid": solid
                }
                grid_tiles[(x, y)] = tile
                transform()
            else:
                solid = False
                if resource_names[current_resource_pack] == "stone" or resource_names[current_resource_pack] == "grass":
                    solid = True
                x, y = pygame.mouse.get_pos()
                tile = {
                    "x": ((x + camera_x) - resources[resource_names[current_resource_pack]][current_resource_index].get_width()/2),
                    "y": ((y + camera_y) - resources[resource_names[current_resource_pack]][current_resource_index].get_height()/2),
                    "resource_name": resource_names[current_resource_pack],
                    "variant": current_resource_index,
                    "solid": solid,
                }
                non_grid_tiles.append(tile)
        if i.type == pygame.MOUSEBUTTONDOWN and i.button == 3:
            if grid_on:
                x, y = pygame.mouse.get_pos()
                x = (x + camera_x)// tile_size
                y = (y + camera_y)// tile_size
                if (x,y) in grid_tiles.keys():
                    del grid_tiles[(x, y)]
            else:
                x, y = pygame.mouse.get_pos()
                for tile in non_grid_tiles:
                    hitbox = pygame.Rect(tile["x"], tile["y"], resources[tile["resource_name"]][tile["variant"]].get_width(), resources[tile["resource_name"]][tile["variant"]].get_height())
                    if hitbox.collidepoint(x, y):
                        non_grid_tiles.remove(tile)
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        camera_y -= 5
    if pressed[pygame.K_RIGHT]:
        camera_x += 5
    if pressed[pygame.K_LEFT]:
        camera_x -= 5
    if pressed[pygame.K_DOWN]:
        camera_y += 5
    # if pressed[pygame.K_LSHIFT]:
    #     for i in events:
    #         if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
    #             x, y = pygame.mouse.get_pos()
    #             image = resources[resource_names[current_resource_pack]][current_resource_index]
    #             tile = {
    #                 "x": x,
    #                 "y": y,
    #                 "resource_name": resource_names[current_resource_pack],
    #                 "variant": current_resource_index
    #             }
    #             non_grid_tiles.append(tile)
    #         if i.type == pygame.MOUSEBUTTONDOWN and i.button == 3:
    #             x, y = pygame.mouse.get_pos()
    #             for tile in non_grid_tiles:
    #                 hitbox = pygame.Rect(tile["x"], tile["y"], resources[tile["resource_name"]][tile["variant"]].get_width(), resources[tile["resource_name"]][tile["variant"]].get_height())
    #                 if hitbox.collidepoint(x, y):
    #                     non_grid_tiles.remove(tile)
    if grid_on: 
        render_grid()
    render_selected_tile()
    render_grid_tile()
    render_non_grid_tile()
    mpos = pygame.mouse.get_pos()
    mpos_image = font.render(f"{mpos[0], mpos[1]}", False, (255, 255, 255))
    screen.blit(mpos_image, (870, 760))
    pygame.display.update()
    save()

 #animation.py

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

 #button.py

import pygame

pygame.init()

class Button:
    def __init__(self, rect_base, text, text_color, button_color, font):
        self.coords = (rect_base[0], rect_base[1])
        self.text = font.render(text, False, text_color)
        self.color = button_color
        self.rect_base = rect_base
        self.slot = None
        self.hitbox = pygame.Rect(rect_base)
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect_base)
        screen.blit(self.text, (self.coords[0] + self.rect_base[2]/2, self.coords[1] + self.rect_base[3]/2))
    def update(self, events):
        coords = pygame.mouse.get_pos()
        for i in events:
            if self.hitbox.collidepoint(coords):
                if i.type == pygame.MOUSEBUTTONDOWN and self.slot != None:
                    self.slot()

 #enemy.py

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

 #level.py

import pygame, pickle
from scripts import utils, physics, menu, share

class Map:
    def __init__(self):
        f = open("data file", "rb")
        data = pickle.load(f)
        self.grid_tiles = data["grid tiles"]
        self.non_grid_tiles = data["non grid tiles"]
        self.resources = {}
        self.camera_x = 0
        self.camera_y = 0
        self.tile_size = 48
        self.scale = self.tile_size / 16
        self.resources["decor"] = utils.load_images("graph/resources/decor", self.scale, color_key=(0, 0, 0))
        self.resources["grass"] = utils.load_images("graph/resources/grass", self.scale, color_key=(0, 0, 0))
        self.resources["large_decor"] = utils.load_images("graph/resources/large_decor", self.scale, color_key=(0, 0, 0))
        self.resources["spawners"] = utils.load_images("graph/resources/spawners", self.scale, color_key=(0, 0, 0))
        self.resources["stone"] = utils.load_images("graph/resources/stone", self.scale, color_key=(0, 0, 0))
        self.background = utils.load_image("background.png", 2.2)
        self.menu = menu.Main_Menu(self)
        self.death_menu = menu.Death_Menu(self)
        f.close()
    def render(self, screen, camera_x, camera_y, events):
        if share.state == "menu":
            self.menu.render(screen)
            self.menu.update(events)
        elif not share.state == "menu" and not share.state == "death menu":
            screen.blit(self.background, (0, 0))
            for tile in self.grid_tiles:
                image = self.resources[self.grid_tiles[tile]["resource_name"]][self.grid_tiles[tile]["variant"]]
                coords = (tile[0] * self.tile_size - camera_x, tile[1] * self.tile_size - int(camera_y))
                screen.blit(image, coords)
            for tile in self.non_grid_tiles:
                image = self.resources[tile["resource_name"]][tile["variant"]]
                coords = (tile["x"]*self.tile_size/16 - camera_x, tile["y"]*self.tile_size/16 - camera_y)
                screen.blit(image, coords)
        elif share.state == "death menu":
            self.death_menu.render(screen)
            self.death_menu.update(events)
    def get_player_coords(self):
        for i in self.grid_tiles:
            if self.grid_tiles[i]["resource_name"] == "spawners":
                if self.grid_tiles[i]["variant"] == 0:
                    del self.grid_tiles[i]
                    return i[0] * self.tile_size, i[1] * self.tile_size
    def get_enemies_coords(self):
        for i in self.grid_tiles.copy():
            if self.grid_tiles[i]["resource_name"] == "spawners":
                if self.grid_tiles[i]["variant"] == 1:
                    del self.grid_tiles[i]
                    yield i[0] * self.tile_size, i[1] * self.tile_size

 #menu.py

import pygame
from scripts import button, share

pygame.init()

def switch_to_game(level_map):
    share.state = "game"
    share.player.health = 100
    print(0)

class Main_Menu:
    def __init__(self, level_map):
        self.sky = (200, 20, 70)
        self.play_button = button.Button((350, 650, 300, 120), "Play", (180, 180, 180), (200, 200, 200), pygame.font.Font("Swamp Ninja.ttf", 32))
        self.buttons = [self.play_button]
        self.play_button.slot = lambda:switch_to_game(level_map)
    def render(self, screen):
        screen.fill(self.sky)
        pygame.draw.circle(screen, (210, 210, 210), (970, 30), 20)
        pygame.draw.circle(screen, (255, 255, 255), (977, 35), 5)
        for i in self.buttons:
            i.render(screen)
    def update(self, events):
        for i in self.buttons:
            i.update(events)

class Death_Menu(Main_Menu):
    def __init__(self, level_map):
        self.font = pygame.font.Font("Swamp Ninja.ttf", 32)
        self.play_again_button = button.Button((350, 650, 300, 120), "Respawn", (255, 20, 40), (30, 255, 57), self.font)
        self.play_again_button.slot = share.respawn
        self.buttons:list[button.Button] = []
        self.buttons.append(self.play_again_button)
        self.sky = (200, 20, 70)
    def render(self, screen:pygame.Surface):
        super().render(screen)
        text = self.font.render("You Have Died Warrior", True, (255, 0, 0))
        screen.blit(text, (400, 300))
    def update(self, events):
        for i in self.buttons:
            i.update(events)

 #physics.py

ground = 800
gravity = 0.3


 #player.py

from scripts import animation, physics, share
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
            "wall slide" : animation.Animation("graph/entities/player/wall_slide", 3, 6),
            "slide attack": animation.Animation("graph/entities/player/slide", 3, 6)
        }
        self.state = "idle"
        self.grid_tiles = grid_tiles
        self.health = 100
        self.energy = 100
        self.timer = 0
    
    def render(self, screen, camera_x, camera_y):
        healh_bar = pygame.Rect(10, 10, self.health * 2, 20)
        energy_bar = pygame.Rect(10, 50, self.energy * 2, 20)
        self.animations[self.state].render((self.x - camera_x, int(self.y - camera_y)), f"{self.dir}", screen)
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100 * 2, 20))
        pygame.draw.rect(screen, (0, 255, 0), healh_bar)
        pygame.draw.rect(screen, (0, 0, 0), (5, 5, 210, 30), 5)
        
        pygame.draw.rect(screen, (0, 0, 0), (10, 50, 100 * 2, 20))
        pygame.draw.rect(screen, (45, 114, 255), energy_bar)
        pygame.draw.rect(screen, (0, 0, 0), (5, 45, 210, 30), 5)
    
    def normal_update(self, tile_size):
        global jumps_done
        self.colliding = False
        if self.state == "wall slide":
            self.vy += self.ay / 4
        else:
            self.vy += self.ay
        self.y += self.vy
        self.collsion_y(tile_size)
        if self.state != "dead":
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
    
    def attack_update(self, tile_size):
        if self.dir == "right":
            if self.energy > 10:
                self.x += 20
                self.collision_x(tile_size, 20)
                self.energy -= 0.75
            else:
                self.state = "idle"
                self.energy = 0
        else:
            if self.energy > 10:
                self.x -= 20
                self.collision_x(tile_size, -20)
                self.energy -= 0.75
            else:  
                self.state = "idle"
                self.energy = 0

    def update(self, tile_size):
        if self.state == "slide attack":
            self.attack_update(tile_size)
            self.timer -= 1
            if self.timer == 0:
                self.state = "idle"
        else:
            self.normal_update(tile_size)
            if self.energy < 100:
                self.energy += 0.2

    def check_for_death(self, level):
        if self.health <= 0:
            share.state = "death menu"

    def collision_x(self, tile_size, dx):
        self.coll_right = False
        self.coll_left = False
        for i in self.grid_tiles:
            if self.grid_tiles[i]["solid"]:
                hitbox = pygame.Rect(self.x, self.y, 42, 54).inflate(-20, 0)
                tile_hitbox = pygame.Rect(i[0] * tile_size, i[1] * tile_size, tile_size, tile_size)
                if hitbox.colliderect(tile_hitbox):
                    if dx < 0:
                        self.x = tile_hitbox.x + tile_size - 10
                        self.coll_right = False
                        self.coll_left = True
                    elif dx > 0:
                        self.x = tile_hitbox.x - 32
                        self.coll_right = True
                        self.coll_left = False
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
        


 #projectile.py

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
        if pygame.Rect(self.x - camera_x, self.y - camera_y, 24, 12).colliderect(pygame.Rect(player.x - camera_x, player.y - camera_y, 42, 54)):
            player.health -= 10
            projectiles.remove(self)
            for i in range(5):
                particles.append(Particle((player.x + 42 - camera_x, player.y + 40 - camera_y), dir))

class Particle:
    def __init__(self, coords, dir):
        self.x = coords[0]
        self.y = coords[1]
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
        pygame.draw.circle(screen, (255, 0, 0), (self.x - camera_x, self.y - camera_y), 300)
        print(self.x, self.y)
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        if self.timer == 0:
            particles.remove(self)
        self.timer -= 1

projectiles = []
particles = []

 #share.py

state = "menu"

 #utils.py

import pygame
import os

pygame.init()
def load_image(image_path, scale=None, size=None, color_key=None):
    image = pygame.image.load(image_path).convert_alpha()
    if size == None:
        scaled_image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
    else:
        scaled_image = pygame.transform.scale(image, size)
    if color_key != None:
        scaled_image.set_colorkey(color_key)
    return scaled_image

def load_images(dir_path, scale=None, size=None, color_key=None):
    images = []
    for i in sorted(os.listdir(dir_path)):
        if i[-4:] == ".png":
            image = load_image(f"{dir_path}/{i}", scale, size, color_key)
            images.append(image)
    return images
