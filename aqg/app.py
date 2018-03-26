import re
import os
import sys
import json
import math
import string
import operator
from collections import defaultdict
from collections import OrderedDict

import nltk
#nltk.download("punkt")
#nltk.download("stopwords")
#nltk.download("averaged_perceptron_tagger")

import argparse
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.externals import joblib

import utils.linguistic as ling
from utils.file_reader import File_Reader
from utils.file_writer import File_Writer
from utils.gap_selection import GapSelection
from utils.sentence_selection import SentenceSelection
from utils.feature_construction import FeatureConstruction
from utils.question_formation import QuestionFormation

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def pipeline(document):
    """Pipeline of Automatic Question Generation 
    - Args:
        document(str): path of input document
    - Returns:
        question_answers(pandas.dataframe): Q/A/Prediction
    """
    # init classes
    ss = SentenceSelection()
    gs = GapSelection()
    
    # changed : aditya --  QuestionFormation() -- added
    qf = QuestionFormation()
    # build candidate questions, extract features
    sentences = ss.prepare_sentences(document)
    print sentences
    candidates = gs.get_candidates(sentences)
    print "candidates are as follows" 
    print candidates
    fc = FeatureConstruction()
    candidates_with_features = fc.extract_feature(candidates)
    question_answers1 = _classify(candidates_with_features)
    # changed : aditya
    question_answers = qf.form_questions(question_answers1)
    # question_answers = qf.form_questions(candidates)
    
    return question_answers


def _classify(df):
    """Classification
    - Args:
        df(pandas.dataframe): candidate qa pairs with extracted features 
    - Returns:
        question_answers(pandas.dataframe): Question, Answer, Prediction (label)
    """
    model_path = os.path.dirname(os.path.abspath(__file__)) + '/models/clf.pkl'
#    model_path = "%s%s" %(str(os.getcwd),"/models/clf.pkl")
    print "Your model path is"
#    print model_path
    clf = joblib.load(model_path)
    
    
    """
    Change : Aditya
    original : question_answers = df[['Question', 'Answer']]
    purpose : to add sentence in dataframe for question_formation
    """
    question_answers = df[['Question', 'Answer', 'Sentence']]
    X = df.drop(['Answer', 'Question', 'Sentence'], axis=1).as_matrix()
    y = clf.predict(X)
    question_answers['Prediction'] = y
    return question_answers


if __name__ == '__main__':
#    parser = argparse.ArgumentParser()
#    parser.add_argument("-f", "--input", help="input document")
#    args = parser.parse_args()
#    input_text = raw_input("Enter your text \n")
#    question_ans_dataframe = (pipeline(args.input))
    
    # Change : Aditya -- put file name as the argument in the following
    question_ans_dataframe = pipeline("one.txt")
    print "App.py output."
    # print(question_ans_dataframe)
    
    print "0: bad question; 1: okay question; 2: good question"
    for num,que in enumerate(question_ans_dataframe):
        print "Question Full: "+" "+str(num+1)+"    "+que["Full_qus"]+" "+"TAG:"+ str(que["Prediction"])
        print "Question Blank: "+" "+str(num+1)+"    "+que["Question"]+" "+"TAG:"+str(que["Prediction"])
        print "Answer"+" "+str(num+1)+"    "+que["Answer"]
        print " "
    
    print "0: bad question; 1: okay question; 2: good question"
