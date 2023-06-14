from utils.helper_funcs.get_screen_size import get_screen_size

suits = ["clubs", "diamonds", "hearts", "spades"]
ranks = ["7", "8", "9", "10", "ace", "queen", "jack", "king"]

announce_string_matrix = [
    ("Clubs", "No Trumps"),
    ("Diamonds", "All Trumps"),
    ("Hearts", "Double"),
    ("Spades", "Redouble")
]

SCREENSIZE = get_screen_size()
WINDOW_WIDTH, WINDOW_HEIGHT = SCREENSIZE

DESTINATION_DICT = {
    0: (WINDOW_WIDTH / 2, WINDOW_HEIGHT - WINDOW_WIDTH / 12),
    90: (WINDOW_WIDTH - WINDOW_WIDTH / 12, WINDOW_HEIGHT / 2),
    180: (WINDOW_WIDTH / 2, 0 + WINDOW_WIDTH / 12),
    270: (0 + WINDOW_WIDTH / 12, WINDOW_HEIGHT / 2)
}

