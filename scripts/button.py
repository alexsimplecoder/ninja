import pygame

pygame.init()

class Button:
    def __init__(self, rect_base, text, text_color, button_color, font, slot):
        self.coords = (rect_base[0], rect_base[1])
        self.text = font.render(text, False, text_color)
        self.color = button_color
        self.rect_base = rect_base
        self.slot = slot()
        self.hitbox = pygame.Rect(rect_base)
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect_base)
        screen.blit(self.text, (self.coords[0] + self.rect_base[2]/2, self.coords[1] + self.rect_base[3]/2))
    def update(self):
        coords = pygame.mouse.get_pos()
        events = pygame.event.get()
        for i in events:
            if self.hitbox.collidepoint(coords):
                if i.type == pygame.MOUSEBUTTONDOWN:
                    self.slot()