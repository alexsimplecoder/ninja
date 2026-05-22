import pygame
from scripts import button, share

pygame.init()

def switch_state(state):
    share.state = state
    share.player.health = 100

def switch_music_mode():
    share.music_on = not share.music_on
    if share.music_on:
        share.dash_sound.set_volume(1)
        share.hit_sound.set_volume(1)
        share.jump_sound.set_volume(1)
        share.shoot_sound.set_volume(1)
        pygame.mixer.music.set_volume(1)
    if not share.music_on:
        share.dash_sound.set_volume(0)
        share.hit_sound.set_volume(0)
        share.jump_sound.set_volume(0)
        share.shoot_sound.set_volume(0)
        pygame.mixer.music.set_volume(0)

def switch_level(level_num):
    if level_num <= share.unlocked_levels - 1:
        share.level_num = level_num
        share.respawn()

class Main_Menu:
    def __init__(self, level_map):
        self.sky = (200, 20, 70)
        self.play_button = button.Button((350, 650, 300, 120), "Play", (110, 110, 255), (200, 200, 200), pygame.font.Font("Swamp Ninja.ttf", 32))
        self.play_button.slot = lambda:switch_state("game")
        self.settings = button.Button((700, 550, 170, 90), "Settings", (255, 255, 255), (130, 130, 130), pygame.font.Font("Swamp Ninja.ttf", 32))
        self.settings.slot = lambda:switch_state("settings")
        self.level_button = button.Button((700, 400, 170, 90), "levels", "blue", (60, 255, 100), pygame.font.Font("Swamp Ninja.ttf", 32))
        self.level_button.slot = share.switch_to_lvl
        self.buttons = [self.play_button, self.level_button, self.settings]
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
    def __init__(self):
        self.font = pygame.font.Font("Swamp Ninja.ttf", 32)
        self.play_again_button = button.Button((350, 650, 300, 120), "Respawn", (255, 20, 40), (30, 255, 57), self.font)
        self.play_again_button.slot = share.respawn
        self.back_to_menu = button.Button((700, 270, 140, 60), "back to menu", (0, 255, 0), (0, 0, 255), self.font)
        self.back_to_menu.slot = lambda:switch_state("menu")
        self.buttons:list[button.Button] = []
        self.buttons.extend([self.play_again_button, self.back_to_menu])
        self.sky = (200, 20, 70)
    def render(self, screen:pygame.Surface):
        super().render(screen)
        text = self.font.render("You Have Died Warrior", True, (255, 0, 0))
        screen.blit(text, (400, 300))
    def update(self, events):
        for i in self.buttons:
            i.update(events)

class Level_Choosing_Menu:
    def __init__(self):
        self.level_buttons:list[button.Button] = []
        x, y = 30, 30
        print(share.level_num, "new")
        for i in range(3):
            b = button.Button((x, y, 50, 50), f"lvl {i}", (255, 255, 255), ((0, 255, 0) if share.unlocked_levels - 1 > i else ((255, 0, 0) if share.unlocked_levels - 1 < i else (0, 0, 255))), pygame.font.Font("Swamp Ninja.ttf", 10))
            self.level_buttons.append(b)
            b.slot = lambda level_num = i :switch_level(level_num)
            x += 80
        back_button = button.Button((800, 50, 100, 40), "back", (0, 255, 100), (255, 0, 0), pygame.font.Font("Swamp Ninja.ttf", 30))
        self.level_buttons.append(back_button)
        back_button.slot = lambda:switch_state("menu")
    def render(self, screen):
        for i in self.level_buttons:
            i.render(screen)
    def update(self, events):
        for i in self.level_buttons:
            i.update(events)

class Pause_Menu:
    def __init__(self):
        self.button_back_to_menu = button.Button((400, 300, 140, 70), "back to menu", (0, 255, 0), (50, 50, 50), pygame.font.Font("Swamp Ninja.ttf", 18))
        self.button_back_to_game = button.Button((400, 400, 140, 70), "back", (255, 0, 0), (50, 50, 50), pygame.font.Font("Swamp Ninja.ttf", 18))
        self.button_back_to_game.slot = lambda:switch_state("game")
        self.button_back_to_menu.slot = lambda:switch_state("menu")
    def render(self, screen):
        screen.blit(self.screen_shot, (0, 0))
        self.button_back_to_game.render(screen)
        self.button_back_to_menu.render(screen)
    def update(self, events):
        self.button_back_to_game.update(events)
        self.button_back_to_menu.update(events)
    def save_screen(self, screen):
        self.screen_shot = pygame.surface.Surface(screen.get_size())
        self.screen_shot.blit(screen, (0, 0))

class Settings:
    def __init__(self):
        self.music_button = button.Button((450, 280, 100, 40), "music ON" if share.music_on else "music OFF", (0, 255, 0) if share.music_on else (255, 0, 0), (30, 30, 30), pygame.font.Font("Swamp Ninja.ttf", 18))
        self.music_button.slot = self.slot
        self.back = button.Button((100, 100, 100, 40), "back to menu", (0, 255, 0), (255, 255, 255), pygame.font.Font("Swamp Ninja.ttf", 18))
        self.back.slot = lambda:switch_state("menu")
    def render(self, screen):
        screen.fill((130, 130, 130))
        self.music_button.render(screen)
        self.back.render(screen)
    def update(self, events):
        self.music_button.update(events)
        self.back.update(events)
    def slot(self):
        switch_music_mode()
        self.music_button = button.Button((450, 280, 100, 40), "music ON" if share.music_on else "music OFF", (0, 255, 0) if share.music_on else (255, 0, 0), (30, 30, 30), pygame.font.Font("Swamp Ninja.ttf", 18))
        self.music_button.slot = self.slot