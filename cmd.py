from helper import *


def cmd_info(words, nodes):
    '''handle `info` command and its arguments.'''
    num_params = len(words)
    if num_params == 1:
        print_all_info(nodes)
    elif num_params == 2:
        node_id = words[1]
        if node_exists(node_id, nodes):
            nodes[node_id].print_info()
    else:
        print("Error: `info` takes at most 2 arguments.")

def cmd_get(words, nodes):
    '''handle `get` command and its arguments.'''
    num_params = len(words)
    if num_params != 4 or words[2] != 'from':
        print("Error: `get` command format is `get <key> from <server name>`.")
    else:
        key, node_id = words[1], words[3]
        if node_exists(node_id, nodes):
            _get(key, node_id, nodes)

def cmd_set(words, nodes):
    '''handle `set` command and its arguments.'''
    num_params = len(words)
    if num_params != 5 or words[3] != 'to':
        print("Error: `set` command format is `set <key> <value> to <server name>`.")
    else:
        key, value, node_id = words[1], words[2], words[4]
        if node_exists(node_id, nodes):
            _set(key, value, node_id, nodes)

def cmd_start(words, nodes):
    pass

def cmd_kill(words, nodes):
    '''handle `kill` command and its arguments.'''
    num_params = len(words)
    if num_params == 2:
        node_id = words[1]
        if node_exists(node_id, nodes):
            kill(node_id, nodes)
    else:
        print("Error: 'kill' takes exactly 1 argument.")

def cmd_help(_, __):
    print('    info [server name]                       ')
    print('    get <key> from <server name>             ')
    print('    set <key> <value> to <server name>       ')
    print('    start <server name>                      ')
    print('    kill <server name>                       ')
    print('    help                                     ')
    print('    exit                                     ')

def cmd_exit(_, __):
    print('Bye!')
    exit()

def cmd_unknown(words):
    print('Unkonwn command `' + words[0] + '`.')