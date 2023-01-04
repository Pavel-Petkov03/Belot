import socket
import pickle

class Client:
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 1117
        self.host = socket.gethostbyname(socket.gethostname())
        self.address = (self.host, self.port,)

    def connect(self):
        self.connection.connect(self.address)

    def send(self, data):
        """
        the data will always be in stringified json format
        :param data:
        :return:
        """
        try:
            data = pickle.dumps(data)
            self.connection.send(data)
            reply = self.connection.recv(2048)
            reply = pickle.loads(reply)
            print(reply)
            return reply
        except socket.error as e:
            return str(e)

