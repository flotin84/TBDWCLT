import numpy as np
import pandas as pd
import json
from dask.array.core import store


def get_exp_notes( exp_path ):
    with pd.HDFStore(exp_path) as store:
        return store['notes'][0]

def get_node_file( path, node_index, type_log = True):
    '''
    Given experiment file and node index returns a DataFrame of log or bin file. 
    Binary files are not stored in a usable way yet.
    
    Arguments:
        path -- path to experiment file
        node_index -- index starts from 0, index of node to get file from
        type_log -- if true log file is returned, false bin file is returned
    '''
    type = 'log' if  type_log else 'bin' 
    return pd.read_hdf(path , type + str(node_index) )

def get_node_type(path, node_index):
    '''
    Given path to experiment file and index of node returns 'master' or 'slave' based on stored node type
    
    Arguments:
        path -- path to experiment file
        node_index -- index starts from 0, index of node to get node type from
    '''
    with pd.HDFStore(path) as store:
        return store['types'][node_index]

def get_node_file_name(path, node_index,is_log):
    file_type = 'log' if is_log else 'bin'
    with pd.HDFStore(path) as store:
        metadata  = store.get_storer(file_type+str(node_index)).attrs.metadata
        return metadata['file_name']