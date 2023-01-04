import pygame
from utils import get_screen_size

WINDOW_HEIGHT, WINDOW_WIDTH = get_screen_size()


class CardSprite(pygame.sprite.Sprite):
    cards_folder = "cards_png/"

    def __init__(self, suit, rank, x_pos, y_pos, owner):
        pygame.sprite.Sprite.__init__(self)
        self.suit = suit
        self.rank = rank
        self.image = pygame.Surface((WINDOW_HEIGHT / 8, WINDOW_WIDTH / 12,))
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.image = self.load_image()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.player_rotation_degrees = owner.rotation_degrees_of_own_cards
        self.make_card_rotation()
        self.owner = owner

    def make_card_rotation(self):
        self.rotate(self.player_rotation_degrees)

    def calculate_destination_of_movement(self):
        speed = 4
        center_x = WINDOW_WIDTH / 2
        center_y = WINDOW_HEIGHT / 2
        step_x = int((center_x - self.rect.x) / 20)
        step_y = int((center_y - self.rect.y) / 20)
        self.rect.x += step_x * speed
        self.rect.y += step_y * speed

    # def draw(self):
    #     window.blit(self.image, self.rect)

    def back_rotate(self):
        self.rotate(-self.player_rotation_degrees)

    def load_image(self):
        location = f"{self.suit}_{self.rank}.png"
        return pygame.image.load("../cards_pngs/" + location)

    def __repr__(self):
        return f"{self.rank}_of_{self.suit} sprite"

    def rotate(self, degrees):
        self.image = pygame.transform.rotate(self.image, degrees)
