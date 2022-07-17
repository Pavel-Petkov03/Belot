from announcement_modal import AnnounceModal
from main import Bot, Animation
from variables import TEAMS


class Announcer:

    def __init__(self):
        self.animation = Animation()
        self.available_announcements = {
            "Pass": 0,
            "Spades": 1,
            "Diamonds": 2,
            "Hearts": 3,
            "Clubs": 4,
            "No trumps": 5,
            "All trumps": 6,
        }
        self.announced_game = None
        self.game_announcer = None
        self.toggle_animation_done = False
        self.announce_modal = AnnounceModal()

    def make_announcements(self, players_deque):
        current_announcer = players_deque[0]
        if not isinstance(current_announcer, Bot):
            self.announce_modal.toggle_modal()
            if self.toggle_animation_done:
                self.make_shift(players_deque)
                self.toggle_animation_done = False
        else:
            announce_result = current_announcer.generate_random_announcements_algorythm()
            self.animation.toggle_rect(announce_result, current_announcer.x_y_position_on_board,
                                       current_announcer.rotation_degrees_of_own_cards)
            self.calculate_available_announcements(announce_result, current_announcer)
            self.game_announcer = current_announcer
            self.announced_game = announce_result
            self.make_shift(players_deque)

    def calculate_available_announcements(self, announce, player):
        upper_announce_dict = {entry[0]: entry[1] for entry in list(self.available_announcements.items()) if
                               self.available_announcements[announce] > self.available_announcements[entry[0]]}
        for team in TEAMS:
            if not (player in team and self.game_announcer in team):
                if "double" in upper_announce_dict:
                    upper_announce_dict["Redouble"] = 8
                else:
                    upper_announce_dict["Double"] = 7
        upper_announce_dict["Pass"] = 0
        self.available_announcements = upper_announce_dict

    @staticmethod
    def make_shift(players_deque):
        players_deque.append(players_deque.popleft())
