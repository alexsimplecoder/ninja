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
        self.play_button = button.Button((350, 650, 300, 120), "Play", (110, 110, 255), (200, 200, 200), pygame.font.Font("Swamp Ninja.ttf", 32))
        self.play_button.slot = lambda:switch_to_game(level_map)
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

class Level_Choosing_Menu:
    def __init__(self):
        self.level_buttons:list[button.Button] = []
        x, y = 30, 30
        for i in range(2):
            self.level_buttons.append(button.Button((x, y, 50, 50), f"lvl {i}", (255, 255, 255), ((0, 255, 0) if share.level_num > i else (255, 0, 0)), pygame.font.Font("Swamp Ninja.ttf", 10)))
            x += 80
    def render(self, screen):
        for i in self.level_buttons:
            i.render(screen)
    def update(self, events):
        for i in self.level_buttons:
            i.update(events)