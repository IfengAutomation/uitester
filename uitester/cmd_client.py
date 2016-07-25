from colorama import Fore, Back, Style
from uitester.tester import Tester


class CmdClient:
    def __init__(self):
        self.running = True
        self.commands = {}
        self.tester = Tester()

    def start(self):
        self.tester.start()
        while self.running:
            self.read_input()

    def read_input(self):
        cmd_line = input(Fore.GREEN+'>>')
        print('commands {}'.format(self.commands))


    def quit(self):
        if self.tester:
            self.tester.stop()
        self.running = False
