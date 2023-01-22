import pygame

from sprites.announcements.announce_rect import AnnounceRect
from utils.variables.contants import WINDOW_WIDTH, WINDOW_HEIGHT, announce_string_matrix


class AnnounceModal(pygame.sprite.Group):
    folder_prefix = "images/announce_png/"

    def __init__(self):
        pygame.sprite.Group.__init__(self, [])
        self.announced_game = None
        self.is_clicked_available_field = False

    def load(self, available_dict):
        self.empty()
        r = pygame.Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4)
        r.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        for x_axis in range(2):
            for y_axis in range(4):
                middle_x = r.width / 4
                divided_y_axis = r.height / 16 * 3
                y_pos = r.top + divided_y_axis * y_axis
                x_pos = r.left + middle_x * x_axis
                announce_string = announce_string_matrix[y_axis][x_axis]

                available = True if announce_string in available_dict else False
                rect = AnnounceRect(x_pos, y_pos, middle_x, divided_y_axis, self.get_location_name(announce_string),
                                    announce_string, available)
                self.add(rect)
        self.add(
            AnnounceRect(r.left, r.top + r.height / 4 * 3, r.width / 2, r.height / 4, "images/announce_png/pass.png", "Pass",
                         True))

    def get_location_name(self, name):
        return self.folder_prefix + "_".join(name.lower().split(" ")) + ".png"

    def click_event_listener(self, event_list):
        if self.is_clicked_available_field:
            return True
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                for sprite in self.sprites():
                    if self.is_available(sprite) and sprite.rect.collidepoint(*pos):
                        self.announced_game = sprite.rect_title
                        self.is_clicked_available_field = True
        return False

    @staticmethod
    def is_available(sprite):
        return sprite.available
