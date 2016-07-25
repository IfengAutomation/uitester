import sys
import logging
from uitester.cmd_client import CmdClient
from uitester import ui_client

logging.basicConfig(level=logging.DEBUG)


def start_ui_mode():
    logging.debug('Start with ui mode')
    ui_client.start_ui()


def start_cmd_mode():
    logging.debug('Start with cmd mode')
    CmdClient().start()


def start():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'cmd':
            start_cmd_mode()
            return
    start_ui_mode()


if __name__ == '__main__':
    start()

