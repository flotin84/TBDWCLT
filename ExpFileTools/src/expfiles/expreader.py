import numpy as np
import pandas as pd

def get_exp_notes( exp_path ):
    with pd.HDFStore(exp_path) as store:
        return store['notes'][0]

def get_node_file( exp_path, node_index, type_log = True):
    '''
    Given experiment file and node index returns a panda dataframe of log or bin file. 
    Binary files are not stored in a usable way yet.
    
<<<<<<< HEAD
    Arguments:
        path -- path to experiment file
        node_index -- index starts at 0, index of node to get file from
        type_log -- if true log file is returned, false bin file is returned
=======
    |  Arguments:
    |      exp_path -- path to experiment file
    |      node_index --  index of node to get file from, 0 or greater
    |      type_log -- if true log file is returned, false bin file is returned
>>>>>>> refs/heads/ExperimentFileReader
    '''
    type = 'log' if  type_log else 'bin' 
    return pd.read_hdf(exp_path, type + str(node_index) )

def get_node_type(exp_path, node_index):
    '''
    Given path to experiment file and index of node returns 'master', 'slave', or empty string based on stored node type
    
    |  Arguments:
    |      exp_path -- path to experiment file
    |      node_index -- index of node to get type from, 0 or greater
    '''
    with pd.HDFStore(exp_path) as store:
        return store['types'][node_index]

def get_node_file_name(exp_path, node_index, is_log):
    '''
    Given path to experiment file and index of node returns string of the original file name 
    before log or bin was added to experiment file. Example log1.txt or nums.bin
    
    |  Arguments:
    |      exp_path -- path to experiment file
    |      node_index -- index of node to get file name from, 0 or greater
    |      is_log -- True to get log file name, false to get bin
    '''
    file_type = 'log' if is_log else 'bin'
    with pd.HDFStore(exp_path) as store:
        metadata  = store.get_storer(file_type+str(node_index)).attrs.metadata
        return metadata['file_name']
    
    
    
    
    
    