import pygame


class TimeRemainingBar:
    def __init__(self):
        self.bar_size = (200, 20)
        self.border_color = (0, 0, 0)
        self.bar_color = (0, 128, 0)
        self.max_bar_capacity = 350

    def draw(self, screen, progress, bar_position):
        pygame.draw.rect(screen, self.border_color, (*bar_position, *self.bar_size), 1)
        inner_pos = (bar_position[0] + 3, bar_position[1] + 3)
        inner_size = (self.bar_size[0] - 6 * progress, self.bar_size[1] - 6)
        pygame.draw.rect(screen, self.bar_color, (*inner_pos, *inner_size))







