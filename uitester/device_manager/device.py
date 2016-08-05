from uitester import cache


class Device:

    def __init__(self, id, send_msg_func, response_handler_cls=None):
        self.id = id
        self.send_msg_func = send_msg_func
        self.response_handler = response_handler_cls

    def send_msg(self, request):
        self.send_msg_func(request)


class BaseResponseHandler:
    """
    Response handler base class.
    ResponseHandler.handle will be call when receive a RPC-response from client
    """
    def handle(self, response):
        if response.entity:
            cache.entity = response.entity

