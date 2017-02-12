'''
Created on Feb 5, 2017

@author: JRC
'''
class Node:
    
    def __init__(self, log_path = '', bin_path = '',node_type = ''):
        '''
        Creates node that can have a log, bin, and node type.
        
        Attributes:
            log_path -- path to log file (default = '')
            bin_path -- path to bin file (default = '')
            node_type -- string master or slave  (default = '')
        '''
        self.logpath = log_path
        self.binpath = bin_path
        self.node_type = node_type if (node_type == 'master' or node_type == 'slave') else ''