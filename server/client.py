import socket
import pickle
import struct
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
            size_in_4_bytes = self.connection.recv(4)  # get only 4 bytes
            size = struct.unpack('I', size_in_4_bytes)
            size = size[0]
            reply = self.connection.recv(size)
            reply = pickle.loads(reply)
            print(reply)
            return reply
        except socket.error as e:
            return str(e)

