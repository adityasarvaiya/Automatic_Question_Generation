# -*- coding: utf-8 -*-
import re, nltk
from actual_question_formation import Actual_Question_Formation
#nltk.download('maxent_ne_chunker')
#nltk.download('words')

class QuestionFormation:
    
    def __init__(self):
        pass
    
    def tree_to_dict(self, tree):
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


    
    def form_questions(self,candidates,outputformat):
        """Ques formation
        - Args:
            df(pandas.dataframe): dataframe of df[['Question', 'Answer', 'Sentence','Prediction']] 
        - Returns:
            question_answers(pandas.dataframe): Full_qus, Question, Answer, Prediction, Sentence
            """
        
        print "From Ques formatrion"

        aqf = Actual_Question_Formation()
        
        candidates1 = []
        df = {}
        for index, candidate in candidates.iterrows():
            # print "candidate : "
            # print candidate
            # print candidate['Answer']
            # sentence_copy = candidate['Question']
            
            print "outputformat :" , outputformat

            tokens = nltk.word_tokenize(str(candidate['Sentence']))
            tagged = nltk.pos_tag(tokens)
    
            ne_chunk = nltk.ne_chunk(tagged)
            # print ne_chunk
            jsondata = self.tree_to_dict(ne_chunk)
            print jsondata
            
            full_ques, ans, flag = aqf.form_full_questions(candidate,jsondata,tagged)                
            
            print "full_ques is " 
            print full_ques
            
            if str(outputformat) == "fullqus":
                if flag == 1:
                    df['Full_qus'] = full_ques[0]
                    if ans == 0:
                        df['Answer'] = candidate['Answer']
                    else:
                        df['Answer'] = ans
            
            if str(outputformat) == "blanks":
                # if flag == 0:
                df['Full_qus'] = candidate['Question']
                if ans == 0:
                    df['Answer'] = candidate['Answer']
                else:
                    df['Answer'] = ans

            if str(outputformat) == "both":
                df['Full_qus'] = full_ques[0]
                if ans == 0:
                    df['Answer'] = candidate['Answer']
                else:
                    df['Answer'] = ans
                
            # df['Question'] = candidate['Question']
            
            # df['Prediction'] = candidate['Prediction']
            # df['Sentence'] = candidate['Sentence']
            # df['flag'] = flag
            if len(df.items()) != 0:
                candidates1.append(df)
            df = {}
            print " "
            print " "
        print "new final output :"
        print candidates1
        return candidates1
    
        
        
