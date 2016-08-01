from colorama import Fore, Back, Style

from uitester.remote_proxy.proxy import CommonProxy
from uitester.tester import Tester
from uitester.command_line import CommandLineClient

cmd = CommandLineClient()
tester = Tester()


@cmd.command('help')
def c_help(*args):
    print('Command help args={}'.format(args))
    print("command |      description          |             usage")
    print("---------------------------------------------------------------------")
    commands = {"run", "devices", "kw"}
    for command in commands:
        if command == 'run':
            print("run     |   run cases               |       run CaseName/tag/CaseId")
        elif command == 'devices':
            print("devices |   list all target devices |       devices")
        elif command == 'kw':
            print("kw      |   run case use kw         |       kw kw_name args")


@cmd.command('run')
def c_start_test():
    # TODO
    tester.execute_script()


@cmd.command('devices')
def c_devices():
    devices = tester.devices()
    for device in devices:
        print('List of devices registered:')
        print(device + "   device")


@cmd.command('kw')
def c_execute_kw_line(kw_name, *args):
    proxy = CommonProxy()
    print('Command kw name={} args={}'.format(kw_name, args))
    for (id, device) in tester.devices().items():
        print("device id: {}".format(id))
        proxy.target_devices.append(device)
    if kw_name == "StartApp":
        proxy.start_app(args[0])


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
