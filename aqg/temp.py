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


#    for num,que in enumerate(question_ans_dataframe):
#             tmp_list = []
#             temp_df = pd.DataFrame()
#             if outputformat == str("fullqus"):
#                 if que["flag"] == 1 :
#                     temp_df = pd.DataFrame([que["Full_qus"][0],que["Answer"]],columns= ["Full_ques", "Answer"])
#                     new_data_frame.append(temp_df)
#                     count+=1
#             if outputformat == "blanks1":
#                 new_data_frame.insert(count,"Full_ques",que["Question"])
#                 new_data_frame.insert(count,"Answer",que["Answer"])
#                 count+=1
#             if outputformat == "both1":
#                 new_data_frame.insert(count,"Full_ques",que["Full_qus"])
#                 new_data_frame.insert(count,"Answer",que["Answer"])
#                 count+=1




@app.route('/summarized.html',methods = ['POST', 'GET'])
def hello_world5():

    Name = request.form['Name']
    Number = request.form['Number']
    Email = request.form['Email']
    outputformat = request.form['outputformat']
    optionsRadios = request.form['optionsRadios']
    
    if(optionsRadios == "text"):
        Text1 = request.form['Text1']
        t  = TextSummarizer()
        t.summarize_from_text(Text1)
        pdf = pdfgeneration()
        pdf.generate_pdf_summarizer("summarizer_output2.txt","summarized.pdf")
        mail_age = ma()
        mail_age.mail_pdf(Email,"summarized.pdf")
        f = open("summarizer_output.txt")
        summarized_text = f.read()
        return  render_template("summarized.html", summarized_text = summarized_text)


    elif(optionsRadios == "file"):
        File1 = request.files['File1']
        File1.save(secure_filename(File1.filename))
        t  = TextSummarizer()
        t.summarize_from_file(File1.filename)
        pdf = pdfgeneration()
        pdf.generate_pdf_summarizer("summarizer_output2.txt","summarized.pdf")
        mail_age = ma()
        mail_age.mail_pdf(Email,"summarized.pdf")
        f = open("summarizer_output.txt")
        summarized_text = f.read()
        return  render_template("summarized.html", summarized_text = summarized_text)
    

    elif(optionsRadios == "link"):
        Link1 = request.form['Link1']
        t  = TextSummarizer()
        t.summarize_from_url(Link1)
        pdf = pdfgeneration()
        pdf.generate_pdf_summarizer("summarizer_output2.txt","summarized.pdf")
        mail_age = ma()
        mail_age.mail_pdf(Email,"summarized.pdf")
        f = open("summarizer_output.txt")
        summarized_text = f.read()
        return  render_template("summarized.html", summarized_text = summarized_text)
    
    return  render_template("summarization.html")