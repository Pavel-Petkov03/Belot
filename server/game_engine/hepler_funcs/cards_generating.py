from utils.variables.contants import suits, ranks


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


def generate_cards():
    cards = []
    for suit in suits:
        for rank in ranks:
            card = Card(rank, suit)
            cards.append(card)
    return cards
