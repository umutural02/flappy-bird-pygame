from Utils import *
from ImageHandler import *
from SoundHandler import *

class Bird:
    def __init__(self):
        self.speed = 0
        self.gravity = GRAVITY
        self.lift = BIRD_LIFT
        self.location = BIRD_INITIAL_LOCATION
        self.flap_images = {state: scale_image(load_image(path), SCREEN_SIZE_MULTIPLIER) for state, path in BIRD_SPRITE_PATHS.items()}
        self.current_flap_state = 'mid'
        self.image = self.flap_images[self.current_flap_state]
        self.rect = self.image.get_rect(topleft=self.location)
        self.jump_sound = load_sound(BIRD_JUMP_SOUND_PATH)

    def update(self):
        # Move the bird
        self.speed += self.gravity
        self.location[1] += self.speed 
        self.rect.topleft = self.location

        # Update flap state of the bird
        if self.speed < -BIRD_FLAP_SPEED_THRESHOLD:
            self.current_flap_state = 'up'
        elif self.speed > +BIRD_FLAP_SPEED_THRESHOLD:
            self.current_flap_state = 'down'
        else:
            self.current_flap_state = 'mid'

        # Update the image with the current flap state
        self.image = self.flap_images[self.current_flap_state]

        # Rotate the image based on the speed
        rotation_angle = -self.speed * BIRD_ROTATION_SPEED
        self.image = rotate_image(self.image, rotation_angle)

    def jump(self):
        self.jump_sound.play()
        self.speed = self.lift


    def draw(self, screen):
        screen.blit(self.image, self.rect)
