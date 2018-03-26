# -*- coding: utf-8 -*-
import nltk
import re

def tree_to_dict(self, tree):
    tree_dict = dict()
    for st in tree:
        # not everything gets a NE tag,
        # so we can ignore untagged tokens
        # which are stored in tuples
        if isinstance(st, nltk.Tree):
            if st.label() in tree_dict:
                tree_dict[st.label()] = tree_dict[st.label()] + [st[0][0]]
            else:
                tree_dict[st.label()] = [st[0][0]]
    return tree_dict


i = "Mixture of some elements is water."
words = nltk.word_tokenize(i)
tagged = nltk.pos_tag(words)
chunkGram = r"""Chunk: {<NN>?}"""
chunkParser = nltk.RegexpParser(chunkGram)
chunked = chunkParser.parse(tagged)
print tree_to_dict(chunked)



from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP(r'G:\JavaLibraries\stanford-corenlp-full-2017-06-09')

sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
print 'Tokenize:', nlp.word_tokenize(sentence)
print 'Part of Speech:', nlp.pos_tag(sentence)
print 'Named Entities:', nlp.ner(sentence)
print 'Constituency Parsing:', nlp.parse(sentence)
print 'Dependency Parsing:', nlp.dependency_parse(sentence)

nlp.close()


import nltk 
print nltk.sent_tokenize("For a non-technical introduction to the topic, see Introduction to genetics. For other uses, see DNA (disambiguation).The structure of the DNA double helix. The atoms in the structure are colour-coded by element and the detailed structures of two base pairs are shown in the bottom right.The structure of part of a DNA double helixDeoxyribonucleic acid (/diˈɒksiˌraɪboʊnjʊˌkliːɪk, -ˌkleɪɪk/ (About this sound listen);[1] DNA) is a thread-like chain of nucleotides carrying the genetic instructions used in the growth, development, functioning and reproduction of all known living organisms and many viruses. DNA and ribonucleic acid (RNA) are nucleic acids; alongside proteins, lipids and complex carbohydrates (polysaccharides), they are one of the four major types of macromolecules that are essential for all known forms of life. Most DNA molecules consist of two biopolymer strands coiled around each other to form a double helix.The two DNA strands are called polynucleotides since they are composed of simpler monomer units called ")



import nltk,re
from nltk.tree import Tree

"""
this page will have all the possible chunks on the basis of which we will create the full questions
"""

def tree_to_dict(tree):
    """
    Aditya : Convert Tree to a usefull dict[] = <list> format
    input : tree
    output : dictionary
    
    """
    tree_dict = dict()
    for st in tree:
        # not everything gets a NE tag,
        # so we can ignore untagged tokens
        # which are stored in tuples
        if isinstance(st, nltk.Tree):
            
            input_chunked = ""
            for d in range(len(st)):
                if (d+1) == len(st):
                    input_chunked = input_chunked + st[d][0]
                else:
                    input_chunked = input_chunked + st[d][0] + " "
        
            if st.label() in tree_dict:
                print "st.label() : "
                print st.label()
                print "tree.dict : "
                print tree.dict
                tree_dict[st.label()].append(input_chunked)
            else:
                tree_dict[st.label()] = input_chunked
    return tree_dict


def form_full_questions(sent):
    """
    Aditya : Takes the sentence and find the chunk (matches the regex)
    input : sentence
    output : chuncked short sentence
    """
    words = nltk.word_tokenize(sent)
    tagged = nltk.pos_tag(words)

    chunkGram = 'Chunk: {"Aditya"}'
    chunkParser = nltk.RegexpParser(chunkGram)
    chunked = chunkParser.parse(tagged)
    chunked.draw()
    # chunked = nltk.ne_chunk(tagged)
    chunk = tree_to_dict(chunked)
    print chunk["Chunk"]
        
        
    
if __name__ == '__main__':
    form_full_questions("")

st = "thismyhome"
print st[:5]
