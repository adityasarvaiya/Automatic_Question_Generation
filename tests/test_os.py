import unittest 
import os
import sys
sys.path.append('..')
from aqg.utils.file_reader import File_Reader
from aqg.utils.file_writer import File_Writer

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class TestOS(unittest.TestCase):
    def test_reader(self):
        test_path = os.path.dirname(os.path.realpath(__file__))
        fr = File_Reader()
        self.assertIsInstance(fr.read_file(test_path+'/obama.txt'), str)

    def test_writer(self):
    	fw = File_Writer()
    	fw.write_candidate_questions("test", os.path.dirname(__file__) + 'test.txt')
    	with open(os.path.dirname(__file__) + 'test.txt', 'r') as f:
    		self.assertEqual(f.readline().replace('"',''), "test")
        os.remove(os.path.dirname(__file__) + 'test.txt')


if __name__ == '__main__':
	unittest.main()
        
        
