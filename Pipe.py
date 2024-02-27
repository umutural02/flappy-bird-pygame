from Utils import *
from ImageHandler import *
import random

class Pipe:
    def __init__(self, x, current_game_speed):
        
        self.point_collected = False
        self.height = random.randint(int(SCREEN_HEIGHT * 0.3) , int(SCREEN_HEIGHT * 0.7))
        self.gap = PIPE_VERTICAL_GAP
        self.speed = current_game_speed
        self.image = scale_image(load_image(PIPE_SPRITE_PATH), SCREEN_SIZE_MULTIPLIER)

        # Bottom part of the pipe
        self.locationBottom = [x, self.height]
        self.rectBottom = self.image.get_rect(topleft=self.locationBottom)

        # Top part of the pipe
        self.locationTop = [x, self.height - self.gap - self.image.get_height()]
        self.rectTop = self.image.get_rect(topleft=self.locationTop)


    def update(self):
        # Accelerate the pipe
        self.speed += GAME_ACCELERATION_PER_SECOND / FPS

        self.locationBottom[0] -= self.speed
        self.rectBottom.topleft = self.locationBottom

        self.locationTop[0] -= self.speed
        self.rectTop.topleft = self.locationTop

    def draw(self, screen):
        screen.blit(self.image, self.rectBottom)
        screen.blit(rotate_image(self.image, 180), self.rectTop)

    def is_off_screen(self):
        return self.locationBottom[0] < -self.image.get_width()
    
    def is_point_collected(self):
        return self.point_collected
    
    def set_point_collected(self):
        self.point_collected = True
    
