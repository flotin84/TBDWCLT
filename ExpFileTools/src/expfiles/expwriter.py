'''
Created on Feb 5, 2017

@author: JRC
'''
import numpy as np
import pandas as pd
import os

import traceback
import ntpath
import node
import expreader
from subprocess import call

# create (or open) an hdf5 file and opens in append mode
def __write_node_metadata(store,id, name):
    store.get_storer(id).attrs.metadata = dict(file_name=name) 
    
def __write_node_files(store,node,index,filepath=''):
    print("writing node file...")
    try:
        if(node.log_path != ""):
            logData = pd.read_csv(node.log_path,sep='\t')
            if (list(logData).pop() == 'Unnamed: 7'):
                del logData['Unnamed: 7']
            #store['log'+ str(index)] = logData;
            logData.to_hdf(filepath,'log'+ str(index),complevel=9,complib='zlib')
            #__write_node_metadata(store,'log'+str(index), __file_name(node.log_path) )
            print('Writing log'+str(index))
        if(node.bin_path != "")  : 
            binData = pd.Series(np.fromfile(node.bin_path,dtype=np.float),dtype=np.float)
            print binData
            #store['bin'+ str(index)] = binData;
            
            binData.to_hdf(filepath,'bin'+ str(index),complevel=9,complib='zlib')
            #__write_node_metadata(store,'bin'+str(index),__file_name(node.bin_path))
            print('Writing bin'+str(index))  
    except IOError as e:
        traceback.print_exc()
        raise e
        
    




def generate_experiment_file(new_path, node_list, exp_notes='', overwrite = False ):
    '''
    Given Node or Node array this function creates hdf5 file filled with Node log files,bin files and node type(master/slave). 
    File must not already exist if overwrite is set to false.
    
    |  Arguments:
    |      new_path -- Path to new experiment file, file extension must end in .h5
    |          , example ..\\\\file\\\\newfile.h5
    |      node_list -- Node or Array of Nodes, it is acceptable for node to not have log, bin
    |          , or metadata (master/slave)
    |      exp_notes -- string to be stored in file as experiment notes (default = '')
    |      overwrite -- Boolean, if True Bypasses safegaurd against overwriting existing file (default = False)
        
    Throws:
        IOError -- If file at path already exists or error occurs during creation. If error occurs during
            creation the experiment file will not be generated. This could be due to invalid log/bin paths.
    '''
    print("generating...")#TODO assert h5 extension
    index = 0
    
    #Check if file at path already exists
    if( os.path.isfile(new_path) ):
        if(overwrite):
            os.remove(new_path);
        else:
            raise IOError("File %s already exists, only generate new files. This error may be suppressed by passing in overwrite = True" %(new_path))    
    
    node_types = []
    try:
                
        if hasattr(node_list, '__iter__'):
            for node in node_list:
                __write_node_files('',node,index,new_path)
                index += 1
                node_types.append(node.node_type)
        else:
            __write_node_files('',node_list,index,new_path)
            node_types.append(node.node_type)
        with pd.HDFStore(new_path) as store:     
            store['notes'] = pd.Series(exp_notes)
            store['types'] = pd.Series(node_types)
        rewrite_hdf5(os.path.relpath(new_path))
        print 'Done Rewriting'
    except IOError as e:
        if(os.path.isfile(new_path)):
            print('File created but error occured, removing partially created file.')
            os.remove(new_path);
        raise e

        
   


def rewrite_hdf5(file_in):#TODO: keep track of complevel
    '''
    Rewrites hdf5 file specified by file_in using pytables ptrepack, reclaiming unused memory and compressing the file.
    ptrepack typically results in better compression than compressing hdf5 files during generation. 
    
    |  Arguments:
    |      file_in -- Pass in relative path to hdf5 file to be rewritten, file should end in .h5
    Throws:
        ValueError -- If file_in does not end in .h5
    '''
    print file_in
    if( not file_in.endswith('.h5') ):
        raise ValueError("file_in should be path that ends with .h5 extension")
    
    file_temp = file_in[0:-3] + '_temp.h5'
    
    if( os.path.isfile(file_temp) ):
        raise IOError(file_temp + ' already exists, remove it before attempting to rewrite ' + file_in + ' again')
    
    
    command = ["ptrepack", "-o", "--chunkshape=auto", "--propindexes","--complevel=9", "--complib=zlib", file_in, file_temp]
    if( call(command) != 0 ):
        if( os.path.isfile(file_temp) ):
            os.remove(file_temp)
        raise StandardError('Issue calling ptrepack cmd, can not rewrite hdf5 to reclaim unused memory')

    os.remove(file_in)
    os.rename(file_temp,file_in)

    
        
