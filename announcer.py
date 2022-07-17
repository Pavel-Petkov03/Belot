from announcement_modal import AnnounceModal
from main import Bot, Animation


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
            self.make_shift(players_deque)

    def set_announced_game(self, new_announce):
        if self.available_announcements[new_announce] > self.available_announcements[self.announced_game]:
            self.announced_game = new_announce



    @staticmethod
    def make_shift(players_deque):
        players_deque.append(players_deque.popleft())
