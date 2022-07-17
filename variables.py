from collections import deque

import pygame

from player import Bot, Player
from team import Team

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
FPS = 30
DISTANCE_BETWEEN_PLAYER_AND_WINDOW = 100
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
all_suits = ["clubs", "hearts", "diamonds", "spades"]
all_ranks = ["7", "8", "9", "10", "J", "Q", "K", "A"]

announce_string_matrix = [
    ("Clubs", "No Trumps"),
    ("Diamonds", "All Trumps"),
    ("Hearts", "Double"),
    ("Spades", "Redouble")
]

player_1 = Bot((WINDOW_WIDTH - DISTANCE_BETWEEN_PLAYER_AND_WINDOW, WINDOW_HEIGHT / 2), 270)
player_2 = Bot((WINDOW_WIDTH / 2, DISTANCE_BETWEEN_PLAYER_AND_WINDOW), 0)
player_3 = Bot((DISTANCE_BETWEEN_PLAYER_AND_WINDOW, WINDOW_HEIGHT / 2), 90)
player_4 = Player((WINDOW_WIDTH / 2, WINDOW_HEIGHT - DISTANCE_BETWEEN_PLAYER_AND_WINDOW), 0)

team_1 = Team(player_1, player_3)
team_2 = Team(player_2, player_4)

TEAMS = (team_1, team_2)
PLAYERS_DEQUE = deque(
    [player_1,
     player_2,
     player_3,
     player_4]
)
