import random

import pygame

from utils import create_deck
from variables import WINDOW_WIDTH, WINDOW_HEIGHT, FPS


class Player:
    def __init__(self):
        self.cards = []


class Bot(Player):
    def generate_random_announcements_algorythm(self):
        pass


class Row:
    def __init__(self, players_deque, cards):
        self.players_deque = players_deque  # [, next , next , next, current dealer]
        self.announced_game = None
        self.cards = cards

    def card_dealing_before_announcements(self):
        first_row_dealing = 3
        second_row_dealing = 2
        self.make_dealing_row(first_row_dealing)
        self.make_dealing_row(second_row_dealing)

    def make_announcements(self):

        available_announcements = {
            "Pass": 0,
            "Spades": 1,
            "Diamonds": 2,
            "Hearts": 3,
            "Clubs": 4,
            "No trumps": 5,
            "All trumps": 6,
        }
        current_announcer = self.players_deque[0]
        if not isinstance(current_announcer, Bot):
            self.toggle_modal_for_announcements()
        else:
            current_announcer.generate_random_announcements_algorythm()

    def toggle_modal_for_announcements(self):
        pass

    def card_dealing_after_announcements(self):
        third_row_dealing = 3
        self.make_dealing_row(third_row_dealing)

    def make_dealing_row(self, dealing_row, ):
        for player in self.players_deque:
            self.pop_n_cards_and_give_to_player(dealing_row, player)

    def pop_n_cards_and_give_to_player(self, n, player):
        for pop_card in range(n):
            taken_card = self.cards.pop()
            taken_card.position = "player"
            player.cards.append(taken_card)

    def taking_hand(self):
        pass

    def run_row(self):
        self.card_dealing_before_announcements()


class Game:
    pass


def run_game():
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    players_deque = [Bot(), Bot(), Bot(), Player()]
    cards = create_deck()
    random.shuffle(cards)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pass
        Row(players_deque, cards).run_row()
        pygame.display.flip()


if __name__ == "__main__":
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    run_game()
