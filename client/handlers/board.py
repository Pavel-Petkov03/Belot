from client.connectors.board import BoardClientConnector
from client.handlers.base import Game


class BoardClient(Game, BoardClientConnector):
    def gameplay(self, event_list):
        self.render_cards()
