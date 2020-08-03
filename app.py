import re
import pandas as pd
from flask import Flask, render_template, request, Response, redirect, flash, url_for
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from time import sleep

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/static/files"
ALLOWED_EXTENSIONS = {'txt'}
path = os.getcwd()
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

remove_words = {"´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´":True,
                "gif":True,
                "omitted":True,
                "audio":True,
                "image":True,
                "video":True,
                " ":True,
                "jjjjj":True,
                "jajajajajajaja":True,
                "jajajj":True,
                "jaja":True,
                "jajaja":True,
                "jjjj":True,
                "jajajajaja":True,
                "jajajaja":True,
                "jajajajaa":True,
                "jajaj":True,
                "haha":True,
                "hahaha":True,
                "lore":True,
                "im":True,
                "pm":True}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            words = get_users(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("home.html", words=words)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def get_users(file):
    # {user: {messages: 10, broken: 3, into: 9, words: 13, with: 4, count: 2}
    # if user, add message to array, else add username with empty array
    chat = {}
    last_name = None
    expression = r"(?<=\s[A-Z][A-Z]]\s)[^:\]]+"
    with open(file, encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            name = re.search(expression, str(line))
            if name:
                last_name = name
            else:
                name = last_name
            if name and line:
                try:
                    words = str(line).split(f" {name.group()}: ")[1].split(" ")
                    for word in words:
                        new_word = ''.join([i.lower() for i in word if i.isalpha()])
                        if new_word.lower() not in remove_words and 32 >= len(new_word) >= 1 :
                            if name.group(0) in chat:
                                if new_word in chat[name.group(0)]:
                                    chat[name.group(0)][new_word] += 1
                                else:
                                    chat[name.group(0)][new_word] = 1
                            else:
                                chat[name.group(0)] = {new_word: 1}
                except IndexError:
                    pass

    return chat



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    get_users("static/files/" + filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename[:-3] + "csv")
                               

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/home')
def home():
    return render_template ('home.html', words={})


if __name__ == "__main__":
    app.run(port=5000)