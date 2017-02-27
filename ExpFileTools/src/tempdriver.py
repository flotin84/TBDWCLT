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
exp_path =  EXPERIMENT_PATH + 'testexpbin2.h5';

print("Running Example...")
node_list = [ node.Node( TEST_FILES_PATH + "log.txt", TEST_FILES_PATH + "Sinusoid.bin", 'slave'),node.Node( TEST_FILES_PATH + "log.txt", TEST_FILES_PATH + "Sinusoid.bin", 'master')]
expwriter.generate_experiment_file(exp_path, node_list, 'My experiment notes', True)

#Add then delete node 2
expwriter.add_nodes(exp_path, node.Node(TEST_FILES_PATH + "log.txt", TEST_FILES_PATH + "Sinusoid.bin", 'master') )
expwriter.del_node(exp_path, 2)

#Delete log file of first node
expwriter.del_node_file(exp_path, 0, True)

#Add back log file to first node
expwriter.set_node_file(exp_path, 0, TEST_FILES_PATH + "log.txt" , True)

# change first node to slave
expwriter.set_node_type(exp_path,0, 'slave')


