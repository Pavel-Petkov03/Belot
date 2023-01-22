import pygame

from client.player import PlayerClient
from sprites.preload_sprites.entry_text_box import EntryTextBox
from sprites.preload_sprites.text_box_base import TextBox
from utils.variables.contants import WINDOW_HEIGHT, WINDOW_WIDTH


class AllBoxes(pygame.sprite.Group):

    def __init__(self, game_state):
        super().__init__([])
        self.game_state = game_state
        font = "Sans serif"
        padding = WINDOW_HEIGHT / 8
        x = WINDOW_WIDTH / 2 - WINDOW_WIDTH / 8
        y = 100
        width = WINDOW_WIDTH / 16
        self.header = TextBox(x, y, width, 100, font, 60, text="Belot Local", backcolor=(95, 35, 35), )
        self.username_header = TextBox(x, y + padding, width, 100, font, 30, text="Type Username",
                                       backcolor=(78, 57, 57), )
        self.username_box = EntryTextBox(x, y + padding * 2, width, 100, font, 30, text="", backcolor=(0, 0, 0))
        self.join_server = TextBox(x, y + padding * 3, width, 100, font, 50, text="Join Server", backcolor=(78, 57, 57),
                                   text_box_type="button", event_func=self.onclick)

        self.add(*[
            self.header, self.username_header, self.username_box, self.join_server
        ])

    def onclick(self):
        username = self.username_box.text
        self.game_state.current_state = "render_waiting_screen"
        player = PlayerClient(username)
        player.connect()
        self.game_state.current_player = player
