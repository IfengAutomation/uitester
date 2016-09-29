"""
Python rpc agent
Use for test rpc server
"""
import socket
from threading import Thread
import logging
import json


logger = logging.getLogger('Tester')


class Agent:
    def __init__(self, device_id):
        self.device_id = device_id
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.real_func = {}

    def start(self, host, port):
        self.sock.connect((host, port))
        logger.debug('Connect to {}:{}'.format(host, port))
        t = Thread(target=self.receive_msg)
        t.setDaemon(True)
        t.start()

    def stop(self):
        unregister_msg = {
            'msg_type': 1,
            'msg_id': 1,
            'version': 1,
            'name': 'unregister',
            'args': []
        }
        self.sock.sendall((json.dumps(unregister_msg) + '\n').encode())
        self.sock.close()

    def receive_msg(self):
        register_msg = {
            'msg_type': 1,
            'msg_id': 1,
            'version': 1,
            'name': 'register',
            'args': [self.device_id]
        }
        response_msg = {
            'msg_type': 2,
            'msg_id': 1,
            'version': 1,
            'name': 'response',
            'args': []
        }
        self.sock.sendall((json.dumps(register_msg) + '\n').encode())
        r_buffer = self.sock.makefile(mode='r')
        register_result = r_buffer.readline()
        #register success
        print(register_result)
        while True:
            line = r_buffer.readline()
            logger.debug('receive msg : {}'.format(line))
            call_obj = json.loads(line)
            method_name = call_obj['name']
            func = self.real_func.get(method_name)
            if func:
                res = func(call_obj['args'])
                response_msg['args'] = [res]
                response_msg['msg_id'] = call_obj['msg_id']
            else:
                response_msg['name'] = 'error'
            self.sock.sendall((json.dumps(response_msg) + '\n').encode())

    def add_func(self, func_name, func):
        self.real_func[func_name] = func


def hello():
    logger.info('Agent: Hello')
    return True


def get_view(view_id):
    logger.info('Agent: GetView by id [{}]'.format(view_id))
    return {'id': view_id, 'class': 'TextView', 'text': None, 'hash': 123456}


def start_app(package_name):
    logger.info('Agent: StartApp bt package name [{}]'.format(package_name))
    return True


def finish_app():
    logger.info('Agent: finish app')
    return True


def click_on_text(text):
    logger.info('Agent: click on text [{}]'.format(text))
    return True


def enter_text(view_hash, text):
    logger.info('Agent: enter text [{}] to view [{}]'.format(text, view_hash))
    return True


def wait_for_text(text):
    logger.info('Agent: wait for text [{}]'.format(text))
    return True


def click_on_view(view_hash):
    logger.info('Agent: click on view [{}]'.format(view_hash))
    return True


def get_test_agent(device_id):
    _agent = Agent(device_id)
    _agent.add_func('hello', hello)
    _agent.add_func('GetView', get_view)
    _agent.add_func('StartApp', start_app)
    _agent.add_func('FinishApp', finish_app)
    _agent.add_func('ClickOnText', click_on_text)
    _agent.add_func('EnterText', enter_text)
    _agent.add_func('WaitForText', wait_for_text)
    _agent.add_func('ClickOnView', click_on_view)
    return _agent
