from player import Bot


class CardTable:
    def __init__(self):
        self.card_given = False

    def main(self, players_deque):
        if not self.card_given:
            current_giver = players_deque[0]
            if isinstance(current_giver, Bot):
                card = current_giver.generate_choose_card_algorythm(1)
                