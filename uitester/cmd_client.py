from colorama import Fore, Back, Style


class CmdClient:

    def start(self):
        while True:
            self.read_input()

    def read_input(self):
        cmd_line = input(Fore.GREEN+'>>')
