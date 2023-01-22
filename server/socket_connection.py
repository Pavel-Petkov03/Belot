import socket
from _thread import start_new_thread
import pickle
import struct

from server.game_engine.main_engine import MainEngine


class Server:
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = socket.gethostbyname(socket.gethostname())
        self.port = 1117
        self.engine = MainEngine()
        self.run()

    def run(self):
        self.bind()
        self.listen()
        while True:
            client_connection, addr = self.connection.accept()
            print("Connected to: ", addr)
            start_new_thread(self.thread, (client_connection, addr))

    def bind(self):
        try:
            self.connection.bind((self.server_ip, self.port))
        except socket.error as e:
            print(str(e))

    def listen(self):
        self.connection.listen()
        print("[SERVER IS LISTENING...]")

    def thread(self, conn: socket.SocketType, address):
        while True:
            data = conn.recv(10000000)
            if not data:
                print("Disconnected")
                conn.send(str.encode("THE CONNECTION HAS BEEN STOPPED"))
                self.engine.remove_player_on_disconnect(conn)
                break

            reply = pickle.loads(data)
            reply = self.engine.get_info(reply, conn)
            data = pickle.dumps(reply)
            size = len(data)
            size_in_4_bytes = struct.pack("I", size)
            conn.send(size_in_4_bytes)
            conn.send(data)
        conn.close()


s = Server()
