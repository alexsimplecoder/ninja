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
        self.play_button = button.Button((350, 650, 300, 120), "Play", (180, 180, 180), (200, 200, 200), pygame.font.Font("Swamp Ninja.ttf", 32))
        self.buttons = [self.play_button]
        self.play_button.slot = lambda:switch_to_game(level_map)
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
    def __init__(self, level_map):
        self.font = pygame.font.Font("Swamp Ninja.ttf", 32)
        self.play_again_button = button.Button((350, 650, 300, 120), "Respawn", (255, 20, 40), (30, 255, 57), self.font)
        self.play_again_button.slot = lambda:switch_to_game(level_map)
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