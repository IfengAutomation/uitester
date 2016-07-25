import socketserver


class RPCServer(socketserver.ThreadingTCPServer):
    pass


class RPCRequestHandler(socketserver.StreamRequestHandler):

    def handle(self):
        data = self.rfile.readline().strip()
        self.wfile.write('read data ==> {}\n'.format(data))


def get_server(host, port):
    return RPCServer((host, port), RPCRequestHandler)
