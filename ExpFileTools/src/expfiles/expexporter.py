'''
Created on Feb 6, 2017

@author: JRC
'''
import numpy as np
import pandas as pd


def export_log(exp_path, new_path ,index):
    """
    Given path to experiment file and an index of the node in the experiment file returns DataFrame of log
    An exception will be thrown if the log file is not found experiment file
   
    Arguments:
        exp_path -- path to experiment file
        new_path -- path to new log ending in file name with .txt extension
        index -- index of node, greater than 0. 
    """
    print('Exporting log of ' + str(index))
    data = pd.read_hdf(expfilepath,'log' + str(index))
    data.to_csv(new_path,sep='\t',index=False);#TODO: check passed in names for validity on log and bin
    

def export_bin(exp_path, new_path ,index):
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

