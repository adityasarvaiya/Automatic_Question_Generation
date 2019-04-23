import os
import unittest 
from collections import defaultdict

import sys
sys.path.append('..')
from aqg.utils.sentence_selection import SentenceSelection

class TestSentenceSelection(unittest.TestCase):
	def test_load_clean_sentence(self):
		ss = SentenceSelection()
		test_path = os.path.dirname(os.path.realpath(__file__))
		sentences = ss._load_sentences(test_path+'/obama.txt')
		self.assertIsInstance(sentences, str)
		sentences = ss._clean_sentences(sentences)
		self.assertIsInstance(sentences, dict)

	def test_prepare_sentences(self):
		ss = SentenceSelection()
		test_path = os.path.dirname(os.path.realpath(__file__))
		semantically_important_sentences = ss.prepare_sentences(test_path+'/obama.txt')
		self.assertIsInstance(semantically_important_sentences, dict)
		self.assertIsNotNone(semantically_important_sentences)
		

if __name__ == '__main__':
	unittest.main()