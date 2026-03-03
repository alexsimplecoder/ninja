import pygame
import os
from scripts import utils, animation, player, level, enemy

screen = pygame.display.set_mode((1000, 800))
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

level_map = level.Map()

coords = level_map.get_player_coords()

main_player = player.Player(coords, level_map.grid_tiles)
enemies = []
for coords in level_map.get_enemies_coords():
    enemies.append(enemy.Enemy(coords[0], coords[1], level_map.grid_tiles))

while True:
    clock.tick(FPS)
    screen.fill((255, 255, 255))
    pygame.display.set_caption(str(main_player.y))
    for i in pygame.event.get():
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_d:
                main_player.mr = True
            if i.key == pygame.K_a:
                main_player.ml = True
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
        if i.type == pygame.QUIT:
            pygame.quit()
            exit()
    if main_player.vy > 0.3:
        main_player.in_the_air = True
    level_map.render(screen, camera_x, camera_y)
    camera_x += ((main_player.x - 500) - camera_x) / 10
    camera_y += ((main_player.y - 400) - camera_y) / 10
    camera_y = int(camera_y)
    main_player.render(screen, camera_x, camera_y)
    main_player.update(level_map.tile_size)
    for i in enemies:
        i.render(screen, camera_x, camera_y)
        i.update(level_map.tile_size)
    pygame.display.update()
    print(main_player.state)