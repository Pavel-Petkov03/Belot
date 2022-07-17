
class Player:
    def __init__(self, x_y_pos, rotation_degrees):
        self.cards = []
        self.x_y_position_on_board = x_y_pos
        self.rotation_degrees_of_own_cards = rotation_degrees


class Bot(Player):
    def generate_random_announcements_algorythm(self):
        # this functionality will be made later
        return "Pass"