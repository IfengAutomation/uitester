from types import FunctionType
import logging
import inspect
import sys
from os.path import dirname, abspath, pardir, join
from types import FunctionType, MethodType
from uitester.remote_proxy.proxy import CommonProxy


script_dir = dirname(abspath(__file__))
libs_dir = join(join(join(script_dir, pardir), pardir), 'libs')
sys.path.append(libs_dir)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.WARNING)


class KWCore:
    AS = 'as'
    QUOTE = '"'
    SPACE = ' '
    COMMENT = '#'
    DOT = '.'

    def __init__(self, context):
        self.context = context
        self.user_var = {}
        self.default_func = {'import': self.kw_import, 'check': self.kw_check, 'print': self.kw_print}
        self.user_func = {**self.default_func}
        self.parsed_line = []
        self.line_count = 0
        context.register(self._kw_core_receiver)
        self.running = False
        self.real_prc_funcs = {}
        self.proxy = CommonProxy(context)

    def _kw_core_receiver(self, msg_type, msg=None):
        if msg_type == 'stop_test':
            self.running = False

    def _execute_line(self, kw_line):
        if kw_line.comment:
            return
        elif kw_line.items[0] == 'import':
            return
        logger.debug('exec items {}'.format(kw_line.items))

        res = self.user_func[kw_line.items[0]](*kw_line.items[1:])
        if kw_line.var:
            self.user_var[kw_line.var] = res

    def parse_line(self, line):
        # set line number
        self.line_count += 1
        if len(line) == 0:
            return
        # parse line to kw line
        kw_line = self._parse_line(line, line_number=self.line_count)
        if kw_line.comment:
            return

        func = kw_line.items[0]

        if func == 'import':
            # pre import lib
            self.default_func['import'](*kw_line.items[1:])

        if func not in self.user_func and func not in self.user_var:
            raise ValueError('Define not found {}'.format(func), kw_line.line_number)

        if kw_line.var:
            self.user_var[kw_line.var] = None

        # add kw line to cache
        self.parsed_line.append(kw_line)

    def execute(self):
        self.running = True
        # run all kw line in cache
        for line in self.parsed_line:
            if not self.running:
                break
            self._execute_line(line)
        self.running = False

    def release(self):
        # release all var and func
        self.user_var.clear()
        self.user_func.clear()
        self.user_func = {**self.default_func}
        self.parsed_line = []
        self.context.unregister(self._kw_core_receiver)

    def _parse_line(self, kw_line, line_number=0):
        line = KWLine(raw=kw_line, line_number=line_number)
        if kw_line.strip().startswith(self.COMMENT):
            line.comment = True
            return line

        kw_items = []
        cache = None
        in_quotation = False
        var = None
        for char in kw_line:
            if char == self.SPACE and not in_quotation and cache:
                kw_items.append(cache)
                cache = None
            elif char == self.QUOTE:
                in_quotation = not in_quotation
            else:
                if not cache:
                    cache = char
                else:
                    cache += char
        if cache:
            kw_items.append(cache)

        if in_quotation:
            raise ValueError('Missing quote. {}'.format(kw_line), line_number)

        if self.AS in kw_items:
            as_index = kw_items.index(self.AS)
            if as_index < (len(kw_items) - 2):
                raise ValueError('Keywords "as" should only set one variable', line_number)
            elif as_index == (len(kw_items) - 1):
                raise ValueError('Keywords "as" need one variable after it', line_number)
            else:
                var = kw_items[as_index + 1]
                kw_items = kw_items[:as_index]

        line.items = kw_items
        line.var = var
        return line

    def get_value(self, word):
        if word in self.user_var:
            return self.user_var[word]

        dot_count = word.count(self.DOT)
        if dot_count > 1:
            raise ValueError('Unsupported usage {}'.format(word))
        elif dot_count == 1:
            var_name, attr_name = word.split(self.DOT)
            if var_name in self.user_var:
                var = self.user_var[var_name]
                if hasattr(var, attr_name):
                    return getattr(var, attr_name)
                else:
                    raise ValueError('{} not has attr {}'.format(var_name, attr_name))
            else:
                raise ValueError('Var {} not found'.format(var_name))
        else:
            return word

    def kw_import(self, *args, **kwargs):
        """
        Import python lib from .libs dir
        After import, you can use functions in py lib by write function name.
        ------------
        e.g.:
        import custom_lib
        test_str
        ------------
        line 1. Import python lib witch named custom_lib in libs dir.
        line 2. call function test_str() in custom_lib.

        :param args:
        :param kwargs:
        :return:
        """
        logger.debug('Import kw lib {}'.format(args))
        for lib_name in args:
            module = __import__(lib_name)
            for attr_name in dir(module):
                clazz = getattr(module, attr_name)
                if not inspect.isclass(clazz):
                    continue

                user_kw_instance = clazz()
                self.attach_rpc_funcs(user_kw_instance)
                self.load_funcs(user_kw_instance)

    def attach_rpc_funcs(self, kw_instance):
        for attr_name in dir(self.proxy):
            if attr_name.startswith('_'):
                continue
            rpc_func = getattr(self.proxy, attr_name)
            if type(rpc_func) is not MethodType:
                continue
            setattr(kw_instance, attr_name, rpc_func)

    def load_funcs(self, kw_instance):
        for attr_name in dir(kw_instance):
            attr = getattr(kw_instance, attr_name)
            if type(attr) is MethodType:
                self.user_func[attr_name] = attr

    def kw_check(self, *args, **kwargs):
        """
        Assert if arg1 equals arg2
        e.g. :
        check some_view.text some_text
        if this view's text is not some_text, then this case will be record as failed
        :param args:
        :return:
        """
        logger.debug('Check {}'.format(args))
        if len(args) < 2:
            raise ValueError('Check need 2 arguments. but {} given'.format(len(args)))

        assert self.get_value(args[0]) == self.get_value(args[1])

    def kw_print(self, *args, **kwargs):
        """
        Print var
        :param args:
        :return:
        """
        output = []
        # rm self from *args
        args = args[1:]
        for arg in args:
            if arg in self.user_func:
                output.append('<KW:{}>'.format(arg))
            elif arg in self.user_var:
                output.append('<Var:{}={}>'.format(arg, self.user_var[arg]))
            elif arg.count(self.DOT) == 1:
                var_name, attr = arg.split(self.DOT)
                if var_name in self.user_var:
                    var = self.user_var[var_name]
                    if hasattr(var, attr):
                        attr_value = getattr(var, attr)
                        output.append(attr_value)
                    else:
                        output.append('<Var:{} not found attr {}>'.format(var, attr))
                else:
                    output.append('<Var:{} not found>'.format(var))
            else:
                output.append(arg)
        print(*output)
        return output


class KWLine:
    """
    Keywords line
    """
    def __init__(self, line_number=0, items=None, var=None, raw=None):
        self.line_number = line_number
        self.items = items
        self.var = var
        self.comment = False
        self.raw = raw
