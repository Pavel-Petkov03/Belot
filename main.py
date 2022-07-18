import random
import time
from collections import deque
from time import sleep

import pygame

from animation import Animation
from announcer import Announcer
from card_table import CardTable
from errors import EndGameError
from utils import create_deck
from variables import window, PLAYERS_DEQUE, player_4


class Row(Animation):
    def __init__(self, players_deque, cards):
        super().__init__()
        self.players_deque = deque(players_deque)  # [, next , next , next, current dealer]
        self.temporary_deque = self.players_deque.copy()
        self.cards = cards
        self.first_row_given = False
        self.second_row_given = False
        self.announcements_made = False
        self.announcer = Announcer()
        self.card_table = CardTable()

    def card_dealing_before_announcements(self):
        first_row_dealing = 3
        second_row_dealing = 2
        self.make_dealing_row(first_row_dealing)
        self.make_dealing_row(second_row_dealing)
        self.first_row_given = True

    def make_announcements(self):
        is_done_bool = self.announcer.make_announcements(self.temporary_deque)  # returns true if done
        if is_done_bool:
            self.announcements_made = True

    def card_dealing_after_announcements(self):
        third_row_dealing = 3
        self.make_dealing_row(third_row_dealing)
        self.second_row_given = True

    def make_dealing_row(self, dealing_row, ):
        for player in self.players_deque:
            self.pop_n_cards_and_give_to_player(dealing_row, player)

    def pop_n_cards_and_give_to_player(self, n, player):
        for pop_card in range(n):
            taken_card = self.cards.pop()
            player.cards.append(taken_card)

    def run_row(self):
        self.deal_cards_animation(self.players_deque)
        if not self.first_row_given:
            self.card_dealing_before_announcements()
        elif not self.announcements_made:
            self.make_announcements()
        elif not self.second_row_given:
            self.card_dealing_after_announcements()
        else:
            self.card_table.main(self.players_deque)


class Game:
    pass

    # todo make implementation inside this class


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
                            game_row.announcer.start = pygame.time.get_ticks()
                            game_row.announcer.announce_rect_text = announce_sprite.rect_title
                            game_row.announcer.generate_available_announcements(player_4)
                            game_row.announcer.add_to_pass_list()

        game_row.run_row()
        pygame.display.flip()


if __name__ == "__main__":
    run_game()

# pygame.time.get_ticks()
