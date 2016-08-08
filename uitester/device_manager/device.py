from uitester import cache


class Device:
    msg_list = []  # 用来存放将要发送给device的msg，存放多个dict对象，dict中id：执行顺序；msg：request；result：response

    def __init__(self, id, send_msg_func, response_handler_cls=None):
        self.id = id
        self.send_msg_func = send_msg_func
        self.response_handler = response_handler_cls

    def send_msg(self, request):
        self.send_msg_func(request)

    def init_msg_list(self, request):
        """
        将与发送的msg放入执行list中，等待处理
        :param request:
        :return:
        """
        msg_dict = dict()
        key = len(self.msg_list)
        msg_dict["id"] = key
        msg_dict["msg"] = request
        msg_dict["result"] = None
        self.msg_list.append(msg_dict)

    def add_result(self, response):
        """
        返回的结果存入list中，等待处理
        :param response:
        :return:
        """
        for msg in self.msg_list:
            if not msg["result"]:
                msg["result"] = response
                if response.entity:
                    cache.entity = response.entity
                self.msg_manager()
                break

    def msg_manager(self):
        """
        device的msg收发管理器
        :return:
        """
        for msg in self.msg_list:
            if not msg["result"]:
                self.send_msg(msg["msg"])
                break


class BaseResponseHandler:
    """
    Response handler base class.
    ResponseHandler.handle will be call when receive a RPC-response from client
    """
    def handle(self, device, response):
        device.add_result(response)


