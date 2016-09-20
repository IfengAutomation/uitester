from device import *


@keyword('hello')
def test_first_method():
    """
    keyword doc:
        print hello
    """
    print('hello, world')
    get_view('1')
