from colorama import Fore, Back, Style

from uitester.tester import Tester
from uitester.command_line import CommandLineClient

cmd = CommandLineClient()
tester = Tester()


@cmd.command('help')
def c_help(*args):
    print(Fore.LIGHTCYAN_EX + 'Command help args={}'.format(args))
    print("command |      description          |             usage")
    print("---------------------------------------------------------------------")
    commands = {"run", "devices", "kw"}
    for command in commands:
        if command == 'run':
            print("run     |   run cases               |       run file_name")
        elif command == 'devices':
            print("devices |   list all target devices |       devices")
        elif command == 'kw':
            print("kw      |   run case use kw         |       kw kw_name args")


@cmd.command('run')
def c_start_test(file_name):
    print(Fore.LIGHTCYAN_EX + 'Command run file_name={}'.format(file_name))
    tester.execute_script(file_name)


@cmd.command('devices')
def c_devices():
    devices = tester.devices()
    if len(devices) > 0:
        for device in devices:
            print(Fore.LIGHTCYAN_EX + 'List of devices registered:')
            print(device + "   device")
    else:
        print(Fore.LIGHTCYAN_EX + 'There is no registered devices.')


@cmd.command('kw')
def c_execute_kw_line(kw_name, *args):
    print(Fore.LIGHTCYAN_EX + 'Command kw name={} args={}'.format(kw_name, args))
    tester.execute_line(kw_name, *args)


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
