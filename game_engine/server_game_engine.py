import random

from card_sprites.sprites import CardSprite
from rendering_and_card_dealing_mechanics.generate_deck import generate_cards
from server.server import BelotServerEngine
from utils import get_screen_size

WIDTH, HEIGHT = get_screen_size()


class DealCardsHandler(BelotServerEngine):

    def __init__(self):
        super().__init__()
        self.cards = generate_cards()
        random.shuffle(self.cards)
        self.card_sprites = []

    def trying(self, connection=None):
        hand_taker = self.players[0]
        current_players_deque = self.shift_to_player(connection, self.players.copy())
        self.get_n_cards_and_give_to_player(self.cards, 3, hand_taker, current_players_deque)
        return self.card_sprites

    def shift_to_player(self, connection, players_deque):
        while connection != players_deque[0].connection:
            players_deque.rotate()

        return players_deque

    def get_n_cards_and_give_to_player(self, cards, n, player, current_players_deque):
        for i in range(n):
            card = cards.pop()
            player.cards.append(card)

            rank = card.rank
            suit = card.suit
            rotation = self.calculate_degrees(current_players_deque, player)
            card_sprite = CardSprite(
                suit,
                rank, (WIDTH / 2, HEIGHT / 2),
                player,
                rotation,
                self.calculate_destination_pos(player, rotation)
            )
            self.card_sprites.append(card_sprite)

    def calculate_degrees(self, current_players_deque, player):
        index = current_players_deque.index(player)
        return index * 90

    def calculate_destination_pos(self, player, rotation):
        MARGIN = 100
        cards_padding = 20 * len(player.cards)
        dest_dict = {
            0: (WIDTH / 2 - cards_padding, HEIGHT - MARGIN),
            90: (WIDTH - MARGIN, HEIGHT / 2 - cards_padding),
            180: (WIDTH / 2 - cards_padding, 0 + MARGIN),
            270: (0 + MARGIN, HEIGHT / 2 - cards_padding)
        }

        return dest_dict[rotation]
