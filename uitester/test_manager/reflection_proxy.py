import logging
from uitester.test_manager import context

logger = logging.getLogger('Tester')

STRING = '01'
INT = '02'
CLASS = '03'
OBJECT = '04'
FLOAT = '05'
BOOL = '06'


class RemoteObject:
    """
    Attr list:

    remote_type

    =Object= ----------
    hash
    class_name

    =View= ---------
    resource_id
    package_name

    =TextView= ----------
    text

    """
    def __init__(self):
        self.remote_type = OBJECT

    @classmethod
    def from_float(cls, float_input):
        obj = cls()
        obj.remote_type = FLOAT
        obj.value = float_input
        return obj

    @classmethod
    def from_dict(cls, attr_dict):
        obj = cls()
        obj.__dict__ = attr_dict
        obj.remote_type = OBJECT
        return obj

    @classmethod
    def from_class_name(cls, class_name):
        obj = cls()
        obj.class_name = class_name
        obj.remote_type = CLASS
        return obj


def _make_arg(arg):
    arg_type = type(arg)
    if arg_type == str:
        return STRING+arg
    elif arg_type == int:
        return INT+str(arg)
    elif arg_type == bool:
        return BOOL+str(arg)
    elif hasattr(arg, 'remote_type') and arg.remote_type == OBJECT:
        return OBJECT+str(arg.hash)+':'+arg.class_name
    elif hasattr(arg, 'remote_type') and arg.remote_type == CLASS:
        return CLASS+str(arg.class_name)
    elif hasattr(arg, 'remote_type') and arg.remote_type == FLOAT:
        return FLOAT+str(arg.value)
    else:
        raise TypeError('Can\'t make remote call arg. Unknown arg type', type(arg), arg)


def _call(*args, **kwargs):
    response = context.agent.call(args[0], *[_make_arg(arg) for arg in args[1:]], version=2, **kwargs)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None
    elif len(response.args) == 1:
        return _make_remote_object(response.args[0])
    else:
        return [_make_remote_object(arg) for arg in response.args]


def _make_remote_object(arg):
    if type(arg) == dict:
        return RemoteObject.from_dict(arg)
    else:
        return arg


def remote_call(remote_instance, method_name, *args, **kwargs):
    return _call('call', remote_instance, method_name, *args, **kwargs)


def remote_call_static(remote_class, method_name, *args, **kwargs):
    return _call('call_static', remote_class, method_name, *args, **kwargs)


def remote_new(class_name, *args, **kwargs):
    return _call('new', class_name, *args, **kwargs)


def remote_delete(remote_instance, **kwargs):
    return _call('delete', remote_instance, **kwargs)


def remote_set_field(remote_object, field_name, value):
    return _call('set', remote_object, field_name, value)


def remote_get_field(remote_object, field_name):
    return _call('get', remote_object, field_name)
