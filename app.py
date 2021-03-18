import re
import pandas as pd
from flask import Flask, render_template, request, Response, redirect, flash, url_for, jsonify
import os
import json
from werkzeug.utils import secure_filename
from flask import send_from_directory
from time import sleep
import zipfile

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/tmp"
ALLOWED_EXTENSIONS = {"txt", "zip"}
path = os.getcwd()
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

remove_words = {
    "´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´": True,
    "gif": True,
    "omitted": True,
    "audio": True,
    "image": True,
    "video": True,
    " ": True,
    "jjjjj": True,
    "jjajj": True,
    "jajajajajajaja": True,
    "jajajj": True,
    "jaja": True,
    "jajaja": True,
    "jjjj": True,
    "jajajajaja": True,
    "jajajaja": True,
    "jajajajaa": True,
    "jajaj": True,
    "haha": True,
    "hahaha": True,
    "lore": True,
    "im": True,
    "pm": True,
    "multimedia": True,
    "omitido": True,
}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_zipped(file):
    return file.filename.rsplit(".", 1)[1].lower() == "zip"


def unzip_file(file):
    if file.filename.rsplit(".", 1)[1].lower() != "zip":
        return

    if file.filename.rsplit(".", 1)[1].lower() == "zip":
        filename = secure_filename(file.filename)
        with zipfile.ZipFile(
            os.path.join(app.config["UPLOAD_FOLDER"], filename), "r"
        ) as zipObj:
            zipObj.extractall(app.config["UPLOAD_FOLDER"])
            print(filename)
        return zipObj.namelist()[0]
    return

def message_count_to_trace(messages):
    traces = []
    
    for key, value in messages.items():
        trace = {
            "x": key,
            "y": value,
            "name": key,
            "type": 'bar'
            }
        traces.append(trace)
    return json.dumps(traces)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if is_zipped(file):
                file.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"], "_".join(file.filename.split(" "))
                    )
                )
                filename = unzip_file(file)
            else:
                filename = secure_filename("_".join(file.filename.split(" ")))
                print(filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            words, traces, average_words, total_words = analyze_chat(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            return render_template("home.html", words=words, traces=traces, average_words=average_words, total_words=total_words)

    return render_template("error.html")

def internationalization(file):
    expression = None
    us_expression = r"(?<=\s[A-Z][A-Z]]\s)[^:\]]+"
    international_expression = r"(?<=\d:\d\d\s[-]\s)[^:\]]+"
    with open(file, encoding="utf8") as f:
        lines = f.readlines()[0:1]
        for line in lines:
            if re.search(us_expression, str(line)):
                expression = us_expression
            else:
                expression = international_expression
    return expression

def analyze_chat(file):
    # {user: {messages: 10, broken: 3, into: 9, words: 13, with: 4, count: 2}
    # if user, add message to array, else add username with empty array
    chat = {}
    messages_count = {}
    message_lengths = {}
    last_found_name = None
    expression = internationalization(file)
    with open(file, encoding="utf8") as f:
        lines = f.readlines()[1:]
        # Go through each line in the chat and check if it is a new message
        for line in lines:
            # some lines are not new messages or are blank so a search is done to find the timestamp and name to verify it is a new message
            # and if the message is new it is added to the count
            name = re.search(expression, str(line))
            if name:
                last_found_name = name
                if name.group() in messages_count:
                    messages_count[name.group()] += 1
                else:
                    messages_count[name.group()] = 1
            else:
                name = last_found_name
                
            # deconstruct each line to get a count of each word in the line for word counts, word totals, and averages
            if name and line:
                try:
                    words = str(line).split(f" {name.group()}: ")[1].split(" ")
                    if name.group() in message_lengths:
                        message_lengths[name.group()].append(len(words))
                    else:
                        message_lengths[name.group()] = [len(words)]
                    for word in words:
                        new_word = "".join([i.lower() for i in word if i.isalpha()])
                        new_word = new_word.replace(r"/[!\.,:;\?]/g", "")
                        if (
                            new_word.lower() not in remove_words
                            and 32 >= len(new_word) >= 1
                        ):
                            if name.group(0) in chat:
                                if new_word in chat[name.group(0)]:
                                    chat[name.group(0)][new_word] += 1
                                else:
                                    chat[name.group(0)][new_word] = 1
                            else:
                                chat[name.group(0)] = {new_word: 1}
                except IndexError:
                    pass
    average_words_per_message = message_length_averages(message_lengths)
    total_words = total_words_per_user(average_words_per_message, messages_count)
    return chat, message_count_to_trace(messages_count), average_words_per_message, total_words

def total_words_per_user(average_words_per_message, message_count):
    total_words = {}
    for user in average_words_per_message.keys():
        total_words[user] = round(average_words_per_message[user] * message_count[user])
    return total_words

def message_length_averages(message_lengths_dict):
    new_dict = {}
    for key, value in message_lengths_dict.items() :
        new_dict[key] = round(sum(value)/len(value), 2)
    return new_dict


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("home.html", words={}, traces={})


if __name__ == "__main__":
    app.run(port=5000)
