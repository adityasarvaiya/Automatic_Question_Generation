from flask import Flask, render_template
from aqg.app1 import Application

app = Flask(__name__)

@app.route('/')
def hello_world():
    apps = Application()
    question_ans_dataframe = apps.ques_application()
    return  render_template("index.html", qad = question_ans_dataframe)


if __name__ == '__main__':
    app.run()