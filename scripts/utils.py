import pygame
import os

pygame.init()
def load_image(image_path, scale=None, size=None, color_key=None):
    image = pygame.image.load(image_path).convert_alpha()
    if size == None:
        scaled_image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
    else:
        scaled_image = pygame.transform.scale(image, size)
    if color_key != None:
        scaled_image.set_colorkey(color_key)
    return scaled_image

def load_images(dir_path, scale=None, size=None, color_key=None):
    images = []
    for i in sorted(os.listdir(dir_path)):
        if i[-4:] == ".png":
            image = load_image(f"{dir_path}/{i}", scale, size, color_key)
            images.append(image)
    return images
