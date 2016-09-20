from uitester.test_manager import rpc_server, rpc_agent
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Tester')

PORT = 11800
selected_device_id = None
test_server = None
commands = {}
agents = {}


def start_agent(device_id):
    _agent = rpc_agent.get_test_agent(device_id)
    agents[device_id] = _agent
    _agent.start('0.0.0.0', PORT)


def close_agent(device_id):
    _agent = agents.get(device_id)
    if _agent:
        _agent.stop()
        agents.pop(device_id)


def show_agents():
    for _agent_id in agents:
        print(_agent_id)


def agent(*args):
    """
    usage: agent [option]

    options:
    add [device_id] 'add agent with device_id'
    rm [device_id] 'remove agent with device_id'
    list 'list all agents'
    """
    if len(args) < 1:
        print('Agent arg error. \nneed at least 1 args\n')
        return
    if args[0] == 'add':
        if len(args) < 2:
            print('Agent add need 2 args')
            return
        start_agent(args[1])
    elif args[0] == 'rm':
        close_agent(args[1])
    elif args[0] == 'list':
        show_agents()
    else:
        print('Unknown agent command')

commands['quit'] = {'func': None, 'help': ''}
commands['agent'] = {'func': agent, 'help': agent.__doc__}


def server(*args):
    """
    usage: server [option]

    options:
    agents 'list all registered agents'
    connections 'list all connections'
    call [remote_method] 'call remote method on agent'
    select [device_id] 'select device_Id'
    """
    global selected_device_id
    if len(args) < 1:
        print('Unknown command')
        return
    if args[0] == 'agents':
        for _agent in test_server._agents:
            print(_agent)
    elif args[0] == 'connections':
        pass
    elif args[0] == 'use':
        if len(args) < 2:
            print('Use need 2 args. e.g. use device_id_1')
            return
        if args[1] not in test_server._agents:
            print('Device id not found in register device list')
            return
        selected_device_id = args[1]
    elif args[0] == 'call':
        if len(args) < 2:
            print('Call remote method need a method name')
            return
        if not selected_device_id:
            print('Not select any device')
            return
        agent_proxy = test_server._agents.get(selected_device_id)
        if agent_proxy:
            remote_call_args = []
            if len(args) > 2:
                remote_call_args = args[2:]
            response = agent_proxy.call(args[1], remote_call_args)
            print(response)
            print(response.to_json())

commands['server'] = {'func': server, 'help': server.__doc__}


def parse_line(line):
    items = []
    cache = None
    in_quotation = False
    for char in line:
        if char == ' ' and not in_quotation and cache:
            items.append(cache)
            cache = None
        elif char == '"':
            in_quotation = not in_quotation
        else:
            if not cache:
                cache = char
            else:
                cache += char
    if cache:
        items.append(cache)

    if in_quotation:
        raise ValueError('Missing quote. {}'.format(line))

    return items


def test():
    global test_server
    test_server = rpc_server.start(11800)
    while True:
        user_input = input('>>').strip()
        if len(user_input) == 0:
            continue
        if user_input == 'quit':
            break
        if user_input == 'help':
            for cmd in commands:
                print('Command: {}'.format(cmd))
                print(commands[cmd]['help'])
            continue
        items = parse_line(user_input)
        cmd = commands.get(items[0])
        if cmd:
            cmd['func'](*items[1:])


if __name__ == '__main__':
    test()
