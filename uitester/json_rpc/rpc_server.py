import inspect
import socketserver

from uitester.json_rpc import json_helper
from uitester.json_rpc.response import Response, RESULT_PASS, RESULT_FAIL


class RPCServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.wfiles = {}
        self.callback_funcs = {}
        self.msg_id = 0

    def register_wfile(self, device_id, wfile):
        self.wfiles[device_id] = wfile

    def unregister_wfile(self, device_id):
        self.wfiles.pop(device_id, default='default')

    def send_msg(self, msg, device_id_list=None):
        if device_id_list is None:
            return
        self.msg_id += 1
        msg.id = self.msg_id
        msg_str = json_helper.obj_to_json(msg)
        for device_id in device_id_list:
            wfile = self.wfiles.get(device_id)
            if wfile:
                wfile.wirte(bytes(msg_str))

    def subscribe(self, device_id, callback_func):
        func_signature = inspect.signature(callback_func)
        if len(func_signature.parameters) < 1:
            raise ValueError('Subscribe callback function need at least 1 argument')
        self.callback_funcs[device_id] = callback_func

    def unsubscribe(self, device_id):
        self.callback_funcs.pop(device_id, default='default')


class RPCRequestHandler(socketserver.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle(self):
        register = False
        device_id = None

        while True:
            data = self.rfile.readline().strip()
            if len(data) == 0:
                if register and device_id:
                    self.server.wfiles.pop(device_id, default=None)
                    self.server.callback_funcs.pop(device_id, default=None)
                break
            origin_msg = json_helper.json_to_obj(data.decode())
            if not register:
                if origin_msg.method == 'register':
                    device_id = origin_msg.args[0]
                    self.server.wfiles[device_id] = self.wfile
                    res = Response()
                    res.id = origin_msg.id
                    res.result = RESULT_PASS
                    self.wfile.write(json_helper.obj_to_json(res).encode())
                else:
                    res = Response()
                    res.id = origin_msg.id
                    res.result = RESULT_FAIL
                    res.error = 'Need register device first.'
                    self.wfile.write(bytes(json_helper.obj_to_json(res)))
            else:
                func = self.server.callback_funcs.get(device_id, default=None)
                if func:
                    func(origin_msg)


def get_server(host, port):
    return RPCServer((host, port), RPCRequestHandler)
