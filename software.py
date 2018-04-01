from flask import Flask, render_template, redirect, url_for, request
from aqg.app1 import Application

app = Flask(__name__)

@app.route('/')
def hello_world():
    return  render_template("welcome.html")

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
        

    elif(optionsRadios == "file"):
        File1 = request.form['File1']
        apps = Application()
        question_ans_dataframe = apps.ques_application(File1,outputformat)
        return  render_template("question.html", qad = question_ans_dataframe)

    elif(optionsRadios == "link"):
        Link1 = request.form['Link1']
    
    return  render_template("question.html")

@app.route('/summarization.html')
def hello_world4():
    return  render_template("summarization.html")

if __name__ == '__main__':
    app.run()