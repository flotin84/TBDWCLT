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
            
        #Generate a variety of test files
        with open(self.FILE_PATH + 'dummy.h5','w') as empty_file:
            empty_file.write('test')
            
        #test logs
        test_data = pd.DataFrame(np.random.randn(10, 4), columns=['A', 'B', 'C', 'D'])
        test_data.to_csv(self.FILE_PATH+'log0.txt', sep='\t', index_label='index')
        test_data = pd.DataFrame(np.random.randn(10, 4), columns=['E', 'F', 'G', 'H'])
        test_data.to_csv(self.FILE_PATH+'log1.txt', sep='\t', index_label='index')
        test_data = pd.DataFrame(np.random.randn(10, 4), columns=['I', 'J', 'K', 'L'])
        test_data.to_csv(self.FILE_PATH+'log2.txt', sep='\t', index_label='index')
        
        #test bins
        with open(self.FILE_PATH + 'num0.bin','w') as bin:
            bin.write('0')        
        with open(self.FILE_PATH + 'num1.bin','w') as bin:
            bin.write('00')
        with open(self.FILE_PATH + 'num2.bin','w') as bin:
            bin.write('000')
            
        # dont change testing.h5
        test_nodes = [node.Node(self.FILE_PATH + 'log0.txt',self.FILE_PATH + 'num0.bin','master'),node.Node(self.FILE_PATH + 'log1.txt',self.FILE_PATH + 'num1.bin','slave'),node.Node(self.FILE_PATH + 'log2.txt',self.FILE_PATH + 'num2.bin','master')]
        path = self.FILE_PATH + 'testing.h5'
        expwriter.generate_experiment_file(path, test_nodes)
        print 'SET UP SUCCESSCFUL'
        
    def tearDown(self):
        if os.path.exists(self.FILE_PATH):
            shutil.rmtree(self.FILE_PATH)
            self.assertFalse(os.path.exists(self.FILE_PATH),'Tear down failed to remove test files')
        print 'TEAR DOWN SUCCESSCFUL'
        
    def test_IOErrors(self):
        #Should throw error if exp file already exists
        with self.assertRaises(IOError):
            expwriter.generate_experiment_file(self.FILE_PATH + 'dummy.h5', '')
        #Should not throw error is overwirte is set to True
        #expwriter.generate_experiment_file( self.FILE_PATH + 'dummy.h5', node.Node(self.FILE_PATH + 'log.txt',self.FILE_PATH + 'num.bin','master'), True)
               
        #Should throw error if log file path is not valid
        with self.assertRaises(IOError):
            expwriter.generate_experiment_file(self.FILE_PATH + 'testlogfailgen555.h5', node.Node('doesntexist333.txt'))
        self.assertFalse( os.path.isfile(self.FILE_PATH + 'testlogfailgen555.h5') )#File should not of been generated
        
        #Shoud throw error if bin file path is not valid
        with self.assertRaises(IOError):
            expwriter.generate_experiment_file(self.FILE_PATH + 'testbinfailgen555.h5', node.Node(self.FILE_PATH + 'log.txt','doesNotExist.bin'))
        self.assertFalse( os.path.isfile(self.FILE_PATH + 'testbinfailgen555.h5') )#File should not of been generated
    
    def test_del_node_file(self):#test is dependent on test_succ_gen
        pd.read_hdf(self.FILE_PATH + 'testing.h5' , 'log0' )
        expwriter.del_node_file(self.FILE_PATH + 'testing.h5', 0 , True)
        with self.assertRaises( KeyError ):
            pd.read_hdf(self.FILE_PATH + 'testing.h5' , 'log0' )
        pd.read_hdf(self.FILE_PATH + 'testing.h5' , 'bin0' )
        expwriter.del_node_file(self.FILE_PATH + 'testing.h5', 0 , False)
        with self.assertRaises( KeyError ):
            pd.read_hdf(self.FILE_PATH + 'testing.h5' , 'bin0' )
        pd.read_hdf(self.FILE_PATH + 'testing.h5' , 'bin1' )
      
    def test_del_node(self):
        test_path = self.FILE_PATH + 'testing.h5';
        
        #del middle node
        expwriter.del_node(test_path, 0)        
        with self.assertRaises(KeyError ):
            pd.read_hdf(test_path, 'log2' )
        with self.assertRaises(KeyError ):
            pd.read_hdf(test_path , 'bin2' )
        self.assertEquals( list(pd.read_hdf(test_path , 'log0' )), ['index','E','F' ,'G' , 'H'] )
        self.assertEquals( list(pd.read_hdf(test_path , 'bin0' )), [48,48] ) 
        self.assertEquals( list(pd.read_hdf(test_path , 'log1' )), ['index','I','J' ,'K' , 'L'] )
        self.assertEquals( list(pd.read_hdf(test_path , 'bin1' )), [48,48,48] )    
            
        #del last node
        expwriter.del_node(test_path, 1)    
        with self.assertRaises(KeyError ):
            pd.read_hdf(self.FILE_PATH + 'testing.h5' , 'log1' )
        with self.assertRaises(KeyError ):
            pd.read_hdf(self.FILE_PATH + 'testing.h5' , 'bin1' )
        self.assertEquals( list(pd.read_hdf(test_path , 'log0' )), ['index','E','F' ,'G' , 'H'] )
        self.assertEquals( list(pd.read_hdf(test_path , 'bin0' )), [48,48] ) 
        
        #del node that doesn't exist
        expwriter.del_node(test_path, 2)    
        with self.assertRaises(KeyError ):
            pd.read_hdf(self.FILE_PATH + 'testing.h5' , 'log1' )
        with self.assertRaises(KeyError ):
            pd.read_hdf(self.FILE_PATH + 'testing.h5' , 'bin1' )
        self.assertEquals( list(pd.read_hdf(test_path , 'log0' )), ['index','E','F' ,'G' , 'H'] )
        self.assertEquals( list(pd.read_hdf(test_path , 'bin0' )), [48,48] ) 

        
            
    def test_succ_gen(self):
        test_nodes = [node.Node(self.FILE_PATH + 'log0.txt',self.FILE_PATH + 'num0.bin','master'),node.Node(self.FILE_PATH + 'log1.txt',self.FILE_PATH + 'num1.bin','slave')]
        path = self.FILE_PATH + 'testExp1.hdf'
        expwriter.generate_experiment_file(path, test_nodes)
        self.assertTrue( os.path.isfile(path) )
        self.assertEquals( list(pd.read_hdf(path , 'log0' )), ['index','A','B' ,'C' , 'D'] )

    

    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()