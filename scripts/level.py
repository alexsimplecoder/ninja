import pygame, pickle
from scripts import utils, physics

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
        f.close()
    def render(self, screen, camera_x, camera_y):
        screen.blit(self.background, (0, 0))
        for i in self.grid_tiles:
            image = self.resources[self.grid_tiles[i]["resource_name"]][self.grid_tiles[i]["variant"]]
            coords = (i[0] * self.tile_size - camera_x, i[1] * self.tile_size - int(camera_y))
            screen.blit(image, coords)
        for i in self.non_grid_tiles:
            image = self.resources[i["resource_name"]][i["variant"]]
            coords = (i["x"] - camera_x, int(i["y"] - camera_y))
            screen.blit(image, coords)
    def get_player_coords(self):
        for i in self.grid_tiles:
            if self.grid_tiles[i]["resource_name"] == "spawners":
                if self.grid_tiles[i]["variant"] == 0:
                    del self.grid_tiles[i]
                    return i[0] * self.tile_size, i[1] * self.tile_size