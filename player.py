import random


class Player:
    def __init__(self, x_y_pos, rotation_degrees):
        self.cards = []
        self.x_y_position_on_board = x_y_pos
        self.rotation_degrees_of_own_cards = rotation_degrees


class Bot(Player):
    def generate_random_announcements_algorythm(self, available_announcements):
        # this functionality will be made later
        return random.choice(list(available_announcements.keys()))

    def generate_choose_card_algorythm(self, available_cards):
        # this functionality will be made later
        return random.choice(self.cards)
