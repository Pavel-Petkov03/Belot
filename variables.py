import pygame

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FPS = 30
DISTANCE_BETWEEN_PLAYER_AND_WINDOW = 100
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
all_suits = ["clubs", "hearts", "diamonds", "spades"]
all_ranks = ["7", "8", "9", "10", "J", "Q", "K", "A"]