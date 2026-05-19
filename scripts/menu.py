import pygame
from scripts import button, share

pygame.init()

def switch_state(state):
    share.state = state
    share.player.health = 100

def switch_level(level_num):
    share.level_num = level_num
    share.respawn()

class Main_Menu:
    def __init__(self, level_map):
        self.sky = (200, 20, 70)
        self.play_button = button.Button((350, 650, 300, 120), "Play", (110, 110, 255), (200, 200, 200), pygame.font.Font("Swamp Ninja.ttf", 32))
        self.play_button.slot = lambda:switch_state("game")
        self.level_button = button.Button((700, 400, 170, 90), "levels", "blue", (60, 255, 100), pygame.font.Font("Swamp Ninja.ttf", 32))
        self.level_button.slot = share.switch_to_lvl
        self.buttons = [self.play_button, self.level_button]
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
        for i in range(2):
            b = button.Button((x, y, 50, 50), f"lvl {i}", (255, 255, 255), ((0, 255, 0) if share.level_num > i else ((255, 0, 0) if share.level_num < i else (0, 0, 255))), pygame.font.Font("Swamp Ninja.ttf", 10))
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