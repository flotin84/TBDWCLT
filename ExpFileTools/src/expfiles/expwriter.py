'''
Created on Feb 5, 2017

@author: JRC
'''
import numpy as np
import pandas as pd
from statsmodels.stats.inter_rater import fleiss_kappa
# create (or open) an hdf5 file and opens in append mode
def __write_experiment_metadata():
    print('yo')

def __get_node_metadata():
    print("getting node metadata...")    
    
def __write_node_files(filepath,node,index):
    print("writing node file...")
    store = pd.HDFStore(filepath)
    if(node.logpath != ""):
        logData = pd.read_csv(node.logpath,sep='\t')
        if (list(logData).pop() == 'Unnamed: 7'):
            del logData['Unnamed: 7']
        store['log'+ str(index)] = logData;
        print('Writing log'+str(index))
    if(node.binpath != ""): 
        binData = pd.Series(np.fromfile(node.binpath,dtype=np.uint8),dtype=np.uint8)
        store['bin'+ str(index)] = binData;
        print('Writing bin'+str(index))
    store.close()

    
#TODO: validate filename

def generate_experiment_file(new_path,node_list):
    '''
    Given Node array this function creates hdf5 file filled with Node log and bin files
    
    Arguments:
        new_path -- Path to new experiment file, file extension must end in .h5
        node_list -- Array of Nodes 
    '''
    
    print("generating...")
    index = 0
    #__write_experiment_metadata(nodelist.count)
    for node in node_list:
        __write_node_files(new_path,node,index)
        index += 1

        
'''
    

'''    
    