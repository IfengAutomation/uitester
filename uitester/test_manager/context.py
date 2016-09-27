import threading

local_context = threading.local()
local_context.agent = None

agent = local_context.agent


class Context:
    pass
