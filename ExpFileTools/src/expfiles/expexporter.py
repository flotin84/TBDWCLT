'''
Created on Feb 6, 2017

@author: JRC
'''
import numpy as np
import pandas as pd
import os
from expfiles import expreader

def export_log(exp_path, dir_path ,node_index, file_name=''):
    """
    Given path to experiment file and an index of the node in the experiment file returns DataFrame of log
    An exception will be thrown if the log file is not found experiment file
   
    Arguments:
        exp_path -- path to experiment file
        new_path -- path to new log ending in file name with .txt extension
        index -- index of node, greater than 0. 
    """
    print('Exporting log of ' + str(node_index))
    if file_name == '':
        file_name = expreader.get_node_file_name(exp_path, node_index, True)
    full_path = os.path.abspath(dir_path)+ '\\' + file_name    
    print full_path
    data = pd.read_hdf(exp_path,'log' + str(node_index))
    data.to_csv(full_path,sep='\t',index=False);#TODO: check passed in names for validity on log and bin
    
'''
def export_bin(exp_path, new_path ,index,file_name=''):
    """
    Given path to experiment file and an index of the node in the experiment file returns DataFrame of bin
    An exception will be thrown if the log file is not found experiment file

    Arguments:
        exp_path -- path to experiment file
        new_path -- path to new log ending in file name with .bin extension
        index -- index of node, greater than 0
    """
    print('Exporting bin of ' + str(index))
    data = pd.read_hdf(exp_path,'bin' + str(index))
    data.to_pickle(new_path);
'''
