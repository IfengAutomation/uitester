from types import FunctionType


class CommandLineClient:
    """
    Command line helper

    Usage:
    @command(your_cmd_name)
    def func_name(*args):
        print('func arg={}'.format(args))

    Input command:
    >>your_cmd_name arg1 arg2
    Got from cmd:
    >>func arg='[arg1, args]'
    """
    commands = {}

    def command(self, *args, **kwargs):
        if len(args) < 0:
            raise ValueError('Should given 1 argument at least')

        if type(args[0]) is FunctionType:
            self.commands[args[0].__name__] = args[0]
            return
        elif type(args[0]) is str:

            def _wrapper(func):
                self.commands[args[0]] = func

            return _wrapper
        raise ValueError('argument should be str or function')

    def execute_cmd_line(self, cmd_line):
        cmd_and_agr_split_index = cmd_line.find(' ')
        if cmd_and_agr_split_index == -1:
            self.call(cmd_line)
        else:
            cmd_name = cmd_line[0:cmd_and_agr_split_index].strip()
            cmd_args = cmd_line[cmd_and_agr_split_index:].strip().split(' ')
            cmd_args = list(filter(lambda x: x != '', cmd_args))
            self.call(cmd_name, *cmd_args)

    def call(self, func_name, *args, **kwargs):
        if func_name in self.commands:
            self.commands[func_name](*args, **kwargs)

    def show_help(self, func_name=None):
        pass

