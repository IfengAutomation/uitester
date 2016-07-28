
class Request:
    id = 0
    version = 1
    method = ''
    args = []
    var = ''

    def __init__(self, id, version, method, var, args):
        self.id = id
        self.version = version
        self.method = method
        self.var = var
        self.args = args