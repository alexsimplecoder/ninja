import pygame
from scripts import button

pygame.init()

def switch_to_game(level_map):
    level_map.in_menu = False

class Main_Menu:
    def __init__(self, level_map):
        self.sky = (200, 20, 70)
        self.play_button = button.Button((350, 650, 300, 120), "Play", (180, 180, 180), (200, 200, 200), pygame.font.Font("Swamp Ninja.ttf", 32), switch_to_game(level_map))
        self.buttons = [self.play_button]
    def render(self, screen):
        screen.fill(self.sky)
        pygame.draw.circle(screen, (210, 210, 210), (970, 30), 20)
        pygame.draw.circle(screen, (255, 255, 255), (977, 35), 5)
        for i in self.buttons:
            i.render(screen)
    def update(self, level_map):
        self.play_button.slot = switch_to_game(level_map)
        for i in self.buttons:
            i.update()
