from client.connectors.deal_cards import DealCardsClientConnector
from client.handlers.base import Game


class DealCardsClient(Game, DealCardsClientConnector):
    FIRST_ROW_CARDS_MAX_LEN = 20
    SECOND_ROW_CARDS_MAX_LEN = 32

    def render_game(self, event_list):
        if len(self.cards) == self.SECOND_ROW_CARDS_MAX_LEN:
            self.set_current_state("gameplay")
            return
        elif len(self.cards) == self.FIRST_ROW_CARDS_MAX_LEN and not self.announcements_done:
            self.set_current_state("announcements")
            return
        response = self.socket_deal_cards(self.calculate_wanted_cards())
        all_cards = response["data"]
        self.add_cards(all_cards)
        self.set_current_state("animation")

    def add_cards(self, all_cards):
        for card in all_cards:
            key = f'suit:{card.suit}rank:{card.rank}'
            if key not in self.cards:
                self.cards[key] = card
            else:
                self.cards[key].rect.center = card.destination_pos

    def calculate_wanted_cards(self):
        if len(self.cards) < 12 or len(self.cards) >= 20:
            return 3
        return 2

    def animation(self, event_list):
        for card in self.cards.values():
            if not card.given:
                if card.rect is None:
                    card.load_image()
                card.calculate_destination_of_movement()
                if card.on_wanted_position():
                    card.given = True
                    self.set_current_state("render_game")
            card.blit(self.screen)