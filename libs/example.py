from device import *
from keywords import get_var


@keyword('hello')
def test_first_method():
    """
    keyword doc:
        print hello
    """
    print('hello, world')
    get_view('1')
    solo = get_var('solo')
    solo.get_text('hello')
