import random
import time
from collections import deque
from time import sleep

import pygame

from animation import Animation
from announcer import Announcer
from utils import create_deck
from variables import window, PLAYERS_DEQUE


class Row(Animation):
    def __init__(self, players_deque, cards):
        self.players_deque = deque(players_deque)  # [, next , next , next, current dealer]
        self.cards = cards
        self.first_row_given = False
        self.announcements_made = False
        self.announcer = Announcer()

    def card_dealing_before_announcements(self):
        first_row_dealing = 3
        second_row_dealing = 2
        self.make_dealing_row(first_row_dealing)
        self.make_dealing_row(second_row_dealing)
        self.first_row_given = True

    def make_announcements(self):
        self.announcer.make_announcements(self.players_deque)

    def card_dealing_after_announcements(self):
        third_row_dealing = 3
        self.make_dealing_row(third_row_dealing)

    def make_dealing_row(self, dealing_row, ):
        for player in self.players_deque:
            self.pop_n_cards_and_give_to_player(dealing_row, player)

    def pop_n_cards_and_give_to_player(self, n, player):
        for pop_card in range(n):
            taken_card = self.cards.pop()
            player.cards.append(taken_card)

    def taking_hand(self):
        pass

    def run_row(self):
        if not self.first_row_given:
            self.card_dealing_before_announcements()
        self.deal_cards_animation(self.players_deque)
        if not self.announcements_made:
            self.make_announcements()


class Game:
    pass


def run_game():
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    cards = create_deck()
    random.shuffle(cards)
    game_row = Row(PLAYERS_DEQUE, cards)
    while run:
        clock.tick(120)
        window.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:

                if not game_row.announcements_made and not game_row.announcer.toggle_animation_done:
                    (x, y) = pygame.mouse.get_pos()
                    for announce_sprite in game_row.announcer.announce_modal.available_sprites():
                        if announce_sprite.rect.collidepoint(x, y):
                            game_row.announcer.toggle_animation_done = True

        game_row.run_row()
        pygame.display.flip()


if __name__ == "__main__":
    run_game()

# pygame.time.get_ticks()
