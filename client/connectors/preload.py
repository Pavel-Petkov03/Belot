from client.connectors.base import ClientConnector


class PreloadClientConnector(ClientConnector):
    def socket_get_players(self):
        return self.send("get_players")
