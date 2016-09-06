import unittest
import socket
from threading import Thread
from uitester.json_rpc import rpc_server
from uitester.json_rpc import json_helper


class TestRPCClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rfile = self.sock.makefile()

    def connect(self):
        self.sock.connect(('0.0.0.0', 11800))

    def call(self, id, method, *args):
        msg = type('RPCCall', (), {})()
        msg.__dict__ = {'id': id, 'method': method, 'args': args}
        byte_msg = json_helper.obj_to_json(msg).encode()
        self.sock.sendall(byte_msg)
        response = self.rfile.readline()
        return json_helper.json_to_obj(response)

    def response(self, id, result, error='', entity=None):
        res = type('RPCResponse', (), {})()
        res.__dict__ = {'id': id, 'result': result, 'error': error, 'entity': entity}
        bytes_msg = json_helper.obj_to_json(res).encode()
        self.sock.sendall(bytes_msg)

    def disconnect(self):
        self.sock.close()


class RPCServerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = server = rpc_server.get_server('0.0.0.0', 11800)
        cls.server_thread = Thread(target=server.serve_forever, args=[1], daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.server_close()
        cls.server = None
        cls.server_thread = None

    def setUp(self):
        self.cli = TestRPCClient()
        self.cli.connect()

    def tearDown(self):
        self.cli.disconnect()
        self.cli = None

    def test_register(self):
        res = self.cli.call(11, 'register', '123456789')
        self.assertTrue(res.id == 11)
        self.assertTrue(res.result == 1)
        self.assertTrue('123456789' in self.server.wfiles)

    def test_msg_before_register(self):
        res = self.cli.call(1, 'hello', '0')
        self.assertTrue(res.id == 1)
        self.assertTrue(res.result == 0)

    def test_response_callback(self):

        def msg_callback(msg):
            self.assertTrue(msg.id == 2)
            self.assertTrue(msg.result == 1)

        res_1 = self.cli.call(1, 'register', '123456789')
        self.assertTrue(res_1.id == 1)
        self.assertTrue(res_1.result == 1)
        self.assertTrue('123456789' in self.server.wfiles)

        self.server.subscribe('123456789', msg_callback)

        self.cli.response(2, 1)

    def test_remote_call(self):
        res_1 = self.cli.call(1, 'register', '123456789')
        self.assertTrue(res_1.id == 1)
        self.assertTrue(res_1.result == 1)
        self.assertTrue('123456789' in self.server.wfiles)

        request = type('Request', (), {})()
        request.__dict__ = {'id': 2, 'method': 'get_view', 'args': ['id-123']}
        self.server.send_msg(request, device_id_list=['123456789'])

        cli_req_str = self.cli.rfile.readline()
        cli_req = json_helper.json_to_obj(cli_req_str)
        self.assertTrue(cli_req.method == 'get_view')
        self.assertTrue(cli_req.args == ['id-123'])
