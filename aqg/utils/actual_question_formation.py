# -*- coding: utf-8 -*-

import nltk,re
from nltk.tree import Tree
from nltk.stem import PorterStemmer

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
                    # print " before : ",tree_dict[st.label()]
                    tree_dict[st.label()] = tree_dict[st.label()] + " " +input_chunked
                    # print " after : ",tree_dict[st.label()]
                    
                else:
                    tree_dict[st.label()] = input_chunked
        return tree_dict


    def pattern_verb_noun1(self, sent, jsondata):
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
        # chunked.draw()
        # chunked = nltk.ne_chunk(tagged)
        chunk = self.tree_to_dict(chunked)
        
        if chunk.has_key("Chunk"):
            pattern_string = chunk["Chunk"]
            print "pattern_string  :  ", str(pattern_string)
        else:
            pattern_string = "" 
        return pattern_string
    
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
                    # print "input__chunked"+input_chunked
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
        # print("Here we are")
        # print(chunked)
        # chunked.draw()
        # chunked = nltk.ne_chunk(tagged)
        chunk = self.tree_to_dict(chunked)
        pattern_strings =[]
        if len(chunk) != 0:
            for chunk_no in range(len(chunk)):

                pattern_string = chunk["Chunk"+str(chunk_no+1)]
                pattern_strings.append(pattern_string)
                print "pattern_string  :  ", str(pattern_string)
         
        return pattern_strings

    def ignore_pos(self, catch_list, tagged):
        ignore_words = [] 
        for word,pos in tagged:
            if pos in catch_list:
                ignore_words.append(word)
        return ignore_words
    
    def catch_pos(self, catch_list, tagged):
        take_words = [] 
        for word,pos in tagged:
            if pos in catch_list:
                take_words.append(word)
        return take_words

    def pattern_verb_dt_adj_noun(self, sent, jsondata):
        """
        Aditya : Takes the sentence and find the chunk (matches the regex)
        input : sentence
        output : chuncked short sentence
        """
        words = nltk.word_tokenize(sent)
        tagged = nltk.pos_tag(words)
        verbs = self.catch_pos(['VB','VBD','VBG','VBN','VBP','VBZ'],tagged)
        nouns = self.catch_pos(['NN','NNP','NNS','NNPS'], tagged)

        chunkGram = 'Chunk: {<VB.?>+<DT>?<JJ.?>?<NN.?>+}'
        chunkParser = nltk.RegexpParser(chunkGram)
        chunked = chunkParser.parse(tagged)
        # print("Here we are")
        print(chunked)
        # chunked.draw()
        # chunked = nltk.ne_chunk(tagged)
        chunk = self.tree_to_dict(chunked)
        pattern_strings =[]
        if len(chunk) != 0:
            for chunk_no in range(len(chunk)):

                pattern_string = chunk["Chunk"+str(chunk_no+1)]
                pattern_strings.append(pattern_string)
                print "pattern_string  :  ", str(pattern_string)
         
        return pattern_strings, verbs, nouns

        
    def form_full_questions(self,candidate,jsondata,tagged):
        """
        flag : is a flag to distinguis the blank ques nd actual ques 
        0 = blank ques    1 = actual ques
        ans : is a flag to keep a track of modified answer
        0 = no change in answer  
        ans = <other then 0> is the modified ans 
        """
        full_ques = candidate['Question']
        sentence = candidate['Sentence']
        answer = candidate['Answer']
        flag = 0
        ans = 0
        new_full_ques = [] 
        
        pattern_strings = self.pattern_verb_noun(candidate['Sentence'],jsondata)
        
        for word,pos in tagged:    
            # to check is word is in answer 
            if ((answer.find(word)) >= 0):
                #to check if blank is in starting 
                if (flag==0) and ((sentence.find(word))==0):
                    if ((('NN' == pos) or ('NNP' == pos) or ('NNPS' == pos)) and jsondata.has_key("PERSON")) and (word in jsondata['PERSON']):
                        full_ques = full_ques.replace("_____" , 'Who')
                        full_ques = full_ques +"?"
                        flag=1
                    elif(jsondata.has_key("LOCATION") and (word in jsondata['LOCATION'])) or (jsondata.has_key("GPE") and (word in jsondata['GPE'])):
                        
                        full_ques = full_ques.replace("_____" , 'Where')
                        full_ques = full_ques +"?"
                        flag=1
                    elif ('NN' == pos) or ('NNP' == pos) or ('NNPS' == pos):
                        full_ques = full_ques.replace("_____" , 'What')
                        full_ques = full_ques +"?"
                        flag=1

                if (flag==0 and (len(pattern_strings)>0)):
                    for pattern_string_no in range(len(pattern_strings)):
                        if ((('NN' == pos) or ('NNP' == pos) or ('NNPS' == pos)) and jsondata.has_key("PERSON")) and (word in jsondata['PERSON']):
                            individual_words = pattern_strings[pattern_string_no].split()
                            verb = [word for word in individual_words if word not in jsondata['PERSON']]
                            print "Verb : ", str(verb)
                            print "pattern_strings[pattern_string_no] : " , str(pattern_strings[pattern_string_no]) 
                            full_ques = sentence.replace(str(pattern_strings[pattern_string_no]), '')
                            full_ques = "What " + str(verb[0]) + " " + str(full_ques).lower() + "?"
                            print "word : " + word + "  pos : " + pos
                            flag=1
                            
                if (flag==0):
                    pattern_strings,verbs,nouns = self.pattern_verb_dt_adj_noun(candidate['Sentence'],jsondata)
                    print "pattern_strings : "
                    print pattern_strings
                    if (len(pattern_strings)>0):
                        if (jsondata.has_key("LOCATION") and (word in jsondata['LOCATION'])) or (jsondata.has_key("GPE") and (word in jsondata['GPE'])):
                            for pattern_string_no in range(len(pattern_strings)):
                                if (pattern_strings[pattern_string_no].find(answer)>=0):
                                    print "pattern_string_no : ", pattern_string_no
                                    individual_words = pattern_strings[pattern_string_no].split()
                                    print "individual_words :"
                                    print individual_words
                                    verb = [word for word in individual_words if word in verbs]
                                    print "Verb : ", str(verb)
                                    print "pattern_strings[pattern_string_no] : ", pattern_strings[pattern_string_no]
                                    full_ques = sentence.replace( pattern_strings[pattern_string_no] , '')
                                    full_ques = "Where " + str(verb[0]) + " " + str(full_ques).lower() + "?"
                                    
                                    noun = [word for word in individual_words if word in nouns]
                                    ps = PorterStemmer()
                                    ans = ps.stem(word)
                                    # print "word : " + word + "  pos : " + pos
                                    flag=1


        new_full_ques.append(full_ques)
        print new_full_ques
        return new_full_ques, ans, flag
    
# if __name__ == '__main__':
#     form_full_questions("Ahmedabad is walking run a very good city")