'''
Created on Feb 5, 2017

@author: JRC
'''
import numpy as np
import pandas as pd
import os.path
import traceback
import ntpath
from expfiles import node

# create (or open) an hdf5 file and opens in append mode
def __write_node_metadata(store,id, name):
    store.get_storer(id).attrs.metadata = dict(file_name=name) 
    
def __write_node_files(filepath,node,index):
    print("writing node file...")
    store = pd.HDFStore(filepath)
    try:
        if(node.log_path != ""):
            logData = pd.read_csv(node.log_path,sep='\t')
            if (list(logData).pop() == 'Unnamed: 7'):
                del logData['Unnamed: 7']
            store['log'+ str(index)] = logData;
            __write_node_metadata(store,'log'+str(index), __file_name(node.log_path) )
            print('Writing log'+str(index))
        if(node.bin_path != ""): 
            binData = pd.Series(np.fromfile(node.bin_path,dtype=np.uint8),dtype=np.uint8)
            store['bin'+ str(index)] = binData;
            __write_node_metadata(store,'bin'+str(index),__file_name(node.bin_path))
            print('Writing bin'+str(index))
        store.close()
    except IOError as e:
        store.close()
        traceback.print_exc()
        raise e
        
    
#TODO: validate filename
def __number_of_nodes(exp_path):
    max_index = -1
    with pd.HDFStore(exp_path) as store:
        nodes = store.keys()
        for node in nodes:
            if node.startswith('/log') or node.startswith('/bin'):
                if int(node[-1]) > max_index:
                    max_index = int(node[-1])
    return max_index + 1 
    

def generate_experiment_file(new_path, node_list, exp_notes='', overwrite = False ):
    '''
    Given Node array this function creates hdf5 file filled with Node log files,bin files and node type(master/slave). 
    File must not already exist.
    
    Arguments:
        new_path -- Path to new experiment file, file extension must end in .h5
        node_list -- Node or Array of Nodes, it is acceptable for node to not have log,bin, or metadata (master/slave)(filename) 
        exp_notes -- string to be stored in file as experiment notes (default = '')
        overwrite -- Boolean, Bypasses safegaurd against overwriting existing file (default = False)
        
    Throws:
        IOError -- If file at path already exists or error occurs during creation. If error occurs during
            creation the experiment file will not be generated. This could be due to invalid log/bin paths.
    '''
    print("generating...")#TODO assert h5 extension
    index = 0
    
    #Check if file at path already exists
    if( not overwrite and os.path.isfile(new_path) ):
        raise IOError("File %s already exists, only generate new files. This error may be suppressed by passing in overwrite = True" %(new_path))
    node_types = []
    try:            
        if hasattr(node_list, '__iter__'):
            for node in node_list:
                __write_node_files(new_path,node,index)
                index += 1
                node_types.append(node.node_type)
        else:
            __write_node_files(new_path,node_list,index)
            node_types.append(node.node_type)
        with pd.HDFStore(new_path) as store:
            store['notes'] = pd.Series(exp_notes)
            store['types'] = pd.Series(node_types)
    except IOError as e:
        if(os.path.isfile(new_path)):
            print('File created but error occured, removing created file.')
            os.remove(new_path);
        raise e
        
        
def set_node_type(exp_path,node_index,new_type):
    '''
    Changes the type (master,slave,'') for a node in an experiment file
    
    Arguments:
        exp_path -- path to experiment file
        node_index -- index starts from 0, index of node to change type
        new_type -- type should be (master,slave,'')
        
    Throws:
        ValueError -- if new_types does not equal master,slave, or ''
    '''
    if new_type != 'master' and new_type != 'slave' and new_type != '':
        raise ValueError(new_type + ' must equal master, slave, or \'\'')
    with pd.HDFStore(exp_path) as store:
        types = store['types'].set_value(node_index,new_type)
        store['types']= types
        
def add_nodes(exp_path,node_list):   
    '''
        Adds nodes if they dont already exist
    
    '''  
    print("Modifying...")
    #TODO: find last node index
    new_index = __number_of_nodes(exp_path);
    try:
        if hasattr(node_list, '__iter__'):
            for node in node_list:
                print new_index
                __write_node_files(exp_path,node,new_index)
                new_index += 1
        else:
            __write_node_files(exp_path,node_list,new_index) 
    except IOError as e:
        print('Error occured all additions might not have taken place')    
        raise e

def set_node_file(exp_path ,node_index, file_path, is_log):
    if is_log:
        __write_node_files(exp_path,node.Node(log_path = file_path ),node_index)
    else:
        __write_node_files(exp_path,node.Node(bin_path = file_path ),node_index)

    


def del_node_file(exp_path,node_index,is_log):
    '''TODO: is this the right way to handle no file
        Removes node file from HDF5 file, if file doesn't exist doesn't exist nothing happens
    '''
    #TODO remove type
    with pd.HDFStore(exp_path) as store:
        node_type = 'log' if is_log else 'bin'
        node_name = node_type + str(node_index)
        if '/'+node_name in store.keys():
            store.remove(node_type + str(node_index))

        
def del_node(exp_path,node_index):
    '''
        Given experiment file and node index, deletes the log and bin at that index if they exist. If no files at that index exist nothing happens.
        All later nodes will be shifted down 1 index so there are no gaps in numbering. For example if file has nodes: 0,1,2 then we remove 1
        -> file now has nodes: 0,1 where the node at index 1 used to be at index 2
        
        Arguments:
            exp_path -- path to experiment file
            node_index -- index starts from 0, index of node to get removed
    '''
    del_node_file(exp_path,node_index,True)
    del_node_file(exp_path,node_index,False)
    with pd.HDFStore(exp_path) as store:
        types = store['types'].drop(node_index)
        types.index = range(types.size)
        store['types'] = types
        for key in store.keys():
            if key.startswith('/log') or key.startswith('/bin'):
                current_index = int(key[-1])
                if current_index > node_index:
                    store.get_node(key)._f_rename( key[1:len(key)-1] + str(current_index - 1) )

        
def __file_name(path):
    ntpath.basename("a/b/c")
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)        
        
        
        
        
        
        
        
        
        

    
    
