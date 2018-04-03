from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from textwrap import wrap
from reportlab.pdfbase import pdfmetrics

class pdfgeneration:
    def __init__(self):
        pass
        
    def generate_pdf_quesans(self,df,flag_of_display = 0):
        c = canvas.Canvas("question_answer_output.pdf",pagesize=A4)
        count = 0
        textobject = c.beginText()
        print("FONTS")
        print(c.getAvailableFonts())
        textobject.setTextOrigin(0.5*inch, 9.5*inch)
        textobject.setFont("Helvetica", 13)
        count = 0 
        for num,que in enumerate(df):
            
            if flag_of_display == 0:
                pass
            if flag_of_display == 1 :
                if '_____' in que["Full_qus"][0].split():
                    continue
            que_with_num = str(num+1) + " ) "+ que["Full_qus"][0]
            if flag_of_display ==2 :
                que_with_num = str(num+1) + " ) "+ que["ques"][0]
    
            print(len(que_with_num))
            textobject.setFillGray(0)
            wraped_text = "\n     ".join(wrap(que_with_num, 70))
            textobject.textLines(wraped_text,trim = 0)
            answer = "Answer : " + que["Answer"]
            textobject.setFillGray(0.3)
            wraped_text2 = "\n".join(wrap(answer, 70))
            textobject.textLines(wraped_text2)
            textobject.textLine()
            count +=1
            if(count % 8 == 0):
                textobject2 =  c.beginText()
                textobject2.setTextOrigin(2.2*inch, 11*inch)
                textobject2.setFont("Times-Bold", 20)
                
                heading = "Automatic Question Generation"
                textobject2.textLine(heading)
                textobject2.textLine()
                c.drawText(textobject2)
                c.line(0,10.5*inch,9*inch,10.5*inch)
                
                c.drawText(textobject)
                c.showPage()
                textobject = c.beginText()
                textobject.setTextOrigin(0.5*inch, 9.5*inch)
                textobject.setFont("Helvetica", 13)
        c.drawText(textobject)
        textobject2 =  c.beginText()
        textobject2.setTextOrigin(2.2*inch, 11*inch)
        textobject2.setFont("Times-Bold", 20)
        
        heading = "Automatic Question Generation"
        textobject2.textLine(heading)
        textobject2.textLine()
        c.drawText(textobject2)
        c.line(0,10.5*inch,9*inch,10.5*inch)
        c.save()
    
    
    def generate_pdf_summarizer(self,filename,outputfile):
        c = canvas.Canvas(outputfile,pagesize=A4)
        file_2 = open(filename,"r+")
        whole_line = file_2.readline()
        words_array = whole_line.split()
        count = int(len(words_array)/350)
        for page in range(count+1):
            if count == 0:
                pass
            else:
                try :
                    whole_line = " ".join(words_array[page*350:350*(page+1)])
                except:
                    whole_line = " ".join(words_array[page*350:])

            textobject = c.beginText()
            # print("FONTS")
            # print(c.getAvailableFonts())
            textobject.setTextOrigin(0.5*inch, 9.5*inch)
            textobject.setFont("Helvetica", 13)



            textobject.setFillGray(0)
            wraped_text = "\n".join(wrap(whole_line, 70))
            textobject.textLines(wraped_text,trim = 0)
            textobject2 =  c.beginText()
            textobject2.setTextOrigin(2.2*inch, 11*inch)
            textobject2.setFont("Times-Bold", 20)

            heading = "Summarizer Output"
            textobject2.textLine(heading)
            textobject2.textLine()
            c.drawText(textobject2)
            c.line(0,10.5*inch,9*inch,10.5*inch)

            c.drawText(textobject)
            c.showPage()

        c.save()
