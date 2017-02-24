'''
Created on Feb 18, 2017

@author: JRC
'''
import unittest
import os
import shutil
import numpy as np
import pandas as pd
import expfiles.expwriter as expwriter
import expfiles.node as node
'''
If file alread exists throw exception
If error occurs during creation file is not gened
'''

class TestExpGenerator(unittest.TestCase):
    FILE_PATH = '../../files/unittestfiles/'
    def setUp(self):
        if not os.path.exists(self.FILE_PATH):
            os.makedirs(self.FILE_PATH)   
        empty = open(self.FILE_PATH + 'dummy.h5','w')
        empty.close()
        test_data = pd.DataFrame(np.random.randn(10, 4), columns=['A', 'B', 'C', 'D'])
        test_data.to_csv(self.FILE_PATH+'log.txt', sep='\t', index_label='index')
        bin = open(self.FILE_PATH + 'num.bin','w')
        bin.write('2136732722383278432782243228734')
        bin.close()
        log = open(self.FILE_PATH + 'log2.txt','w')
        log.write('hello    how    are    you\n1    2    3    4')
        log.close()
        bin = open(self.FILE_PATH + 'num2.bin','w')
        bin.write('2136732722383278432782243228734')
        bin.close()
    
    
    def tearDown(self):
        if os.path.exists(self.FILE_PATH):
            shutil.rmtree(self.FILE_PATH)
    
    def test_IOErrors(self):
        #Should throw error if exp file already exists
        with self.assertRaises(IOError):
            expwriter.generate_experiment_file(self.FILE_PATH + 'dummy.h5', '')
                  
        #Should throw error if log file path is not valid
        with self.assertRaises(IOError):
            expwriter.generate_experiment_file(self.FILE_PATH + 'testlogfailgen555.h5', node.Node('doesntexist333.txt'))
        self.assertFalse( os.path.isfile(self.FILE_PATH + 'testlogfailgen555.h5') )#File should not of been generated
        
        #Shoud throw error if bin file path is not valid
        with self.assertRaises(IOError):
            expwriter.generate_experiment_file(self.FILE_PATH + 'testbinfailgen555.h5', node.Node(self.FILE_PATH + 'log.txt','doesNotExist.bin'))
        self.assertFalse( os.path.isfile(self.FILE_PATH + 'testbinfailgen555.h5') )#File should not of been generated
    
    
    def test_succ_gen(self):
        test_nodes = [node.Node(self.FILE_PATH + 'log.txt',self.FILE_PATH + 'num.bin','master'),node.Node(self.FILE_PATH + 'log2.txt',self.FILE_PATH + 'num2.bin','slave')]
        path = self.FILE_PATH + 'testExp1.hdf'
        expwriter.generate_experiment_file(path, test_nodes)
        self.assertTrue( os.path.isfile(path) )
        self.assertEquals( list(pd.read_hdf(path , 'log0' )), ['index','A','B' ,'C' , 'D'] )
        with self.assertRaises( KeyError ):
            pd.read_hdf(path , 'bin2')
    

    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()