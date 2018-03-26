# -*- coding: utf-8 -*-

import nltk,re
from nltk.tree import Tree

"""
this page will have all the possible chunks on the basis of which we will create the full questions
"""
class Actual_Question_Formation:
    def tree_to_dict1(self, tree):
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
                    print " before : ",tree_dict[st.label()]
                    tree_dict[st.label()] = tree_dict[st.label()] + " " +input_chunked
                    print " after : ",tree_dict[st.label()]
                    
                else:
                    tree_dict[st.label()] = input_chunked
        return tree_dict


    def pattern_noun_verb(self, sent, jsondata):
        """
        Aditya : Takes the sentence and find the chunk (matches the regex)
        input : sentence
        output : chuncked short sentence
        """
        words = nltk.word_tokenize(sent)
        tagged = nltk.pos_tag(words)

        
        chunkGram = 'Chunk: {<VB.?>+<NN.?>+}'
        chunkParser = nltk.RegexpParser(chunkGram)
        chunked = chunkParser.parse(tagged)
        chunked.draw()
        # chunked = nltk.ne_chunk(tagged)
        chunk = self.tree_to_dict1(chunked)
        
        if chunk.has_key("Chunk"):
            pattern_string = chunk["Chunk"]
            print "pattern_string  :  ", str(pattern_string)
        else:
            pattern_string = "" 
        return pattern_string

        
    def form_full_questions(self,candidate,jsondata,tagged):
        pattern_string = self.pattern_noun_verb(candidate['Sentence'],jsondata)
        full_ques = candidate['Question']
        sentence = candidate['Sentence']
        flag = 0
        if (len(pattern_string)>0):
            for word,pos in tagged:    
                if ((str(candidate['Answer']).find(word)) >= 0):
                    if ((('NN' == pos) or ('NNP' == pos) or ('NNPS' == pos)) and jsondata.has_key("PERSON")) and (word in jsondata['PERSON']):
                        individual_words = pattern_string.split()
                        verb = [word for word in individual_words if word not in jsondata['PERSON']]
                        print "Verb : ", str(verb)
                        full_ques = sentence.replace( pattern_string , '')
                        full_ques = "What " + str(verb[0]) + " " + str(full_ques).lower() + "?"
                        print "word : " + word + "  pos : " + pos
                        flag=1

        return full_ques, flag
    
# if __name__ == '__main__':
#     form_full_questions("Ahmedabad is walking run a very good city")