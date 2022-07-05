import pygame

from variables import WINDOW_WIDTH, WINDOW_HEIGHT


class CardSprite(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WINDOW_WIDTH / 12, WINDOW_HEIGHT / 8))
        self.image.fill("green")
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank





