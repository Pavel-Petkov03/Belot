class Team:

    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player

    def __contains__(self, player):
        return player in (self.first_player, self.second_player)
