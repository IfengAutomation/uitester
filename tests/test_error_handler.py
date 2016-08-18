from uitester import error_handler
from unittest import TestCase


class TestErrorHandler(TestCase):

    def test_handler(self):
        error_handler.error_handlers.append(HandlerForTest())

        @error_handler.handle_error
        def err_func():
            raise ValueError('msg')

        err_func()


class HandlerForTest(error_handler.BaseHandler):
    def handle(self, exception):
        assert type(exception) == ValueError
        assert exception.args[0] == 'msg'