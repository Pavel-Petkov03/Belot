import pygame
from locals import *


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.image = self.load_image()

    def load_image(self):
        location = f"{self.suit}_{self.rank}.png"
        return pygame.image.load("../cards_pngs/" + location)


def generate_cards():
    cards = []
    for suit in suits:
        for rank in ranks:
            card = Card(rank, suit)
            cards.append(card)
    return cards
