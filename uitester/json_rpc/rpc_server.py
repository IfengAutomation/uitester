import socketserver

from uitester.device_manager.device import Device, BaseResponseHandler
from uitester.json_rpc import json_helper
from uitester.json_rpc.response import Response, RESULT_PASS
from uitester import cache


class RPCServer(socketserver.ThreadingTCPServer):
    pass


class RPCRequestHandler(socketserver.StreamRequestHandler):
    device = None

    def handle(self):
        self.wait_for_register()
        self.wait_for_rpc_command()

    def send_msg(self, msg):
        msg_str = json_helper.encode_obj_to_json(msg)
        self.wfile.write(msg_str)

    def wait_for_register(self):
        while True:
            data = self.rfile.readline().strip()
            request = json_helper.decoded_json_to_request(data.decode())
            if request.method == "register" and self.handle_register(request):
                break
            else:
                pass

    def handle_register(self, request):
        response_handler = BaseResponseHandler().handle
        self.device = device = Device(request.args[0], self.send_msg, response_handler)
        # 添加至设备列表
        cache.devices[device.id] = device
        response = Response(request.id, RESULT_PASS)
        self.send_msg(response)
        return True

    def wait_for_rpc_command(self):
        while True:
            data = self.rfile.readline().strip()
            if self.device.response_handler:
                response = json_helper.decoded_json_to_response(data.decode())
                self.device.response_handler(response)   # 处理response结果


def get_server(host, port):
    return RPCServer((host, port), RPCRequestHandler)
