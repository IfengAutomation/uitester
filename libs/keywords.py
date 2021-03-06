import socket

kw_func = {}

var_cache = {}

STRING = '01'
INT = '02'
CLASS = '03'
OBJECT = '04'
FLOAT = '05'
BOOL = '06'


def keyword(name):
    def _register(func):
        kw_func[name] = func
        return func
    return _register


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


"""

    =====     Remote reflection api     ======

"""


def call(remote_object, method, *args):
    return var_cache['reflection'].remote_call(remote_object, method, *args)


def call_static(remote_class, method, *args):
    return var_cache['reflection'].remote_call_static(remote_class, method, *args)


def new(remote_class, *args):
    return var_cache['reflection'].remote_new(remote_class, *args)


def delete(remote_object):
    return var_cache['reflection'].remote_delete(remote_object)


def set_field(remote_object, field_name, value):
    return var_cache['reflection'].remote_set_field(remote_object, field_name, value)


def get_field(remote_object, field_name):
    return var_cache['reflection'].remote_get_field(remote_object, field_name)


def set_var(name, value):
    var_cache[name] = value


def get_var(name):
    return var_cache.get(name)


def get_solo():
    solo = var_cache.get("solo")
    if not solo:
        raise ValueError("You should use start_video to create solo instance before tests")
    return solo


def get_ui_device():
    device = var_cache.get("ui_device")
    if not device:
        raise ValueError("You should use start_video to create UiDevice instance before tests")
    return device


"""

     ======     Local api     =====

"""


@keyword('activate_mock')
def activate_mock(interface_name):
    """
    Activate mock interface
    :param interface_name:
    :return: True or False
    """
    if not var_cache['local'].activate_mock_interface(interface_name):
        raise AssertionError('activate '+interface_name+' fail')


@keyword('deactivate_mock')
def deactivate_mock(interface_name):
    """
    Deactivate mock interface
    :param interface_name:
    :return: True or False
    """
    if not var_cache['local'].deactivate_mock_interface(interface_name):
        raise AssertionError('deactivate '+interface_name+' fail')


@keyword('reset_mock')
def reset_mock():
    """
    Reset mock server, all default mock interface will be active , and other interfaces will be set to inactive
    :return: True or False
    """
    if not var_cache['local'].reset_mock_interface():
        raise AssertionError('reset mock server fail')


@keyword('count_request_contains_str')
def count_request_contains_str(sting_input):
    """
    Count requests url in mock server's request log ,which contains string_input
    :param sting_input:
    :return: int request count
    """
    request_list = var_cache['local'].get_request_list()
    match_count = 0
    for url in request_list:
        if url.find(sting_input) > -1:
            match_count += 1
    return match_count


@keyword('clear_request_log')
def clear_request_log():
    """
    clear mock server's request log
    :return:
    """
    if not var_cache['local'].clear_request_list():
        raise ValueError('Clear request log failed.')


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
    def __init__(self):
        self.remote_type = OBJECT

    @classmethod
    def from_dict(cls, attr_dict):
        obj = cls()
        obj.__dict__ = attr_dict
        obj.remote_type = OBJECT
        return obj

    @classmethod
    def from_object(cls, remote_obj):
        obj = cls()
        obj.__dict__ = remote_obj.__dict__
        obj.remote_type = OBJECT
        return obj

    @classmethod
    def from_class_name(cls, class_name):
        remote_class = cls()
        remote_class.class_name = class_name
        remote_class.remote_type = CLASS
        return remote_class

    @classmethod
    def from_float(cls, float_input):
        obj = cls()
        obj.remote_type = FLOAT
        obj.value = float_input
        return obj

    @classmethod
    def from_bool(cls, bool_input):
        obj = cls()
        obj.remote_type = BOOL
        obj.value = bool_input
        return obj

    def set_field(self, field, value):
        set_field(self, field, value)

    def get_field(self, field):
        return get_field(self, field)
