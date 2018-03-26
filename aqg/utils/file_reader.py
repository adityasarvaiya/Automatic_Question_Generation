from os import listdir
from os.path import isfile, join


class File_Reader:


    def __init__(self):
        pass

    def read_file(self, file_name):
        '''
        @usage: read file content from current file
        @arg file_name: name of current file need to read
        @return content of current file
        '''
        with open(file_name, 'r') as f:
            return f.read().replace('\n', '')
    def read_text(self,input_text):
        return input_text.replace('\n','')
