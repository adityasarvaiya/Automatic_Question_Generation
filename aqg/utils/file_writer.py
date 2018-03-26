import os
import json


class File_Writer:

    def write_candidate_questions(self, content, file_name):
        '''
        @usage: write document length to local storage
        @arg content: content need to write
        '''
        with open(file_name, 'w') as c:
            json.dump(content, c)
