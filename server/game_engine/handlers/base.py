from collections import deque

from server.player import PlayerServer


class BelotServerEngine:
    def __init__(self):
        self.players = deque()
        self.sockets_connected = 0  # the first one will give the cards

    def accept_player_connection(self, data, connection=None):
        player = PlayerServer(data["name"], connection)
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

    def get_index_of_player_by_connection(self, players_array, connection):
        for index in range(len(players_array)):
            player = players_array[index]
            if player.connection == connection:
                return index

    def get_player_by_connection(self, players_array, connection):
        return players_array[self.get_index_of_player_by_connection(players_array, connection)]