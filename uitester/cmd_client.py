from colorama import Fore, Back, Style
from uitester.tester import Tester
from uitester.command_line import CommandLineClient

cmd = CommandLineClient()
tester = Tester()


@cmd.command('help')
def c_help(*args):
    print('Command help args={}'.format(args))


@cmd.command('run')
def c_start_test():
    # TODO
    tester.execute_script()


@cmd.command('devices')
def c_devices():
    # TODO
    tester.devices()


@cmd.command('kw')
def c_execute_kw_line(kw_name, *args):
    print('Command kw name={} args={}'.format(kw_name, args))


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
