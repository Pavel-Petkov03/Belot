from client.connectors.base import ClientConnector


class DealCardsClientConnector(ClientConnector):
    def socket_deal_cards(self, wanted_cards):
        return self.send("deal_cards", params={"wanted_cards": wanted_cards})