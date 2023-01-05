import socket
from _thread import start_new_thread
import pickle
from collections import deque
from game_engine.server_game_engine import DealCardsHandler
from players.simple_player import SimplePlayer


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
