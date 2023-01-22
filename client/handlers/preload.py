from client.connectors.preload import PreloadClientConnector
from client.handlers.base import Game
from sprites.preload_sprites.all_text_boxes import AllBoxes
from sprites.preload_sprites.text_box_base import TextBox


class TextBoxesGroup:
    pass


class PreloadClient(Game, PreloadClientConnector):
    MAX_PLAYERS = 4

    def __init__(self):
        super().__init__()
        self.all_start_boxes = AllBoxes(self)

    def render_start_dialog(self, event_list):
        self.all_start_boxes.update(event_list)
        self.all_start_boxes.draw(self.screen)

    def render_waiting_screen(self, event_list):
        reply = self.socket_get_players()

        current_players_length = len(reply["data"])
        if current_players_length == self.MAX_PLAYERS:
            self.set_current_state("render_game")
            return

        text_box = TextBox(100, 100, 200, 200, font="Sans Serif", font_size=50, backcolor="green",
                           text=f"Waiting for other {4 - current_players_length} to join", )
        text_box.update(event_list)
        text_box.draw(self.screen)
