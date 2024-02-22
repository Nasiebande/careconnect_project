from flask import Flask, render_template
import datetime
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html',  utc_dt=datetime.datetime.utcnow())

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/comments/')
def comments():
    comments = ['This is the first comment.',
                'This is the second comment.',
                'This is the third comment.',
                'This is the fourth comment.'
                ]

    return render_template('comments.html', comments=comments)

@app.route('/capitalize/<word>/')
def capitalize(word):
    return '<h1>{}</h1>'.format(escape(word.capitalize()))