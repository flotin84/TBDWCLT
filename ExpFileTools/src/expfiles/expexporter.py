'''
Created on Feb 6, 2017

@author: JRC
'''
import numpy as np
import pandas as pd
import os
import expreader


def export_log(exp_path, new_path ,node_index):
    '''
    The log file at the associated node_index is exported as a tab delimited csv at new_path
   
    |  Arguments:
    |      exp_path -- path to experiment file
    |      new_path -- path to place exported file, ex C:\\\\User\\\\Jack\\\\exported_files\\\\test.txt 
    |          or C:\\\\User\\\\Jack\\\\exported_files\\\\test.txt  or ..\\\\files\\\\test.txt   use single slashes
    |      index -- index of node to export, 0 or greater. 
    '''
    print('Exporting log of ' + str(node_index))
    data = pd.read_hdf(exp_path,'log' + str(node_index))
    data.to_csv(new_path,sep='\t',index=False);#TODO: check passed in names for validity on log and bin
    

def export_bin(exp_path, new_path ,index):
    '''
    The bin file at the associated node_index is exported as a binary file of 64-bit floating point values 
    at new_path
        Arguments:
    |      exp_path -- path to experiment file
    |      new_path -- path to place exported file, ex C:\\\\User\\\\Jack\\\\exported_files\\\\test.bin 
    |          or C:\\\\User\\\\Jack\\\\exported_files\\\\test.bin  or ..\\\\files\\\\test.bin   use single slashes
    |      index -- index of node to export, 0 or greater. 
    '''
    print('Exporting bin of ' + str(index))
    data = pd.read_hdf(exp_path,'bin' + str(index))
    data.as_matrix().tofile(new_path)

