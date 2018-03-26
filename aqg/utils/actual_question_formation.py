# -*- coding: utf-8 -*-

import nltk,re
from nltk.tree import Tree

"""
this page will have all the possible chunks on the basis of which we will create the full questions
"""
class Actual_Question_Formation:
    def tree_to_dict(self, tree):
        """
        Aditya : Convert Tree to a usefull dict[] = <list> format
        input : tree
        output : dictionary
        
        """
        tree_dict = dict()
        chunk_count = 0
        for st in (tree):
            
            # not everything gets a NE tag,
            # so we can ignore untagged tokens
            # which are stored in tuples
            input_chunked = ""
            if isinstance(st, nltk.Tree):
                print(len(st))
                input_chunked = ""
                for d in range(len(st)):
                    print "input__chunked"+input_chunked
                    if (d+1) == len(st):
                        input_chunked = input_chunked + st[d][0]
                    else:
                        input_chunked = input_chunked + st[d][0] + " "
                chunk_count +=1
                # if st.label() in tree_dict:
                #     print " before : ",tree_dict[st.label()+str(num)]
                #     tree_dict[st.label()+str(num)] = tree_dict[st.label()] + " " +input_chunked
                #     print " after : ",tree_dict[st.label()]
                    
                # else:
                
                print(st.label())
                tree_dict["Chunk"+str(chunk_count)] = input_chunked
        print(tree_dict)
        return tree_dict


    def pattern_verb_noun(self, sent, jsondata):
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
        print("Here we are")
        print(chunked)
        chunked.draw()
        # chunked = nltk.ne_chunk(tagged)
        chunk = self.tree_to_dict(chunked)
        pattern_strings =[]
        if len(chunk) != 0:
            for chunk_no in range(len(chunk)):

                pattern_string = chunk["Chunk"+str(chunk_no+1)]
                pattern_strings.append(pattern_string)
                print "pattern_string  :  ", str(pattern_string)
         
        return pattern_strings

        
    def form_full_questions(self,candidate,jsondata,tagged):
        pattern_strings = self.pattern_verb_noun(candidate['Sentence'],jsondata)
        full_ques = candidate['Question']
        new_full_ques = []
        sentence = candidate['Sentence']
        answer = candidate['Answer']
        flag = 0
        if (len(pattern_strings)>0):
            for pattern_string_no in range(len(pattern_strings)):
                for word,pos in tagged:    
                    if ((str(candidate['Answer']).find(word)) >= 0):
                        if ((('NN' == pos) or ('NNP' == pos) or ('NNPS' == pos)) and jsondata.has_key("PERSON")) and (word in jsondata['PERSON']):
                            individual_words = pattern_strings[pattern_string_no].split()
                            verb = [word for word in individual_words if word not in jsondata['PERSON']]
                            print "Verb : ", str(verb)
                            full_ques = sentence.replace( pattern_strings[pattern_string_no] , '')
                            full_ques = "What " + str(verb[0]) + " " + str(full_ques).lower() + "?"
                            print "word : " + word + "  pos : " + pos
                            flag=1
                new_full_ques.append(full_ques)
                        
        print(new_full_ques)
        return new_full_ques, flag
    
# if __name__ == '__main__':
#     form_full_questions("Ahmedabad is walking run a very good city")