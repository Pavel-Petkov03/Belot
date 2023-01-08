import random
from collections import deque

from card_sprites.sprites import CardSprite
from players.simple_player import SimplePlayer
from rendering_and_card_dealing_mechanics.generate_deck import generate_cards
from utils import get_screen_size

WIDTH, HEIGHT = get_screen_size()


class BelotServerEngine:
    def __init__(self):
        self.players = deque()  # the first one will give the cards

    def accept_player_connection(self, data, connection=None):
        player = SimplePlayer(data["name"], connection)
        self.players.append(player)
        print(self.players)
        return {}

    def get_args(self, data):
        try:
            result = data["params"]
            return result
        except KeyError:
            return None

    def load_func(self, data, func, conn):
        args = self.get_args(data)
        if args:
            return func(args, connection=conn)
        return func(connection=conn)

    def customised_result(self, result):
        if not result:
            result = {
                "data": "void"
            }
        else:
            result = {
                "data": result
            }
        return result

    def dispatch_action(self, data, conn):
        func = getattr(self, data["action"])
        result = self.load_func(data, func, conn)
        return self.customised_result(result)

    def get_players(self, connection=None):
        return self.players

    def get_info(self, data, conn):
        return self.dispatch_action(data, conn)


class DealCardsHandler(BelotServerEngine):

    def __init__(self):
        super().__init__()
        self.cards = generate_cards()
        random.shuffle(self.cards)
        self.receivers_count = 0

    def deal_cards(self, connection=None):
        hand_taker = self.players[0]
        print(hand_taker)
        current_players_deque = self.shift_to_player(connection, deque(self.players.copy()))
        self.get_n_cards_and_give_to_player(self.cards, 3, hand_taker, current_players_deque)
        self.players.rotate()
        return self.players

    def shift_to_player(self, connection, players_deque):
        while connection != players_deque[0].connection:
            players_deque.rotate()

        return players_deque

    def get_n_cards_and_give_to_player(self, cards, n, player, current_players_deque):
        if self.receivers_count == 4:
            [cards.pop() for _ in range(n)]
            self.receivers_count = 0
        else:
            self.receivers_count += 1
        for i in range(n):
            card = cards[-(i + 1)]

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
            player.cards.append(card_sprite)

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
