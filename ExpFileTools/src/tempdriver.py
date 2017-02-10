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

node_list = [node.Node( TEST_FILES_PATH + "log.txt", TEST_FILES_PATH + "Sinusoid.bin"),node.Node( TEST_FILES_PATH + "log.txt", TEST_FILES_PATH + "Sinusoid.bin")]
exp_path =  EXPERIMENT_PATH + 'testexp.h5';
expwriter.generate_experiment_file(exp_path, node_list)

expexporter.export_bin(exp_path, EXPORT_PATH + 'exportedlog1.txt',1)
print ( expreader.get_node_file(exp_path, 1, True) )
