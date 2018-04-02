from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
#from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


class TextSummarizer:

    def __init__(self, count=10):
        self.LANGUAGE = "czech"
        self.SENTENCES_COUNT = count


    def summarize_from_url(self,url):

        parser = HtmlParser.from_url(url, Tokenizer(self.LANGUAGE))
        stemmer = Stemmer(self.LANGUAGE)
        summarizer = Summarizer(stemmer)
        file_1 = open("summarizer_output.txt","w+")
        file_2 = open("summarizer_output2.txt","w+")
        for sentence in summarizer(parser.document, self.SENTENCES_COUNT):
            file_2.write(str(sentence))
            file_1.write(str(sentence))
            file_1.write("\n")
        file_1.close()
        file_2.close()


    def summarize_from_text(self,text):

        parser = PlaintextParser.from_string(text, Tokenizer(self.LANGUAGE))
        stemmer = Stemmer(self.LANGUAGE)
        summarizer = Summarizer(stemmer)
        
        file_1 = open("summarizer_output.txt","w+")
        file_2 = open("summarizer_output2.txt","w+")
        for sentence in summarizer(parser.document, self.SENTENCES_COUNT):
            file_2.write(str(sentence))
            file_1.write(str(sentence))
            file_1.write("\n")
        file_1.close()
        file_2.close()


    def summarize_from_file(self,file_name):

        parser = PlaintextParser.from_file(file_name, Tokenizer(self.LANGUAGE))
        stemmer = Stemmer(self.LANGUAGE)
        summarizer = Summarizer(stemmer)
        file_1 = open("summarizer_output.txt","w+")
        file_2 = open("summarizer_output2.txt","w+")
        for sentence in summarizer(parser.document, self.SENTENCES_COUNT):
            file_2.write(str(sentence))
            file_1.write(str(sentence))
            file_1.write("\n")
        file_1.close()
        file_2.close()






# t  = TextSummarizer()
# t.summarize_from_file("obama_short.txt")
# pdf = pdfgeneration()
# pdf.generate_pdf_summarizer("summarizer_output2.txt")
