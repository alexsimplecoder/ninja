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
            p.if_hit(main_player, camera_x, camera_y)
    if share.state == "menu":
        level_map.menu.render(screen)
        level_map.menu.update(events)
    if share.state == "death menu":
        level_map.death_menu.render(screen)
        level_map.death_menu.update(events)
    pygame.display.update()