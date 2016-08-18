

class Device:
    BLANK = 0x0
    OFFLINE = 0x1
    ONLINE = 0x2
    READY = 0x3
    RUNNING = 0x4

    def __init__(self, device_id, send_msg_func, response_handler_cls=None):
        self.status = self.BLANK
        self.id = device_id
        self.send_msg_func = send_msg_func
        self.response_handler = response_handler_cls

    def send_msg(self, request):
        self.send_msg_func(request)


class BaseResponseHandler:
    """
    Response handler base class.
    ResponseHandler.handle will be call when receive a RPC-response from client
    """
    def handle(self, device, response):
        pass

