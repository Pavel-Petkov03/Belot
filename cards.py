import pygame

from variables import WINDOW_WIDTH, WINDOW_HEIGHT, window


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


class Deck(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def find_card_sprite(self, suit, rank):
        return list(filter(lambda sprite: sprite.suit == suit and sprite.rank == rank, self.sprites()))[0]


class BoardCards(pygame.sprite.Group):
    pass


class CardSprite(pygame.sprite.Sprite, Card):
    cards_folder = "cards_png/"

    def __init__(self, suit, rank, x_pos, y_pos, degrees):
        pygame.sprite.Sprite.__init__(self)
        self.suit = suit
        self.rank = rank
        self.image = pygame.Surface((WINDOW_WIDTH / 12, WINDOW_HEIGHT / 8))
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.image = pygame.image.load(self.get_image_location())
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image = pygame.transform.rotate(self.image, degrees)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=(x_pos, y_pos)).center)

    def update(self, *args, **kwargs) -> None:
        window.blit(self.image, self.rect)

    def get_image_location(self):
        return f"{self.cards_folder}{self.rank}_of_{self.suit}.png"
