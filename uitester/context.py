
class Context:
    callback_funcs = []

    def register(self, callback_func):
        self.callback_funcs.append(callback_func)

    def unregister(self, callback_func):
        self.callback_funcs.remove(callback_func)

    def publish(self, msg_type, msg=None):
        for func in self.callback_funcs:
            func(msg_type, msg=msg)
