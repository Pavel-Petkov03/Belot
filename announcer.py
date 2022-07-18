import time
from collections import deque

import pygame.time

from animation import Animation
from announcement_modal import AnnounceModal
from errors import EndGameError, AnnouncementsDoneError
from player import Bot
from variables import TEAMS


class Announcer(Animation):

    def __init__(self):
        super().__init__()
        self.available_announcements = {
            "Pass": 0,
            "Clubs": 1,
            "Diamonds": 2,
            "Hearts": 3,
            "Spades": 4,
            "No Trumps": 5,
            "All Trumps": 6,
        }
        self.game_announcer = None
        self.toggle_animation_done = False
        self.announce_modal = AnnounceModal()
        self.start = pygame.time.get_ticks()
        self.delay = 2000
        self.animation_started = False
        self.announce_rect_text = None
        self.pass_list = []  # if 4 passes or 1 announcement and 3 passes stop making announcements

    def add_to_pass_list(self):
        if self.announce_rect_text != "Pass":
            self.pass_list.clear()
            self.pass_list.append(self.announce_rect_text)
        elif len(list(filter(lambda announce: announce == "Pass", self.pass_list))) == 4:
            raise EndGameError("Not chosen game")
        else:
            # its pass
            self.pass_list.append(self.announce_rect_text)

    def make_announcements(self, players_deque):
        try:
            current_announcer = players_deque[0]
            if not isinstance(current_announcer, Bot):
                if self.toggle_animation_done:
                    self.make_animation_delay(current_announcer, players_deque)
                else:
                    self.announce_modal.toggle_modal(self.available_announcements)

            else:
                if not self.animation_started:
                    self.announce_rect_text = current_announcer.generate_random_announcements_algorythm(
                        self.available_announcements)
                    self.generate_available_announcements(current_announcer)
                    self.add_to_pass_list()  # adds the announcement
                    self.animation_started = True

                self.make_animation_delay(current_announcer, players_deque)
        except AnnouncementsDoneError:
            return True

    def generate_available_announcements(self, current_announcer):
        self.calculate_available_announcements(self.announce_rect_text, current_announcer)
        self.game_announcer = current_announcer

    def make_animation_delay(self, current_announcer, players_deque):
        if self.start + self.delay > pygame.time.get_ticks():
            self.toggle_rect(
                self.announce_rect_text,
                current_announcer.x_y_position_on_board,
                current_announcer.rotation_degrees_of_own_cards
            )
        else:
            self.make_shift(players_deque)
            self.animation_started = False
            self.toggle_animation_done = False
            self.start = pygame.time.get_ticks()
            if len(self.pass_list) == 4:
                raise AnnouncementsDoneError("Stop announcements")

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
