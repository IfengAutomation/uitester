from types import FunctionType
import logging
import inspect
import sys
from os.path import dirname, abspath, pardir, join
from types import FunctionType


script_dir = dirname(abspath(__file__))
libs_dir = join(join(join(script_dir, pardir), pardir), 'libs')
print(script_dir, libs_dir)

sys.path.append(libs_dir)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


AS = 'as'
QUOTE = '"'
SPACE = ' '
COMMENT = '#'


def import_lib(*args, **kwargs):
    logger.debug('Import lib {}'.format(args))
    for lib_name in args:
        module = __import__(lib_name)
        for attr_name in dir(module):
            if attr_name.startswith('__'):
                continue
            attr = getattr(module, attr_name)
            if type(attr) is FunctionType:
                user_func[attr_name] = attr


def check(*args, **kwargs):
    logger.debug('Check {}'.format(args))


user_func = {'import': import_lib, 'check': check}
user_var = {}


class KWLine:
    """
    Keywords line
    """
    def __init__(self, line_number=0, items=None, var=None, raw=None):
        self.line_number = line_number
        self.items = items
        self.func = None
        self.var = var
        self.comment = False
        self.raw = raw

    def execute(self):
        if self.comment:
            return
        logger.debug('exec items {}'.format(self.items))
        if self.items[0] in user_func:
            user_func[self.items[0]](*self.items[1:])

    @classmethod
    def parse_line(cls, kw_line, line_number=0):
        line = cls(raw=kw_line, line_number=line_number)
        if kw_line.strip().startswith(COMMENT):
            line.comment = True
            return line

        kw_items = []
        cache = None
        in_quotation = False
        var = None
        for char in kw_line:
            if char == SPACE and not in_quotation and cache:
                kw_items.append(cache)
                cache = None
            elif char == QUOTE:
                in_quotation = not in_quotation
            else:
                if not cache:
                    cache = char
                else:
                    cache += char
        if cache:
            kw_items.append(cache)

        if in_quotation:
            raise ValueError('Missing quote. {}'.format(kw_line))

        if AS in kw_items:
            as_index = kw_items.index(AS)
            if as_index < (len(kw_items) - 2):
                raise ValueError('Keywords "as" should only set one variable')
            elif as_index == (len(kw_items) - 1):
                raise ValueError('Keywords "as" need one variable after it')
            else:
                var = kw_items[as_index + 1]
                kw_items = kw_items[:as_index]

        line.items = kw_items
        line.var = var
        return line


def start_test_cmd():

    while True:
        cmd_line = input('>>')
        if cmd_line == '':
            continue
        elif cmd_line == 'quit':
            break
        kw_line = KWLine.parse_line(cmd_line)
        if not kw_line.comment:
            kw_line.execute()

if __name__ == '__main__':
    start_test_cmd()
