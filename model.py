from prompt_toolkit import HTML
from prompt_toolkit import print_formatted_text as print


class Node(object):
    def __init__(self, node_id, status=1, data=None):
        self.node_id = node_id
        self.status = status
        self.data = data
    
    def print_info(self):
        '''print info.'''
        # print node_id
        print(HTML('<violet>[' + self.node_id + ']</violet>'))
        
        # print status
        if self.status == 0:
            print(HTML('Status: <ansired>Off</ansired>'))
        else:
            print(HTML('Status: <ansigreen>On</ansigreen>'))


class Master(Node):
    def __init__(self, node_id, slaves=None, status=1, data=None):
        super().__init__(node_id)
        self.slaves = slaves
        if not slaves:
            self.slaves = []

    def print_info(self):
        super().print_info()
        if isinstance(self, Slave):
            print(HTML('Type: Slave'))
            print(HTML('Slave of: ' + str(self.slaveof)))
        else:
            print(HTML('Type: <skyblue>Master</skyblue>'))
        print(HTML('Slaves: <ansiyellow>' + str(self.slaves) + '</ansiyellow>'))
        print() # seperator


class Slave(Master):
    def __init__(self, node_id, slaveof=None, status=1, data=None):
        super().__init__(node_id)
        self.slaveof = slaveof


class Sentinel(Node):
    def __init__(self, node_id, monitor=None, status=1, data=None):
        super().__init__(node_id)
        self.monitor = monitor
    
    def print_info(self):
        super().print_info()
        print(HTML('Type: <seagreen>Sentinel</seagreen>'))
        print(HTML('Monitor: ' + str(self.monitor)))
        print() # seperator