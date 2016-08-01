from colorama import Fore, Back, Style
from uitester.tester import Tester
from uitester.command_line import CommandLineClient

cmd = CommandLineClient()
tester = Tester()


@cmd.command('help')
def c_help(*args):
    pass


@cmd.command('run')
def c_start_test():
    # TODO
    tester.execute_script()


@cmd.command('devices')
def c_devices():
    # TODO
    tester.devices()


def start():
    tester.start()
    while True:
        cmd_line = input(Fore.GREEN + '>>').strip()
        if cmd_line == '':
            continue
        if cmd_line == 'quit':
            break

        cmd.execute_cmd_line(cmd_line)


if __name__ == '__main__':
    start()
