import pygame

from card_sprites.sprites import WINDOW_WIDTH, WINDOW_HEIGHT

announce_string_matrix = [
    ("Clubs", "No Trumps"),
    ("Diamonds", "All Trumps"),
    ("Hearts", "Double"),
    ("Spades", "Redouble")
]


class AnnounceRect(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, width, height, image, rect_title, available):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.rect_title = rect_title
        self.image = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.available = available

    def blit(self, screen):
        screen.blit(self.image, self.rect)


class AnnounceModal(pygame.sprite.Group):
    folder_prefix = "announce_png/"


    def toggle_modal(self, available_dict):
        self.empty()
        margin = WINDOW_WIDTH / 5
        r = pygame.Rect(margin, margin, WINDOW_WIDTH - margin, WINDOW_HEIGHT - margin)
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
            AnnounceRect(r.left, r.top + r.height / 4 * 3, r.width / 2, r.height / 4, "announce_png/pass.png", "Pass",
                         True))

    def get_location_name(self, name):
        return self.folder_prefix + "_".join(name.lower().split(" ")) + ".png"

    def available_sprites(self):
        return filter(lambda sprite: sprite.available is True, self.sprites())
