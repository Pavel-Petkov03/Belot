import pygame

from main import WINDOW_WIDTH, WINDOW_HEIGHT, window
from utils import animation_frame


class AnnounceRect(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height, image, rect_title):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.rect_title = rect_title
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        window.blit(self.image, self.rect)


class AnnounceModal(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def toggle_modal(self):
        margin = 400
        r = pygame.Rect(margin, margin, WINDOW_WIDTH - margin, WINDOW_HEIGHT - margin)
        r.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        pygame.draw.rect(window, "white", r)
        for x_axis in range(2):
            for y_axis in range(4):
                middle_x = (r.width / 2)
                divided_y_axis = r.height / 16 * 3
                y_pos = r.top + divided_y_axis * y_axis
                x_pos = r.left + middle_x * x_axis
                rect = AnnounceRect(x_pos, y_pos, middle_x, divided_y_axis, "random.jpg", "")
                self.add(rect)
        self.add(AnnounceRect(r.left, r.top + r.height / 4 * 3, r.width, r.height / 4, "random.jpg", ""))

    def await_for_announcement(self):
        not_announced = True
        while not_announced:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    position = pygame.mouse.get_pos()
                    for sprite in self.sprites():
                        if sprite.image.get_rect().collidepoint(*position):
                            not_announced = False
