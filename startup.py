import sys
import logging
from uitester import ui_client

logger = logging.getLogger('UiTester')
logger.setLevel(logging.DEBUG)


def start():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'cmd':
            print('Unsupported cmd')
            return
    logger.debug('Start with ui mode')
    ui_client.start()


if __name__ == '__main__':
    start()

