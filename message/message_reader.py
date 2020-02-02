from message import handshake
import message.message

import socket


class Message_Reader:

    def __init__(self, s: socket.socket):
        self.s = s

    def read(self):
        try:
            # Read Handshake
            handshake_data = self.s.recv(handshake.LENGTH_V1)
            # validate handshake

            while True:
                self.s.recv(message.message.LEN)
                # get message length
                # data = self.s.recv(message_length)
                # message.message.Message.handle_data(data)

        except Exception as e:
            print(e)
