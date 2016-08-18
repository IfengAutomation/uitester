

error_handlers = []


def handle_error(func):
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            for handler in error_handlers:
                handler.handle(e)
    return _wrapper


class BaseHandler:
    def handle(self, exception):
        pass
