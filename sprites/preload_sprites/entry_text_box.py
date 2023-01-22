import pygame

from sprites.entry_text_box.text_box_base import TextBox


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
                self.render_text((5, 5))
