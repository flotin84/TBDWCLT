'''
Created on Feb 5, 2017

@author: JRC
'''
import numpy as np
import pandas as pd
import os.path
import traceback
# create (or open) an hdf5 file and opens in append mode
def __write_node_metadata(store,id, type):
    store.get_storer(id).attrs.metadata = dict(node_type=type) 
    
def __write_node_files(filepath,node,index):
    print("writing node file...")
    store = pd.HDFStore(filepath)
    try:
        if(node.logpath != ""):
            logData = pd.read_csv(node.logpath,sep='\t')
            if (list(logData).pop() == 'Unnamed: 7'):
                del logData['Unnamed: 7']
            store['log'+ str(index)] = logData;
            __write_node_metadata(store,'log'+str(index),node.node_type)
            print('Writing log'+str(index))
        if(node.binpath != ""): 
            binData = pd.Series(np.fromfile(node.binpath,dtype=np.uint8),dtype=np.uint8)
            store['bin'+ str(index)] = binData;
            __write_node_metadata(store,'bin'+str(index),node.node_type)
            print('Writing bin'+str(index))
        store.close()
    except IOError as e:
        store.close()
        traceback.print_exc()
        raise e
        
    
#TODO: validate filename

def generate_experiment_file(new_path, node_list, overwrite = False ):
    '''
    Given Node array this function creates hdf5 file filled with Node log files,bin files and node type(master/slave). 
    File must not already exist.
    
    Throws:
        IOError -- If file at path already exists or error occurs during creation. If error occurs during
            creation the experiment file will not be generated. This could be due to invalid log/bin paths.
    
    Arguments:
        new_path -- Path to new experiment file, file extension must end in .h5
        node_list -- Node or Array of Nodes, it is acceptable for node to not have log,bin, or metadata (master/slave)(filename) 
        overwrite -- Boolean, Bypasses safegaurd against overwriting existing file (default = False)
    '''
    print("generating...")#TODO assert h5 extension
    index = 0
    
    #Check if file at path already exists
    if( not overwrite and os.path.isfile(new_path) ):
        raise IOError("File %s already exists, only generate new files. This error may be suppressed by passing in overwrite = True" %(new_path))
    
    try:
        if hasattr(node_list, '__iter__'):
            for node in node_list:
                __write_node_files(new_path,node,index)
                index += 1
        else:
            __write_node_files(new_path,node_list,index) 
    except IOError as e:
        if(os.path.isfile(new_path)):
            print('File created but error occured, removing created file.')
            os.remove(new_path);
        raise e
        
        
def modify_node_file(exp_path,node_list):   
    '''
       Replaces file currently associated with node 
    
    '''  
    print("Modifying...")
    index = 0
    #__write_experiment_metadata(nodelist.count)
    for node in node_list:
        __write_node_files(exp_path,node,index)
        index += 1
        
def add_node(exp_path,node_list):   
    '''
        Adds nodes if they dont already exist
    
    '''  
    print("Modifying...")
    index = 0
    #__write_experiment_metadata(nodelist.count)
    for node in node_list:
        __write_node_files(exp_path,node,index)
        index += 1
    
def del_node_file(exp_path,node_index,is_log):
    '''
    
    '''
    with pd.HDFStore(exp_path) as store:
        node_type = 'log' if is_log else 'bin'
        store.remove(node_type + str(node_index))
        

        
        
        
        
        
        
        
        
        
        

    
    
