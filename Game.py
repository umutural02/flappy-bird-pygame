import pygame
import Background
import Bird
import Base
import Pipe
from Utils import *
from ImageHandler import *
from SoundHandler import *

class Game:
    def __init__(self):
        
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.bird = Bird.Bird()
        self.background = Background.Background()
        self.base = Base.Base()
        self.pipes = [Pipe.Pipe(i, INITIAL_GAME_SPEED) for i in [j for j in range(PIPE_INITIAL_LOCATION_X, SCREEN_WIDTH * 2, PIPE_HORIZONTAL_GAP)]]

        self.game_speed = INITIAL_GAME_SPEED
        self.point = 0
        self.point_sound = load_sound(POINT_SOUND_PATH)
        self.gameover_sound = load_sound(GAME_OVER_SOUND_PATH)
        
    
    def start(self):
        self.start_screen()
        self.main_loop()
        pygame.quit()


    def check_collision(self):
        return (self.check_pipe_collision() or self.check_base_collision())

    def check_pipe_collision(self):
        for pipe in self.pipes:
            if pipe.rectBottom.colliderect(self.bird.rect) or pipe.rectTop.colliderect(self.bird.rect):
                return True
        return False

    def check_base_collision(self):
        for rect in self.base.rects:
            if rect.colliderect(self.bird.rect):
                return True
        return False

    def check_point_collection(self):
        return not self.pipes[0].is_point_collected() and self.bird.rect.centerx > self.pipes[0].rectBottom.centerx

    def render_number(self, number):    
        number_str = str(number)
    
        total_width = 0
        digit_images = []
        for digit in number_str:
            digit_image = scale_image(load_image(NUMBERS_SPRITE_PATHS[int(digit)]), SCREEN_SIZE_MULTIPLIER)
            digit_images.append(digit_image)
            total_width += digit_image.get_width()

        x_position = SCREEN_WIDTH / 2 - total_width / 2
        y_position = SCREEN_HEIGHT * 0.1

        for digit_image in digit_images:
            self.screen.blit(digit_image, (x_position, y_position))
            x_position += digit_image.get_width()

    def render_points(self, points):
        self.render_number(points)

    def start_screen(self):
        for i in range(3):
            self.background.draw(self.screen)
            self.base.draw(self.screen)
            self.bird.draw(self.screen)
            self.render_points(3 - i)
            pygame.display.flip()
            pygame.time.wait(1000)

    def gameover_screen(self):

        gameOverImage = scale_image(load_image(GAME_OVER_SPRITE_PATH), SCREEN_SIZE_MULTIPLIER)
        gameOverRect = (SCREEN_WIDTH / 2 - gameOverImage.get_width() / 2, SCREEN_HEIGHT / 2 - gameOverImage.get_height() / 2)
        self.screen.blit(gameOverImage, gameOverRect)
        pygame.display.flip()
        pygame.time.wait(GAME_OVER_SCREEN_TIME * 1000)

    def main_loop(self):
        running = True
        while running:

            # Event check
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.bird.jump()
            
            # Update scene
            self.bird.update()
            self.background.update()
            self.base.update()
            for pipe in self.pipes:
                if pipe.is_off_screen():
                    self.pipes.append(Pipe.Pipe(self.pipes[-1].locationBottom[0] + PIPE_HORIZONTAL_GAP, self.game_speed))
                    self.pipes.remove(pipe)
                else:
                    pipe.update()

            # Render scene
            self.background.draw(self.screen)
            for pipe in self.pipes:
                pipe.draw(self.screen)
            self.render_points(self.point)
            self.base.draw(self.screen)
            self.bird.draw(self.screen)

            # Collision check
            if (self.check_collision()):
                self.gameover_sound.play()
                self.gameover_screen()
                running = False

            # Point collection check.
            if (self.check_point_collection()):
                self.pipes[0].set_point_collected()
                self.point += 1
                self.point_sound.play()

            # Accelarate the game speed.
            self.game_speed += GAME_ACCELERATION_PER_SECOND / FPS

            pygame.display.flip()
            self.clock.tick(FPS)