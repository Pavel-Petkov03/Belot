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

    def make_shift(self):
        self.players.append(self.players.popleft())


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
                    rank, (WIDTH / 2, HEIGHT / 2),
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
            0: (WIDTH / 2 - cards_padding, HEIGHT - WIDTH / 12),
            90: (WIDTH - WIDTH / 12, HEIGHT / 2 - cards_padding),
            180: (WIDTH / 2 - cards_padding, 0 + WIDTH / 12),
            270: (0 + WIDTH / 12, HEIGHT / 2 - cards_padding)
        }

        return dest_dict[rotation]


class AnnouncementsHandler(BelotServerEngine):
    def __init__(self):
        super().__init__()
        self.players_announcements_order = None
        self.sockets_connected = 0

    def set_players_announcements_order_deque(self):
        self.sockets_connected += 1
        if self.players_announcements_order is None:
            self.players_announcements_order = deque(self.players.copy())
        else:
            if self.sockets_connected == 4:
                self.sockets_connected = 0
                self.players_announcements_order.append(self.players_announcements_order.popleft())

    def check_announcements_order(self, connection=None):
        self.set_players_announcements_order_deque()
        player_on_move = self.players_announcements_order[0]
        connected_player = self.get_player_by_connection(connection)
        return player_on_move == connected_player

    def get_player_by_connection(self, connection):
        for player in self.players_announcements_order:
            if player.connection == connection:
                return player
