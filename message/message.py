from typing import Dict

from message.handshake import Handshake

LEN = 4


def init_message_handlers() -> Dict[int, ()]:
    return {
        1: Handshake.__init__
    }


class Message:
    messageHandler = init_message_handlers()

    def handle(self):
        raise NotImplementedError

    def get_id(self) -> int:
        raise NotImplementedError

    @staticmethod
    def handle_data(data: bytes):
        # get message id from data
        # call the respective handler
        pass
