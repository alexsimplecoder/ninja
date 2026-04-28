import pygame
import os
import random
import gc
screen = pygame.display.set_mode((1000, 800))
dark_screen = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
from scripts import utils, animation, player, level, enemy, projectile, menu, share

compress_timer = 0
expend_timer = 40
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
screen_shake_timer = 0
small_figure = utils.load_image("graph/entities/enemy/idle/00.png", 1.12, color_key=(0, 0, 0))
level_num = 0

def respawn():
    global main_player
    global level_num
    global level_map
    global expend_timer
    if len(enemies) == 0:
        level_num += 1
    level_map = level.Map(level_num)
    main_player = player.Player(level_map.get_player_coords(), level_map.grid_tiles)
    share.player = main_player
    share.state = "game"
    enemies.clear()
    for cds_2 in level_map.get_enemies_coords():
        enemies.append(enemy.Enemy(cds_2[0], cds_2[1], level_map.grid_tiles))
    projectile.projectiles.clear()
    expend_timer = 40
    gc.collect()

def attack_hit():
    for i in enemies.copy():
        if main_player.state == "slide attack" and main_player.get_hitbox().colliderect(i.get_hitbox()):
            i.health -= 35
            if i.health <= 0:
                enemies.remove(i)
            for j in range(13):
                projectile.particles.append(projectile.Particle(i.get_hitbox().center, "right" if j % 2 == 0 else "left"))

share.respawn = respawn

level_map = level.Map(level_num)

coords = level_map.get_player_coords()


main_player = player.Player(coords, level_map.grid_tiles)
share.player = main_player
enemies:list[enemy.Enemy] = []
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
                if i.key == pygame.K_q and main_player.energy > 10:
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
            i.render(screen, camera_x, camera_y)
            i.update(level_map.tile_size)
            i.ai_move(pygame.Rect(main_player.x - camera_x, main_player.y- camera_y, 42, 54).inflate(-20, 0), level_map)
            i.in_sight()
        for p in projectile.projectiles:
            p.render(screen, camera_x, camera_y)
            p.update()
            if p.x > main_player.x:
                if p.if_hit(main_player, camera_x, camera_y, "right"):
                    screen_shake_timer = 20
            else:
                if p.if_hit(main_player, camera_x, camera_y, "left"):
                    screen_shake_timer = 20
        for i in range(len(enemies)):
            screen.blit(small_figure, (900 + i*20, 50))
        for particle in projectile.particles:
            particle.render(screen, camera_x, camera_y)
            particle.update()
    if share.state == "menu":
        level_map.menu.render(screen)
        level_map.menu.update(events)
    if screen_shake_timer > 0:
        screen_shake_timer -= 1
        camera_x += random.randint(-screen_shake_timer, screen_shake_timer)
        camera_y += random.randint(-screen_shake_timer, screen_shake_timer)
    if share.state == "death menu":
        level_map.death_menu.render(screen)
        level_map.death_menu.update(events)
    if len(enemies) == 0:
        respawn() 
    attack_hit()
    level_map.check_for_collision()
    if expend_timer > 0:
        expend_timer -= 1
        dark_screen.fill((0, 0, 0, 255))
        pygame.draw.circle(dark_screen, (255, 255, 255, 0), (500, 400), (-15 * expend_timer + 600))
    pygame.display.update()