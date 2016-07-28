
class Request:
    id = 0
    version = 1
    method = ''
    args = []
    var = ''

    def __init__(self, id, method, args, var=None):
        self.id = id
        self.method = method
        self.args = args
        if var:
            self.var = var