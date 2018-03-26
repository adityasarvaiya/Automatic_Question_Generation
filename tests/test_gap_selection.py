import os
import unittest 
from collections import defaultdict

import sys
sys.path.append('..')
from aqg.utils.gap_selection import GapSelection
from aqg.utils.sentence_selection import SentenceSelection

class TestGapSelection(unittest.TestCase):
    def test_parser(self):
    	gs = GapSelection()
    	parser = gs._prepare_parser()
    	self.assertIsNotNone(parser)
    	test_sentence = 'He is a nice guy from the Netherlands.'
    	parsed_sentence = gs._parse(test_sentence)
    	self.assertIsInstance(parsed_sentence, list)

    def test_gap_selection(self):
    	ss = SentenceSelection()
    	test_path = os.path.dirname(os.path.realpath(__file__))
    	semantically_important_sentences = ss.prepare_sentences(test_path+'/obama_short.txt')
    	gs = GapSelection()
    	candidate_questions = gs.get_candidates(semantically_important_sentences)
    	self.assertIsInstance(candidate_questions, list)

if __name__ == '__main__':
	unittest.main()