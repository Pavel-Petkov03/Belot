import pygame


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
