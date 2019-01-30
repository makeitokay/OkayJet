import time

import pygame

from . import util
from .objects.coin import Coin
from .objects.player import Player
from .settings import SCREEN_WIDTH, FPS


class Game:
    def __init__(self, surface):
        self.surface = surface

        # Идет ли игра?
        self.game = True

        self.background = util.load_image("background.jpg")
        self.background_width = self.background.get_rect().width
        self.background_x = 0

        self.sprite_groups = {
            'all': pygame.sprite.Group()
        }

        self.start_time = time.time()
        self.clock = pygame.time.Clock()

        self.player = Player(self, (30, 355))
        self.coin = Coin(self, (600, 100))

    @property
    def slide_speed(self):
        return 3 + ((time.time() - self.start_time) * 0.05)

    @property
    def intro(self):
        return self.player.rect.x > SCREEN_WIDTH // 4

    def run(self):
        while self.game:
            self.events()
            self.update()
            self.clock.tick(FPS)

    def events(self):
        self.keypress_handler()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                util.terminate()

    def update(self):
        self.update_background()
        self.sprite_groups['all'].update()
        self.sprite_groups['all'].draw(self.surface)
        pygame.display.flip()

    def update_background(self):
        x = self.background_x % self.background_width
        self.surface.blit(self.background, (x - self.background_width, 0))
        if x < SCREEN_WIDTH:
            self.surface.blit(self.background, (x, 0))
        if self.intro:
            self.background_x -= self.slide_speed

    def keypress_handler(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_SPACE]:
            self.player.move(0, -4.5)
