from libs import kw_proxy


class CustomKeywords(kw_proxy.KWProxy):

    def test_func(self):
        print('Test func from custom lib')

    def test_number(self):
        return 1

    def test_bool(self):
        return False

    def test_str(self):
        return 'hello'

    def test_obj(self):
        return type('View', (), {'text': 'title01', 'id': 'test-view-id-1'})

