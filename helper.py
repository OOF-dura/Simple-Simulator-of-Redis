import os.path
import configparser
from collections import OrderedDict
from model import *


def print_welcome():
    '''Print a welcome text.'''
    print(HTML('Welcome to <skyblue>Simple Simulator of Redis</skyblue> (SSR)'))
    print(r'''
      ___           ___           ___     
     /  /\         /  /\         /  /\    
    /  /::\       /  /::\       /  /::\   
   /__/:/\:\     /__/:/\:\     /  /:/\:\  
  _\_ \:\ \:\   _\_ \:\ \:\   /  /::\ \:\ 
 /__/\ \:\ \:\ /__/\ \:\ \:\ /__/:/\:\_\:\
 \  \:\ \:\_\/ \  \:\ \:\_\/ \__\/~|::\/:/
  \  \:\_\:\    \  \:\_\:\      |  |:|::/ 
   \  \:\/:/     \  \:\/:/      |  |:|\/  
    \  \::/       \  \::/       |__|:|~   
     \__\/         \__\/         \__\|
    ''')
    print("For any help, please input the `help` command.")

def load_config_file():
    '''Load config file.'''
    # check whether config file exists
    if os.path.isfile("redis.conf"):
        print('Config file found.')
    else:
        print('Error: no config file `redis.conf` exists.')
    
    # load config file
    config = configparser.ConfigParser()
    config.read("redis.conf")
    
    # check if there're duplicate nodes
    node_ids = config.sections()
    if len(set(node_ids)) != len(node_ids):
        raise Exception('duplicate nodes.')
    
    # create a map from node_id to node
    nodes = OrderedDict()
    for node_id in node_ids:
        if config.has_option(node_id, 'slaveof'):
            slaveof = config.get(node_id, 'slaveof')
            nodes[node_id] = Slave(node_id, slaveof)
        elif config.has_option(node_id, 'monitor'):
            nodes[node_id] = Sentinel(node_id, config.get(node_id, 'monitor'))
        else:
            nodes[node_id] = Master(node_id)
    
    # set matser's slave list
    for node in nodes.values():
        if isinstance(node, Slave):
            nodes[node.slaveof].slaves.append(node.node_id)
    print('Config file loaded successfully.')
    return nodes

def print_all_info(nodes):
    '''print all nodes' info.'''
    for node in nodes.values():
        node.print_info()

def _get(key, node_id, nodes):
    '''get value by key from node.'''
    node = nodes[node_id]
    print(node.data[key] if node.data and key in node.data.keys() else 'None')

def set_helper(key, value, node_id, nodes):
    node = nodes[node_id]
    node.data[key] = value if node.data else node.data = {}

def node_exists(node_id, nodes):
    result = node_id in nodes.keys()
    if not result:
        print('Error: No node called', node_id) 
    return result

def _set(key, value, node_id, nodes):
    '''set (key, value) to node.'''
    node = nodes[node_id]
    if isinstance(node, Slave):
        print('Error: cannot set data to slave node.')
    set_helper(key, value, node_id, nodes)
    for slave_id in node.slaves:
        set_helper(key, value, slave_id, nodes)

def kill(node_id, nodes):
    node = nodes[node_id]
    if node.status == 0:
        return
    node.status = 0