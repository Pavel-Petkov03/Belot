import random
import time
from collections import deque
from time import sleep

import pygame

from announcement_modal import AnnounceModal
from cards import CardSprite, Deck
from utils import create_deck
from variables import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, window, DISTANCE_BETWEEN_PLAYER_AND_WINDOW


class Player:
    def __init__(self, x_y_pos):
        self.cards = []
        self.x_y_position_on_board = x_y_pos


class Bot(Player):
    def generate_random_announcements_algorythm(self):
        # this functionality will be made later
        return "Pass"


class Animation:
    def deal_cards_animation(self, players):
        deck = Deck()
        distance_between_cards = 50
        degrees = 90
        for player in players:
            player_x, player_y = player.x_y_position_on_board
            add_tup, reduce_tup = self.define_movement_axis(player, distance_between_cards)
            add_x, add_y = add_tup
            reduce_x, reduce_y = reduce_tup
            next_card_x = player_x + add_x - reduce_x
            next_card_y = player_y + add_y - reduce_y
            for card in sorted(player.cards, key=lambda obj: (obj.suit, obj.rank)):
                animation_card = CardSprite(next_card_x, next_card_y, f"cards_png/{card.get_image_location()}", degrees)
                next_card_x += add_x
                next_card_y += add_y
                deck.add(animation_card)
                animation_card.update()
            degrees += 90

    @staticmethod
    def define_movement_axis(player, distance_between_cards):
        not_moving = 0

        player_x, player_y = player.x_y_position_on_board
        reduce_value = len(player.cards) / 2 * distance_between_cards
        if player_x in (DISTANCE_BETWEEN_PLAYER_AND_WINDOW, WINDOW_WIDTH - DISTANCE_BETWEEN_PLAYER_AND_WINDOW):
            reduce_tup = (not_moving, reduce_value)
            add_tup = (not_moving, distance_between_cards)
        else:
            add_tup = (distance_between_cards, not_moving)
            reduce_tup = (reduce_value, not_moving)
        return add_tup, reduce_tup

    @staticmethod
    def rotate_sprite(image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect


class Row(Animation):
    def __init__(self, players_deque, cards):
        self.players_deque = deque(players_deque)  # [, next , next , next, current dealer]
        self.announced_game = None
        self.cards = cards
        self.first_row_given = False

    def card_dealing_before_announcements(self):
        first_row_dealing = 3
        second_row_dealing = 2
        self.make_dealing_row(first_row_dealing)
        self.make_dealing_row(second_row_dealing)
        self.deal_cards_animation(self.players_deque)
        self.first_row_given = True

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
        self.players_deque.append(self.players_deque.popleft())

    def toggle_modal_for_announcements(self):
        AnnounceModal().toggle_modal()

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
        # self.make_announcements()


class Game:
    pass


def run_game():
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    players_deque = [Bot((WINDOW_WIDTH - DISTANCE_BETWEEN_PLAYER_AND_WINDOW, WINDOW_HEIGHT / 2)),
                     Bot((WINDOW_WIDTH / 2, DISTANCE_BETWEEN_PLAYER_AND_WINDOW)),
                     Bot((DISTANCE_BETWEEN_PLAYER_AND_WINDOW, WINDOW_HEIGHT / 2)),
                     Player((WINDOW_WIDTH / 2, WINDOW_HEIGHT - DISTANCE_BETWEEN_PLAYER_AND_WINDOW))]
    cards = create_deck()
    random.shuffle(cards)
    game_row = Row(players_deque, cards)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pass
        game_row.run_row()
        pygame.display.flip()


if __name__ == "__main__":
    run_game()
