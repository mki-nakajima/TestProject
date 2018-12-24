'''
Created on 2018/12/24

@author: shunsuke
'''
import unittest
from tests import utility


class Test(unittest.TestCase):


    def setUp(self):
        print('setUp start.')
        utility.copy_test_dir_before_test()
        print('setUp finished.')


    def tearDown(self):
        print('tearDown start.')
        utility.remove_test_dir_after_test()
        print('tearDown finished.')


    def testName(self):
        print('Test Start.')
        print('Test Finished.')


if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testName']
    unittest.main()