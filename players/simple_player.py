class SimplePlayer:
    def __init__(self, name, connection):
        self.name = name
        self.team = None
        self.cards = []
        self.connection = connection

    def __getstate__(self):
        return {
            "name": self.name,
            "team": self.team,
            "cards": self.cards,
        }

