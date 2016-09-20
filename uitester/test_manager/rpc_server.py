from socketserver import ThreadingTCPServer, StreamRequestHandler
import json
from threading import Thread
import logging
import queue


logger = logging.getLogger('Tester')

Timeout = 5
Port = 11800


class RPCServer(ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self._agents = {}

    def add_agent(self, agent):
        self._agents[agent.device_id] = agent

    def rm_agent(self, device_id):
        self._agents.pop(device_id)


class RPCHandler(StreamRequestHandler):

    def __init__(self, request, client_address, server):
        self.has_register = False
        self.agent_proxy = None
        super().__init__(request, client_address, server)

    def handle(self):
        while True:
            line = self.rfile.readline().decode().strip()
            if len(line) == 0:
                break
            try:
                msg = RPCMessage.from_json(line)
                if not self.has_register:
                    self.handle_register(msg)
                elif msg.name == 'unregister':
                    self.handle_unregister()
                else:
                    self.handle_message(msg)
            except Exception as e:
                print(e.message)
                continue
        if self.has_register:
            self.server.rm_agent(self.agent_proxy.device_id)

    def handle_register(self, msg):
        if msg.msg_type == RPCMessage.RPC_CALL and msg.name == 'register':
            if len(msg.args) < 1:
                res = self._make_error_msg()
                self.wfile.write(res.to_json().encode())
            self.agent_proxy = RPCAgent()
            self.agent_proxy.device_id = msg.args[0]
            self.agent_proxy.wfile = self.wfile
            self.agent_proxy.connection = self.connection
            self.server.add_agent(self.agent_proxy)
            self.has_register = True
        else:
            self.wfile.write(self._make_error_msg())

    def _make_error_msg(self):
        err_msg = RPCMessage()
        err_msg.msg_type = RPCMessage.RPC_RESULT
        err_msg.args = [False]
        return err_msg

    def handle_unregister(self):
        self.server.rm_agent(self.agent_proxy.device_id)
        self.connection.close()
        self.agent_proxy.is_closed = True

    def handle_message(self, msg):
        self.agent_proxy.responses.put(msg)


class RPCAgent:

    def __init__(self):
        self.device_id = ''
        self.is_closed = False
        self.msg_id = 0
        self.wfile = None
        self.connection = None
        self.responses = queue.Queue()

    def call(self, method, args=None):
        self.msg_id += 1
        msg = RPCMessage()
        msg.msg_id = self.msg_id
        msg.msg_type = RPCMessage.RPC_CALL
        msg.name = method
        msg.args = args
        self.wfile.write((msg.to_json() + '\n').encode())
        res = self.responses.get()
        return res

    def close(self):
        self.connection.close()


class RPCMessage:
    RPC_CALL = 1
    RPC_RESULT = 2

    def __init__(self):
        self.msg_type = None
        self.msg_id = None
        self.version = 1
        self.name = None
        self.args = []

    @classmethod
    def from_json(cls, json_str):
        msg_dict = json.loads(json_str)
        if type(msg_dict) is not dict:
            raise TypeError('Json is not a dict, can\'t create rpc message')
        instance = cls()
        instance.__dict__ = msg_dict
        return instance

    def to_json(self):
        return json.dumps(self.__dict__)


def start(port):
    server = RPCServer(('0.0.0.0', port), RPCHandler)
    t = Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()
    logger.debug('RPC Server started')
    return server
