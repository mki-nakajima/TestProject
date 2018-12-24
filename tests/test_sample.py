'''
Created on 2018/12/24

@author: shunsuke
'''
import unittest
from tests import utility


class Sample(object):

    def __init__(self, element1='abc', element2='123'):
        self.element1 = element1
        self.element2 = element2


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
        sample1 = Sample()
        print(sample1.__dict__)
        sample2 = Sample('qaz', 'wsx')
        print(sample2.__dict__)
        print('Test Finished.')


if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testName']
    unittest.main()