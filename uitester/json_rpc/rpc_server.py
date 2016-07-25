import socket
import SocketServer


class RPCServer(SocketServer.ThreadingTCPServer):
    pass


class RPCRequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        data = self.rfile.readline().strip()
        self.wfile.write('read data ==> {}\n'.format(data))


def get_server(host, port):
    return RPCServer((host, port), RPCRequestHandler)
