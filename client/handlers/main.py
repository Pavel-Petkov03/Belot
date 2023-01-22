import pygame


from client.handlers.announcements import AnnouncementsClient
from client.handlers.board import BoardClient
from client.handlers.deal_cards import DealCardsClient
from client.handlers.preload import PreloadClient


class MainClient(PreloadClient, AnnouncementsClient, DealCardsClient, BoardClient):
    def run(self):

        running = True

        while running:
            self.blit_background()
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    running = False

            self.dispatch(event_list)
            pygame.display.flip()
