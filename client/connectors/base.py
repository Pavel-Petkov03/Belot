class ClientConnector:
    def __init__(self):
        self.current_player = None

    def send(self, action, params=None):
        if params:
            return self.current_player.net.send({
                "action": action,
                "params": params
            })
        return self.current_player.net.send({
            "action": action,
        })