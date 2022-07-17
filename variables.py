import pygame

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