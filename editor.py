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