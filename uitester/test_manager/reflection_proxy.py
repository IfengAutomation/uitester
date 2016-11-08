import logging
from uitester.test_manager import context

logger = logging.getLogger('Tester')

STRING = '01'
INT = '02'
CLASS = '03'
OBJECT = '04'


class RemoteObject:
    """
    Attr list:

    =Object= ----------
    hash
    class_name

    =View= ---------
    resource_id
    package_name

    =TextView= ----------
    text

    """

    @classmethod
    def from_dict(cls, attr_dict):
        obj = cls()
        obj.__dict__ = attr_dict
        return obj


class RemoteClass:
    """
    Attr list:
    -----------
    class_name

    """
    def __init__(self):
        self.class_name = ''

    @classmethod
    def from_class_name(cls, class_name):
        remote_class = cls()
        remote_class.class_name = class_name
        return remote_class


def _make_arg(arg):
    arg_type = type(arg)
    if arg_type == str:
        return STRING+arg
    elif arg_type == int:
        return INT+str(arg)
    elif arg_type == RemoteObject:
        return OBJECT+str(arg.hash)
    elif arg_type == RemoteClass:
        return CLASS+str(arg.class_name)
    else:
        raise TypeError('Can\'t make remote call arg. Unknown arg type', arg)


def _call(*args):
    response = context.agent.call(args[0], *[_make_arg(arg) for arg in args[1:]], version=2)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None
    else:
        result = response.args[0]
        if type(result) == dict:
            obj = RemoteObject()
            obj.__dict__ = result
            return obj
        else:
            return result


def remote_call(remote_instance, method_name, *args):
    return _call('call', remote_instance, method_name, *args)


def remote_call_static(remote_class, method_name, *args):
    return _call('call_static', remote_class, method_name, *args)


def remote_new(class_name, *args):
    return _call('new', class_name, *args)


def remote_delete(remote_instance):
    return _call('delete', remote_instance)
