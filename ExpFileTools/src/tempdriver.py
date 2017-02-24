'''
Created on Feb 5, 2017

@author: JRC
'''

#from expfiles import expfilegenerator as gen
import numpy as np
import pandas as pd
from expfiles import *

EXPORT_PATH = '../files/exportedfiles/'
EXPERIMENT_PATH = '../files/generatedfiles/'
TEST_FILES_PATH = '../files/testfiles/'

print("Running test...")

node_list = [ node.Node( TEST_FILES_PATH + "log.txt", TEST_FILES_PATH + "Sinusoid.bin", 'slave'),node.Node( TEST_FILES_PATH + "log.txt", TEST_FILES_PATH + "Sinusoid.bin", 'master')]
node_list = node.Node(bin_path = TEST_FILES_PATH + "Sinusoid.bin") 
exp_path =  EXPERIMENT_PATH + 'testexpbin2.h5';
expwriter.generate_experiment_file(exp_path, node_list)

#expexporter.export_log(exp_path, EXPORT_PATH + 'exportedlog.txt',1)
#print ( expreader.get_node_file(exp_path, 1, True) )
#expwriter.modify_node(exp_path, [ node.Node(TEST_FILES_PATH + "log.txt", TEST_FILES_PATH + "Sinusoid.bin", 'slave')] )
#expexporter.export_log(exp_path, EXPORT_PATH + 'exportedlogmodified.txt',1)
