kw_func = {}

var_cache = {}


def keyword(name):
    def _register(func):
        kw_func[name] = func
        return func
    return _register


def call(remote_object, method, *args):
    return var_cache['reflection'].remote_call(remote_object, method, *args)


def call_static(remote_class, method, *args):
    return var_cache['reflection'].remote_call_static(remote_class, method, *args)


def new(remote_class, *args):
    return var_cache['reflection'].remote_new(remote_class, *args)


def delete(remote_object):
    return var_cache['reflection'].remote_delete(remote_object)


class RemoteObject:
    """
    Attr list:

    =Object= ----------
    hash
    class_name

    =View= ---------
    resource_id
    package_name
    content_desc

    =TextView= ----------
    text

    """

    @classmethod
    def from_dict(cls, attr_dict):
        obj = cls()
        obj.__dict__ = attr_dict
        return obj

    @classmethod
    def from_object(cls, remote_obj):
        obj = cls()
        obj.__dict__ = remote_obj.__dict__
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