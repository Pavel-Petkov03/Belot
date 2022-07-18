import time

import pygame.time

from animation import Animation
from announcement_modal import AnnounceModal
from player import Bot
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
        self.game_announcer = None
        self.toggle_animation_done = False
        self.announce_modal = AnnounceModal()
        self.start = time.time()
        self.delay = 1
        self.animation_started = False
        self.announce_rect_text = None
        self.pass_list = []  # if 4 passes or 1 announcement and 3 passes stop make announcements

    def add_to_pass_list(self, value):
        if value != "Pass":
            self.pass_list.clear()
            self.pass_list.append(value)

        if value == "Pass" and self.pass_list[0] == "Pass":
            pass

    def make_announcements(self, players_deque):
        current_announcer = players_deque[0]
        if not isinstance(current_announcer, Bot):
            self.announce_modal.toggle_modal(self.available_announcements)
            if self.toggle_animation_done:
                self.make_shift(players_deque)
                self.toggle_animation_done = False
        else:
            if not self.animation_started:
                self.announce_rect_text = current_announcer.generate_random_announcements_algorythm(
                    self.available_announcements)
                self.calculate_available_announcements(self.announce_rect_text, current_announcer)
                self.game_announcer = current_announcer
                self.animation_started = True

            if self.start + self.delay > time.time():
                self.animation.toggle_rect(self.announce_rect_text,
                                           current_announcer.x_y_position_on_board,
                                           current_announcer.rotation_degrees_of_own_cards)
            else:
                self.make_shift(players_deque)
                self.animation_started = False
                self.start = time.time()

    def calculate_available_announcements(self, announce, player):
        if announce == "Pass":
            return
        upper_announce_dict = {entry[0]: entry[1] for entry in list(self.available_announcements.items()) if
                               self.available_announcements[announce] < self.available_announcements[entry[0]]}
        for team in TEAMS:
            if player in team and self.game_announcer in team:
                if "Double" in upper_announce_dict:
                    upper_announce_dict["Redouble"] = 8
                else:
                    upper_announce_dict["Double"] = 7
        upper_announce_dict["Pass"] = 0
        self.available_announcements = upper_announce_dict

    @staticmethod
    def make_shift(players_deque):
        players_deque.append(players_deque.popleft())
