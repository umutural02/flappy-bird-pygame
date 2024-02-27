from Utils import *
from ImageHandler import *
from math import ceil

class Base:
    def __init__(self):
        temp_image = load_image(BASE_SPRITE_PATH)
        num_images = ceil(SCREEN_WIDTH / temp_image.get_width())
        self.images = [scale_image(load_image(BASE_SPRITE_PATH), SCREEN_SIZE_MULTIPLIER) for _ in range(num_images)]
        self.rects = [image.get_rect() for image in self.images]

        # Set initial positions for all images
        for i in range(num_images):
            self.rects[i].x = i * self.rects[i].width
            self.rects[i].y = SCREEN_HEIGHT - self.rects[i].height

        self.speed = INITIAL_GAME_SPEED

    def update(self):
        self.speed += GAME_ACCELERATION_PER_SECOND / FPS

        # Move all images to the left
        for rect in self.rects:
            rect.x -= self.speed

        # Check if any image is completely off the screen
        for i in range(len(self.rects)):
            if self.rects[i].right <= 0:
                # Move it to the right of the last image
                self.rects[i].x = self.rects[(i - 1) % len(self.rects)].right

    def draw(self, screen):
        for i in range(len(self.images)):
            screen.blit(self.images[i], self.rects[i])
