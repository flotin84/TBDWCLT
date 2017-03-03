'''
Created on Feb 6, 2017

@author: JRC
'''
import numpy as np
import pandas as pd
import os
import expreader

def export_log(exp_path, dir_path ,node_index, file_name=''):
    """
    The log file at the associated node_index is exported as a tab delimited csv with the same name it had before being
    placed in the experiment file. Unless alternative file_name is specified. 
   
    |  Arguments:
    |      exp_path -- path to experiment file
    |      dir_path -- path to directory to place exported file, ex C:\\\\User\\\\Jack\\\\exported_files 
    |          or C:\\\\User\\\\Jack\\\\exported_files\\\\ or ..\\\\files  use single slashes
    |      index -- index of node to export, 0 or greater. 
    |      file_name -- if no file name is given the original log file name is used
    """
    print('Exporting log of ' + str(node_index))
    if file_name == '':
        file_name = expreader.get_node_file_name(exp_path, node_index, True)
    full_path = os.path.abspath(dir_path) 
    if full_path.endswith('\\'):
        full_path = full_path + file_name
    else:
        full_path = full_path + '\\' + file_name    
    data = pd.read_hdf(exp_path,'log' + str(node_index))
    data.to_csv(full_path,sep='\t',index=False);#TODO: check passed in names for validity on log and bin
    
'''
def export_bin(exp_path, new_path ,index,file_name=''):

    Given path to experiment file and an index of the node in the experiment file returns DataFrame of bin
    An exception will be thrown if the log file is not found experiment file



    print('Exporting bin of ' + str(index))
    data = pd.read_hdf(exp_path,'bin' + str(index))
    data.to_pickle(new_path);
'''
