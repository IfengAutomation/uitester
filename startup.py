import sys
import logging
from uitester import cmd_client
from uitester import ui_client

logging.basicConfig(level=logging.DEBUG)


def start():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'cmd':
            logging.debug('Start with cmd mode')
            cmd_client.start()
            return\
    logging.debug('Start with ui mode')
    ui_client.start()


if __name__ == '__main__':
    start()

