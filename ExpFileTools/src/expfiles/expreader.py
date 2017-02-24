import numpy as np
import pandas as pd


def get_node_file( path, node_index, type_log = True):
    '''
    Given experiment file and node index returns a DataFrame of log or bin file. 
    
    Arguments:
        path -- path to experiment file
        node_index -- index starts at 0, index of node to get file from
        type_log -- if true log file is returned, false bin file is returned
    '''
    type = 'log' if  type_log else 'bin' 
    return pd.read_hdf(path , type + str(node_index) )