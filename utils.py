import pygame

from cards import Card
from variables import all_suits, all_ranks



def create_deck():
    result = []
    for suit in all_suits:
        for rank in all_ranks:
            result.append(Card(suit, rank))
    return result




