import pygame

import utils
from players.player import Player

SCREENSIZE = utils.get_screen_size()


class TextBoxesGroup(pygame.sprite.Group):
    def update(self, *args, **kwargs) -> None:
        for sprite in self.sprites():
            sprite.update(*args, **kwargs)

    def draw(self, window):
        for sprite in self.sprites():
            sprite.draw(window)


class TextBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, font=None, font_size=None, backcolor=None, text="", text_box_type="text",
                 event_func=None):
        super().__init__()
        self.color = "white"
        self.text_box_type = text_box_type
        self.backcolor = backcolor
        self.pos = (x, y)
        self.width = w
        self.height = h
        self.font = pygame.font.SysFont(font, font_size)
        self.text = text
        self.image = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.render_text()
        self.event_func = event_func

    def draw(self, window):
        pygame.draw.rect(self.image, self.color, self.rect)
        window.blit(self.image, self.pos)

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width() + 10), t_surf.get_height() + 10),
                                    pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list, **kwargs):
        if self.text_box_type == "button":
            for event in event_list:
                if self.rect.collidepoint(*pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.type == pygame.MOUSEBUTTONDOWN)
                    self.event_func()


class EntryTextBox(TextBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = False

    def update(self, event_list, **kwargs):
        super().update(event_list)
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) <= 10:
                        self.text += event.unicode
                self.render_text()


class AllBoxes:
    def __init__(self, game_state):
        self.game_state = game_state
        font = "Sans serif"
        padding = SCREENSIZE[1] / 8
        x = SCREENSIZE[0] / 2 - SCREENSIZE[0] / 8
        y = 100
        width = SCREENSIZE[0] / 16
        self.header = TextBox(x, y, width, 100, font, 60, text="Belot Local", backcolor=(95, 35, 35), )
        self.username_header = TextBox(x, y + padding, width, 100, font, 30, text="Type Username",
                                       backcolor=(78, 57, 57), )
        self.username_box = EntryTextBox(x, y + padding * 2, width, 100, font, 30, text="", backcolor=(0, 0, 0))
        self.join_server = TextBox(x, y + padding * 3, width, 100, font, 50, text="Join Server", backcolor=(78, 57, 57),
                                   text_box_type="button", event_func=self.onclick)

        self.all_boxes = [
            self.header, self.username_header, self.username_box, self.join_server
        ]

    def onclick(self):
        username = self.username_box.text
        self.game_state.current_state = "render_waiting_screen"
        player = Player(username)
        player.connect()
        self.game_state.current_player = player


