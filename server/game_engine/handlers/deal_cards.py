import random
from collections import deque

from server.game_engine.handlers.base import BelotServerEngine
from server.game_engine.hepler_funcs.cards_generating import generate_cards
from sprites.card_sprites import CardSprite
from utils.variables.contants import WINDOW_HEIGHT, WINDOW_WIDTH


class DealCardsHandler(BelotServerEngine):

    def __init__(self):
        super().__init__()
        self.cards = generate_cards()
        random.shuffle(self.cards)
        self.receivers_count = 0

    def deal_cards(self, data, connection=None):
        hand_taker = self.players[0]
        wanted_cards = data["wanted_cards"]
        current_players_deque = self.shift_to_player(connection, deque(self.players.copy()))
        self.get_n_cards_and_give_to_player(self.cards, wanted_cards, hand_taker, current_players_deque)
        return self.all_cards(current_players_deque)

    @staticmethod
    def all_cards(current_players_deque):
        cards = []
        for player in current_players_deque:
            if player.cards:
                cards.extend(player.cards)
        return cards

    def shift_to_player(self, connection, players_deque):
        while connection != players_deque[0].connection:
            players_deque.append(players_deque.popleft())
        return players_deque

    def get_n_cards_and_give_to_player(self, cards, n, player, current_players_deque):
        self.receivers_count += 1

        if self.receivers_count == 4:
            self.receivers_count = 0
            self.make_shift()
        if self.receivers_count == 1:
            for i in range(n):
                card = cards.pop()

                rank = card.rank
                suit = card.suit
                card_sprite = CardSprite(
                    suit,
                    rank, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
                    player,
                )
                player.cards.append(card_sprite)
        for person_index in range(len(current_players_deque)):
            person = current_players_deque[person_index]
            index = 0
            for card in person.cards:
                rotation = self.calculate_degrees(current_players_deque, person)
                card.player_rotation_degrees = rotation
                card.destination_pos = self.calculate_destination_pos(index, rotation)
                index += 1

    def calculate_degrees(self, current_players_deque, player):
        index = current_players_deque.index(player)
        return index * 90

    def calculate_destination_pos(self, index, rotation):
        cards_padding = 50 * index
        dest_dict = {
            0: (WINDOW_WIDTH / 2 - cards_padding, WINDOW_HEIGHT - WINDOW_WIDTH / 12),
            90: (WINDOW_WIDTH - WINDOW_WIDTH / 12, WINDOW_HEIGHT / 2 - cards_padding),
            180: (WINDOW_WIDTH / 2 - cards_padding, 0 + WINDOW_WIDTH / 12),
            270: (0 + WINDOW_WIDTH / 12, WINDOW_HEIGHT / 2 - cards_padding)
        }

        return dest_dict[rotation]
