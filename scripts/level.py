import pygame, pickle
from scripts import utils, physics, menu, share, projectile

class Map:
    def __init__(self, level_num):
        f = open(f"level {level_num}", "rb")
        data = pickle.load(f)
        self.grid_tiles:dict = data["grid tiles"]
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
        self.death_menu = menu.Death_Menu()
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
    def check_for_collision(self):
        for p in projectile.projectiles.copy():
            for tile_coords in self.grid_tiles:
                if p.get_hitbox().colliderect(tile_coords[0]*self.tile_size, tile_coords[1]*self.tile_size, self.tile_size, self.tile_size):
                    projectile.projectiles.remove(p)
    def check_for_fall(self, foot_x, foot_y, dir):
        if dir == "right":
            if ((foot_x + 20) // self.tile_size, foot_y // self.tile_size) in self.grid_tiles:
                return False
        else:
            if ((foot_x - 20) // self.tile_size, foot_y // self.tile_size) in self.grid_tiles:
                return False
        return True