def set_node_type(exp_path,node_index,new_type):
    '''
    Set or change the type (master,slave,'') for a node in an experiment file
    
    |  Arguments:
    |      exp_path -- path to experiment file
    |      node_index --  index of node to change type, 0 or greater
    |      new_type -- string, type should be master, slave, or empty string)
        
    Throws:
        ValueError -- if new_types does not equal master,slave, or empty string
    '''
    if new_type != 'master' and new_type != 'slave' and new_type != '':
        raise ValueError(new_type + ' must equal master, slave, or \'\'')
    with pd.HDFStore(exp_path) as store:
        types = store['types'].set_value(node_index,new_type)
        store['types']= types
        
def add_nodes(exp_path,node_list):   
    '''
    Appends Node or list of Nodes to the experiment file.
        
    |  Arguments:
    |      exp_path -- path to experiment file    
    |      node_list --  single Node or list of Nodes to append to experiment file  
        
    Throws:
        IOError -- if something bad happens
    '''  
    #TODO: find last node index
    new_index = expreader.get_number_of_nodes(exp_path)
    node_types = []
    with pd.HDFStore(exp_path) as store:
        if hasattr(node_list, '__iter__'):
            for node in node_list:
                __write_node_files(store,node,new_index)
                new_index += 1
                node_types.append(node.node_type)
        else:
            __write_node_files(store,node_list,new_index) 
            node_types.append(node_list.node_type)
       
        #Write node types
        store['types'] = store['types'].append( pd.Series(node_types) )



def set_node_file(exp_path ,node_index, file_path, is_log):
    '''
    Set/replace the log or bin file of an existing node. Don't use to create new nodes
    use add_node() to create new nodes.
    
    |  Arguments:
    |      exp_path -- path to experiment file
    |      node_index -- index of node whose file will be changed, 0 or greater
    |      file_path -- path to log/bin file being added
    |      is_log -- True if new file is log, False if new file is bin
        
    Throws:
        ValueError -- if node_index is less than 0 or larger than existing node index
    '''
    if (node_index >= expreader.get_number_of_nodes(exp_path) or node_index < 0):
        raise ValueError('node_index out of bounds only set files for nodes that exist, used add_node() to create new node')
    with pd.HDFStore(exp_path) as store:
        if is_log:
            __write_node_files(store,node.Node(log_path = file_path ),node_index)
        else:
            __write_node_files(store,node.Node(bin_path = file_path ),node_index)

    


def del_node_file(exp_path,node_index,is_log):
    '''
        Removes log/bin file from HDF5 file, if file doesn't exist doesn't exist nothing happens
        
    |  Arguments:
    |      exp_path -- path to experiment file
    |      node_index -- index of node to remove file from, 0 or greater
    |      is_log -- True to delete log, False to delete bin
    '''
    with pd.HDFStore(exp_path) as store:
        node_type = 'log' if is_log else 'bin'
        node_name = node_type + str(node_index)
        if '/'+node_name in store.keys():
            store.remove(node_type + str(node_index))
    rewrite_hdf5(os.path.relpath(exp_path))#reclaim memory


        
def del_node(exp_path,node_index):
    '''
        Given experiment file and node index, deletes the log and bin at that index if they exist. If no files at that index exist nothing happens.
        All later nodes will be shifted down 1 index so there are no gaps in numbering. For example if file has nodes: 0,1,2 then we remove 1
        -> file now has nodes: 0,1 where the node at index 1 used to be at index 2
        
        |  Arguments:
        |      exp_path -- path to experiment file
        |      node_index -- index starts from 0, index of node to get removed
    '''
    del_node_file(exp_path,node_index,True)
    del_node_file(exp_path,node_index,False)
    with pd.HDFStore(exp_path) as store:
        types = store['types']
        types.index = range(types.size)#TODO make better, this fixes holes in series indexing
        types = types.drop(node_index)
        types.index = range(types.size)
        store['types'] = types
        for key in store.keys():
            if key.startswith('/log') or key.startswith('/bin'):
                current_index = int(key[-1])
                if current_index > node_index:
                    store.get_node(key)._f_rename( key[1:len(key)-1] + str(current_index - 1) )
    rewrite_hdf5(os.path.relpath(exp_path))#reclaim memory
        
def __file_name(path):
    ntpath.basename("a/b/c")
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)        
        
        
        
        
        
        
        
        
        

    
    