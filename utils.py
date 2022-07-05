import pygame

from cards import Card
from variables import all_suits, all_ranks


def animation_frame(func):
    some_bool = True
    while some_bool:
        for event in pygame.event.get():
            func(event)


def create_deck():
    result = []
    for suit in all_suits:
        for rank in all_ranks:
            result.append(Card(suit, rank))
    return result
