import pygame

def load_image(path):
    return pygame.image.load(path)

def scale_image(image, scale):
    return pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)