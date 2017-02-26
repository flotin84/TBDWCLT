'''
Created on Feb 5, 2017

@author: JRC
'''
import warnings
class Node:
    
    def __init__(self, log_path = '', bin_path = '',node_type = '',file_name=''):
        '''
        Creates node that can have a log, bin, and metadata (node type and file_name).
        
        Attributes:
            log_path -- path to log file (default = '')
            bin_path -- path to bin file (default = '')
            node_type -- string master or slave  (default = '')
            file_name -- original file name, used to export later (default = '')
        '''
        self.logpath = log_path
        self.binpath = bin_path
        if (node_type != 'master' and node_type != 'slave' and node_type != ''):
            raise ValueError('node_type provided "%s" should equal "slave", "master", or be empty '%(node_type))
        self.node_type = node_type;
        if(file_name == ''):
            warnings.warn('Node does not have file name, exported file will not maintain original name')
        self.file_name = file_name;