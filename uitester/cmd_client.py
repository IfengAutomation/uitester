from colorama import Fore, Back, Style
from uitester.tester import Tester

commands = []


def command(func):
    print('register cmd {}'.format(func))
    commands.append(func)


@command
def hello():
    print('hello')


@command
def world():
    print('world')


def execute_cmd(name, *args):
    print('exec {} args={}'.format(name, args))


def start():
    Tester().start()
    while True:
        cmd_line = input(Fore.GREEN + '>>').strip()
        if cmd_line == '':
            continue
        if cmd_line == 'quit':
            break

        cmd_and_agr_split_index = cmd_line.find(' ')
        if cmd_and_agr_split_index == -1:
            execute_cmd(cmd_line)
        else:
            cmd_name = cmd_line[0:cmd_and_agr_split_index].strip()
            cmd_args = cmd_line[cmd_and_agr_split_index:].strip().split(' ')
            cmd_args = list(filter(lambda x: x != '', cmd_args))
            execute_cmd(cmd_name, cmd_args)


if __name__ == '__main__':
    start()
