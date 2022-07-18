import pygame

from cards import Deck, BoardCards, CardSprite
from player import Bot
from variables import window, WINDOW_WIDTH, WINDOW_HEIGHT


class CardTable:
    def __init__(self):
        self.animation_started = False
        self.board_cards = BoardCards()
        self.sprites = pygame.sprite.Group()
        self.start = pygame.time.get_ticks()
        self.delay = 2000

    def main(self, players_deque):
        current_giver = players_deque[0]
        if isinstance(current_giver, Bot):
            if not self.animation_started:
                card = current_giver.generate_choose_card_algorythm()
                current_giver.cards.remove(card)
                self.sprites.add(CardSprite(
                    card.suit,
                    card.rank,
                    WINDOW_WIDTH / 2,
                    WINDOW_HEIGHT / 2,
                    current_giver.rotation_degrees_of_own_cards))
                self.animation_started = True
                self.start = pygame.time.get_ticks()
            else:
                if not (self.start + self.delay > pygame.time.get_ticks()):
                    players_deque.append(players_deque.popleft())
                    self.animation_started = False

            self.sprites.update()

