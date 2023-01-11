import math

import pygame
from utils import get_screen_size

WINDOW_HEIGHT, WINDOW_WIDTH = get_screen_size()


class CardSprite(pygame.sprite.Sprite):
    cards_folder = "cards_pngs/"
    animation_divider = 10

    def __init__(self, suit, rank, start_pos, owner):
        pygame.sprite.Sprite.__init__(self)
        self.suit = suit
        self.rank = rank
        self.image = pygame.Surface((WINDOW_WIDTH / 12, WINDOW_HEIGHT / 8,))
        self.start_pos = start_pos
        self.player_rotation_degrees = None
        self.owner = owner
        self.destination_pos = None
        self.rect = None
        self.given = False

    def make_card_rotation(self):
        self.rotate(self.player_rotation_degrees)

    def on_wanted_position(self):
        return self.rect.centerx == self.destination_pos[0] and self.rect.centery == self.destination_pos[1]

    def calculate_destination_of_movement(self):
        current_x, current_y = self.rect.center
        destination_x, destination_y = self.destination_pos

        step_x = abs(current_x - destination_x) / self.animation_divider
        step_y = abs(current_y - destination_y) / self.animation_divider
        new_x = self.define_movement_axis(current_x, destination_x, step_x)
        new_y = self.define_movement_axis(current_y, destination_y, step_y)
        self.rect.center = (new_x, new_y)

    def define_movement_axis(self, current_vertex, destination_vertex, step):
        if current_vertex < destination_vertex:
            current_vertex += step
        else:
            current_vertex -= step
        if abs(current_vertex - destination_vertex) <= self.animation_divider:
            return destination_vertex
        return current_vertex

    # def draw(self):
    #     window.blit(self.image, self.rect)

    def back_rotate(self):
        self.rotate(-self.player_rotation_degrees)

    def load_image(self):
        location = f"{self.suit}_{self.rank}.png"
        self.rect = pygame.Rect((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), (WINDOW_WIDTH / 12, WINDOW_HEIGHT / 8))
        self.image = pygame.image.load(self.cards_folder + location)
        self.rect.center = self.start_pos
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.make_card_rotation()

    def rotate(self, degrees):
        self.image = pygame.transform.rotate(self.image, degrees)

    def blit(self, screen):
        screen.blit(self.image, self.rect)

    def __getstate__(self):
        return {
            "suit": self.suit,
            "rank": self.rank,
            "start_pos": self.start_pos,
            "destination_pos": self.destination_pos,
            "owner": self.owner,
            "player_rotation_degrees": self.player_rotation_degrees,
            "rect": self.rect,
            "given": self.given,
        }

    def __repr__(self):
        return f'{self.suit} {self.rank}'
