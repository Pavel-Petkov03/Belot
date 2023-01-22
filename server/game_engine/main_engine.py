from collections import deque

from server.game_engine.handlers.announcements import AnnouncementsHandler
from server.game_engine.handlers.deal_cards import DealCardsHandler


class MainEngine(DealCardsHandler, AnnouncementsHandler):

    def remove_player_on_disconnect(self, connection):
        self.players = deque([player for player in self.players if player.connection != connection])
