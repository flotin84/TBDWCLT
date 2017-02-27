'''
Created on Feb 5, 2017

@author: JRC
'''

#from expfiles import expfilegenerator as gen
import numpy as np
import pandas as pd
from expfiles import *

# Do this to not have to write expreader/expwriter
from expfiles import expreader as er
from expfiles import expwriter as ew

EXPORT_PATH = '../files/exportedfiles/'
EXPERIMENT_PATH = '../files/generatedfiles/'
TEST_FILES_PATH = '../files/testfiles/'
exp_path =  EXPERIMENT_PATH + 'testexpbin2.h5';


node_list = [ node.Node( TEST_FILES_PATH + "log.txt", TEST_FILES_PATH + "Sinusoid.bin", 'slave'),node.Node( TEST_FILES_PATH + "log.txt", TEST_FILES_PATH + "Sinusoid.bin", 'master')]
node2 = node.Node(TEST_FILES_PATH + "log.txt", TEST_FILES_PATH + "Sinusoid.bin", 'master')

print "Running Example...\n"

#generates experiment file with overwriting has node 0 and node 1
ew.generate_experiment_file(exp_path, node_list, 'My experiment notes', True)

#Add node 2
print '\n\nBefore there are ' + str( er.get_number_of_nodes(exp_path) )  + ' nodes'
ew.add_nodes(exp_path, node2 )
print 'After add there are ' + str( er.get_number_of_nodes(exp_path) )  + ' nodes'

#Delete node 2
ew.del_node(exp_path, 2)
print 'After del there are ' + str( er.get_number_of_nodes(exp_path) )  + ' nodes'


#Delete log file of first node
print '\n\nBefore del log, node0 has log? ' + str( er.has_log_file(exp_path, 0) )
ew.del_node_file(exp_path, 0, True)
print 'After del log, node0 has log? ' + str( er.has_log_file(exp_path, 0) )

#Add back log file to first node
ew.set_node_file(exp_path, 0, TEST_FILES_PATH + "log.txt" , True)
print 'After add log, node0 has log? ' + str(er.has_log_file(exp_path, 0))


# change first node to slave
ew.set_node_type(exp_path,0, 'slave')


print "\nNode 0 info"
#Print some first node info
print er.get_node_type(exp_path, 0)
print er.get_node_file_name(exp_path, 0, True)
print er.get_node_file(exp_path, 0, True)



