import pygame


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
