import os.path

import pygame

# from client.handlers.decorators import always_load_func_dec
from utils.variables.contants import SCREENSIZE
from utils.variables.settings import BACKGROUND_IMAGE_URL


class Game:

    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = self.get_screen()
        self.current_state = "render_start_dialog"
        self.cards = {}
        self.announcements_done = False
        self.always_load_funcs = []

    def add_always_load_func(self, always_load_func):
        self.always_load_funcs.append(always_load_func)

    def set_current_state(self, new_state):
        self.current_state = new_state

    def render_cards(self):
        for sprite in (self.cards.values()):
            sprite.blit(self.screen)

    def dispatch(self, *args, **kwargs):
        func = getattr(self, self.current_state)
        func(*args, **kwargs)

    @staticmethod
    def get_screen():
        return pygame.display.set_mode(SCREENSIZE)

    def blit_background(self):
        image = self.render_image(BACKGROUND_IMAGE_URL)
        image = self.scale_image(image, SCREENSIZE)
        self.screen.blit(image, (0, 0))

    @staticmethod
    def render_image(image_location, ):
        return pygame.image.load(image_location).convert()

    def scale_image(self, image, scale_cord):
        return pygame.transform.scale(image, scale_cord)
