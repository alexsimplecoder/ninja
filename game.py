import pygame
import os
import random
import gc
import pickle
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1000, 800))
dark_screen = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
from scripts import utils, animation, player, level, enemy, projectile, menu, share

pygame.mixer.music.load("sounds/ambience.wav")
pygame.mixer.music.play(-1)
share.jump_sound = pygame.mixer.Sound("sounds/jump.wav")
share.jump_sound.set_volume(1)

share.dash_sound = pygame.mixer.Sound("sounds/dash.wav")
share.dash_sound.set_volume(1)

compress_timer = 0
expend_timer = 40
collaps_timer = 0
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
share.unlocked_levels = 1
share.level_num = 0

def switch_to_levels():
    share.state = "level choosing"

def save():
    f = open("progress.save", "wb")
    pickle.dump([share.level_num, share.unlocked_levels], f)
    f.close()

def load():
    try:
        with open("progress.save", "rb") as f:
            share.level_num, share.unlocked_levels = pickle.load(f)
    except:
        print("data not loaded")

load()
def respawn():
    global main_player
    global level_map
    global expend_timer
    if len(enemies) == 0:
        share.level_num += 1
    print(share.level_num, share.unlocked_levels)
    if len(enemies) == 0 and share.level_num == share.unlocked_levels:
        share.unlocked_levels += 1
    level_map = level.Map(share.level_num)
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

share.switch_to_lvl = switch_to_levels

level_map = level.Map(share.level_num)

pause_menu = menu.Pause_Menu()

settings = menu.Settings()

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
            save()
            exit()
    if share.state == "game":
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
                if p.if_hit(main_player, "right"):
                    screen_shake_timer = 20
            else:
                if p.if_hit(main_player, "left"):
                    screen_shake_timer = 20
        for i in range(len(enemies)):
            screen.blit(small_figure, (900 + i*20, 50))
        for particle in projectile.particles:
            particle.render(screen, camera_x, camera_y)
            particle.update()
        for i in events:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_d:
                    main_player.mr = True
                if i.key == pygame.K_a:
                    main_player.ml = True
                if i.key == pygame.K_q and main_player.energy > 10:
                    main_player.state = "slide attack"
                    main_player.timer = 40
                    share.dash_sound.play()
                if i.key == pygame.K_r:
                    enemies = []
                if i.key == pygame.K_ESCAPE:
                    pause_menu.save_screen(screen)
                    share.state = "pause"
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
                            share.jump_sound.play()
            if i.type == pygame.KEYUP:
                if i.key == pygame.K_d:
                    main_player.mr = False
                if i.key == pygame.K_a:
                    main_player.ml = False
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
    if len(enemies) == 0 and collaps_timer == 0:
        collaps_timer = 40
    attack_hit()
    level_map.check_for_collision()
    if expend_timer > 0 and share.state == "game":
        expend_timer -= 1
        dark_screen.fill((0, 0, 0, 255))
        pygame.draw.circle(dark_screen, (255, 255, 255, 0), (500, 400), (-15 * expend_timer + 600))
        screen.blit(dark_screen, (0, 0))
    if collaps_timer > 0:
        collaps_timer -= 1
        dark_screen.fill((0, 0, 0, 255))
        pygame.draw.circle(dark_screen, (255, 255, 255, 0), (500, 400), (collaps_timer * 15))
        screen.blit(dark_screen, (0, 0))
        if collaps_timer == 0:
            respawn()
    if share.state == "level choosing":
        level_choosing_menu = menu.Level_Choosing_Menu()
        level_choosing_menu.render(screen)
        level_choosing_menu.update(events)
    if share.state == "pause":
        pause_menu.render(screen)
        pause_menu.update(events)
    if share.state == "settings":
        settings.render(screen)
        settings.update(events)
    pygame.display.update()