from collections import deque

from server.game_engine.handlers.base import BelotServerEngine
from utils.variables.contants import WINDOW_WIDTH, WINDOW_HEIGHT


class AnnouncementsHandler(BelotServerEngine):
    def __init__(self):
        super().__init__()
        self.players_announcements_order = None
        self.sockets_connected = 0
        self.announced_game = None
        self.bar_counter = 100
        self.pass_counter = 0
        self.top_announcer = None
        self.points_multiply_coefficient = 1

    def set_players_announcements_order_deque(self):
        if self.players_announcements_order is None:
            self.players_announcements_order = deque(self.players.copy())

    def get_announcement_info(self, connection=None):
        top_announcer_in_same_team = self.get_player_by_connection(self.players_announcements_order, connection)
        return {
            "top_announcement": self.announced_game,
            "top_announcer_in_same_team": top_announcer_in_same_team,
            "points_multiply_coefficient": self.points_multiply_coefficient
        }

    def set_announcement(self, data, connection=None):
        self.players_announcements_order.append(self.players_announcements_order.popleft())
        current_announcement = data["announced_game"]
        self.set_announcement_algo(current_announcement)
        self.set_pass_counter(current_announcement)

    def set_announcement_algo(self, announced_game):
        announce_array = ["Pass", "Clubs", "Diamonds", "Hearts", "Spades", "No Trumps", "All Trumps"]
        if announced_game in announce_array:
            self.announced_game = announced_game
        else:
            if self.points_multiply_coefficient == 1:
                self.points_multiply_coefficient = 2
            elif self.points_multiply_coefficient == 2:
                self.points_multiply_coefficient = 4

    def set_pass_counter(self, announcement):
        if announcement == "Pass":
            self.pass_counter += 1
        else:
            self.pass_counter = 0

    def get_pass_counter(self, connection=None):
        return self.pass_counter

    def get_loading_bar_info(self, connection):
        self.sockets_connected += 1
        if self.sockets_connected == 1:
            self.bar_counter += 1
        elif self.sockets_connected == 4:
            self.sockets_connected = 0
        index = self.get_index_of_player_by_connection(self.players_announcements_order, connection)
        dest_dict = {
            0: (WINDOW_WIDTH / 2, WINDOW_HEIGHT - WINDOW_WIDTH / 12),
            90: (WINDOW_WIDTH - WINDOW_WIDTH / 12, WINDOW_HEIGHT / 2),
            180: (WINDOW_WIDTH / 2, 0 + WINDOW_WIDTH / 12),
            270: (0 + WINDOW_WIDTH / 12, WINDOW_HEIGHT / 2)
        }

        return {
            "counter": self.bar_counter,
            "position": dest_dict[index * 90]
        }

    def check_announcements_order(self, connection=None):
        self.set_players_announcements_order_deque()
        player_on_move = self.players_announcements_order[0]
        connected_player = self.get_player_by_connection(self.players_announcements_order, connection)
        return player_on_move == connected_player
