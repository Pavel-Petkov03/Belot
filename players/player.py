from server.client import Client


class Player:
    def __init__(self, name):
        self.name = name
        self.net = Client()

    def connect(self):
        self.net.connect()
        self.net.send({
            "params": {
                "name": self.name
            },
            "action": "accept_player_connection"
        })
