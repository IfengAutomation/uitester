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
