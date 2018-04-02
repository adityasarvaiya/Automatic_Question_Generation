from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import os
from aqg.app1 import Application
from aqg.utils.summarizer import TextSummarizer
from aqg.utils.pdfgenration import pdfgeneration
from aqg.utils.mail_agent import mail_agent as ma
from aqg.utils.pdfgenration import pdfgeneration as pdf

app = Flask(__name__)

@app.route('/')
def hello_world():
    return  render_template("welcome.html")

@app.route('/index4')
def hello_world8():
    return  render_template("index4.php")

@app.route('/index.html')
def hello_world1():
    return  render_template("index.html")

@app.route('/procedure.html' )
def hello_world2():
    return  render_template("procedure.html")

@app.route('/question.html',methods = ['POST', 'GET'])
def hello_world3():
    Name = request.form['Name']
    Number = request.form['Number']
    Email = request.form['Email']
    outputformat = request.form['outputformat']
    optionsRadios = request.form['optionsRadios']
    
    if(optionsRadios == "text"):
        Text1 = request.form['Text1']
        file_object = open("InputText.txt",'w')
        file_object.write(Text1)
        file_object.close()
        apps = Application()
        question_ans_dataframe = apps.ques_application("InputText.txt",outputformat,Email)
        pdf2 = pdf()
        pdf2.generate_pdf_quesans(question_ans_dataframe)
        mail_age = ma()
        mail_age.mail_pdf(Email)
        return  render_template("question.html", qad = question_ans_dataframe)


    elif(optionsRadios == "file"):
        File1 = request.files['File1']
        File1.save(secure_filename(File1.filename))
        apps = Application()
        question_ans_dataframe = apps.ques_application(File1.filename,outputformat,Email)
        pdf2 = pdf()
        pdf2.generate_pdf_quesans(question_ans_dataframe)
        mail_age = ma()
        mail_age.mail_pdf(Email)
        return  render_template("question.html", qad = question_ans_dataframe)

    elif(optionsRadios == "link"):
        Link1 = request.form['Link1']
        t  = TextSummarizer()
        t.summarize_from_url(Link1)
        apps = Application()
        question_ans_dataframe = apps.ques_application("summarizer_output.txt",outputformat,Email)
        pdf2 = pdf()
        pdf2.generate_pdf_quesans(question_ans_dataframe)
        mail_age = ma()
        mail_age.mail_pdf(Email)
        return  render_template("question.html", qad = question_ans_dataframe)

    
    return  render_template("question.html")


@app.route('/summarization.html')
def hello_world4():
    return  render_template("summarization.html")

@app.route('/summarized.html',methods = ['POST', 'GET'])
def hello_world5():

    Name = request.form['Name']
    Number = request.form['Number']
    Email = request.form['Email']
    Nolines = request.form['Nolines']
    optionsRadios = request.form['optionsRadios']
    t  = TextSummarizer(Nolines)
    
    if(optionsRadios == "text"):
        Text1 = request.form['Text1']
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
        t.summarize_from_url(Link1)
        pdf = pdfgeneration()
        pdf.generate_pdf_summarizer("summarizer_output2.txt","summarized.pdf")
        mail_age = ma()
        mail_age.mail_pdf(Email,"summarized.pdf")
        f = open("summarizer_output.txt")
        summarized_text = f.read()
        return  render_template("summarized.html", summarized_text = summarized_text)
    
    return  render_template("summarization.html")

if __name__ == '__main__':
    app.run()