RESULT_PASS = 1
RESULT_FAIL = 0


class Response:

    def __init__(self):
        self.id = 0
        self.version = 1
        self.result = 1
        self.error = ''
        self.entity = {}
