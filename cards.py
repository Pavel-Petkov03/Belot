import pygame

from variables import WINDOW_WIDTH, WINDOW_HEIGHT, window


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_image_location(self):
        return f"{self.rank}_of_{self.suit}.png"


class Deck(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)


class CardSprite(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image_location, degrees):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WINDOW_WIDTH / 12, WINDOW_HEIGHT / 8))
        self.image_location = image_location
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.image = pygame.image.load(image_location)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image = pygame.transform.rotate(self.image, degrees)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=(x_pos, y_pos)).center)

    def update(self, *args, **kwargs) -> None:
        window.blit(self.image, self.rect)
