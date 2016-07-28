RESULT_PASS = 1
RESULT_FAIL = 0


class Response:
    id = 0
    version = 1
    result = 1
    error = ''
    entity = {}

    def __init__(self, id, result, error=None, entity=None):
        self.id = id
        self.result = result
        if error:
            self.error = error
        if entity:
            self.entity = entity
