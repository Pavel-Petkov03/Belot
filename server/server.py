import random
import socket
from _thread import start_new_thread
import pickle
from collections import deque

from players.simple_player import SimplePlayer
from rendering_and_card_dealing_mechanics.generate_deck import generate_cards


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

    def get_players(self):
        return self.players

    def get_info(self, data, conn):
        return self.dispatch_action(data, conn)


class DealCardsHandler(BelotServerEngine):

    def __init__(self):
        super().__init__()
        self.cards = generate_cards()
        random.shuffle(self.cards)
        self.card_sprites = []

    def trying(self, connection=None):
        hand_taker = self.players[0]
        self.get_n_cards_and_give_to_player(self.cards, 3, hand_taker)
        current_players_deque = self.shift_to_player(connection, self.players.copy())
        

    def shift_to_player(self, connection, players_deque):
        while connection != players_deque[0].connection:
            players_deque.rotate()
        return players_deque

    def get_n_cards_and_give_to_player(self, cards, n, player):
        for i in range(n):
            card = cards.pop()
            player.cards.append(card)


class MainEngine(DealCardsHandler):
    pass


class Server:
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = socket.gethostbyname(socket.gethostname())
        self.port = 1117
        self.engine = MainEngine()
        self.run()

    def run(self):
        self.bind()
        self.listen()
        while True:
            client_connection, addr = self.connection.accept()
            print("Connected to: ", addr)
            start_new_thread(self.thread, (client_connection, addr))

    def bind(self):
        try:
            self.connection.bind((self.server_ip, self.port))
        except socket.error as e:
            print(str(e))

    def listen(self):
        self.connection.listen()
        print("[SERVER IS LISTENING...]")

    def thread(self, conn: socket.SocketType, address):
        while True:
            data = conn.recv(2048)
            reply = pickle.loads(data)
            if not data:
                print("Disconnected")
                conn.send(str.encode("THE CONNECTION HAS BEEN STOPPED"))
                break
            reply = self.engine.get_info(reply, conn)
            conn.sendall(pickle.dumps(reply))
        conn.close()


s = Server()
