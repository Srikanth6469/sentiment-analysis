import os
import MySQLdb
import smtplib
import random
import string
from datetime import datetime
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash, send_file
from database1 import db_connect, inc_reg, ins_loginact
import pandas as pd
import io
import json
import pickle
from omicornalgo import *
from flask import Flask, request, render_template
import speech_recognition as sr
from pydub import AudioSegment
from nltk.sentiment import SentimentIntensityAnalyzer
import pymysql
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()


# Initialize Flask App
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Use the connection like this:
def db_connect():
    _conn = MySQLdb.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        passwd=os.environ["DB_PASSWORD"],
        db=os.environ["DB_NAME"]
    )
    return _conn.cursor(), _conn

# Replace MySQLdb with pymysql for compatibility
# pymysql.install_as_MySQLdb()

# def db_connect():
#     _conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="toxic")
#     c = _conn.cursor()
#     return _conn.cursor(), conn

# Configure upload location for audio
app.config['UPLOAD_FOLDER'] = "./audio"

# Define routes for the Flask application
@app.route("/")
def FUN_root():
    return render_template("index.html")

@app.route("/at.html")
def at():
    return render_template("at.html")

@app.route("/ua.html")
def ua():
    return render_template("ua.html")

@app.route("/user.html")
def ins():
    return render_template("user.html")

@app.route("/increg.html")
def increg():
    return render_template("increg.html")

@app.route("/ihome.html")
def ihome():
    return render_template("ihome.html")

@app.route("/inslogin", methods=['GET', 'POST'])       
def inslogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Login Attempt: {username}, {password}")  # Debugging line
        
        status = ins_loginact(username, password)
        print(f"Login Status: {status}")  # Debugging line
        
        if status == 1:
            session['username'] = username
            print(f"Session Set: {session['username']}")  # Debugging line
            return redirect(url_for('ihome'))
        else:
            return render_template("user.html", m1="Login Failed")

# Load NLTK's SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(tweet):
    sentiment_score = sia.polarity_scores(tweet)
    
    # Classify sentiment based on compound score
    if sentiment_score['compound'] >= 0.05:
        return 'Positive'
    elif sentiment_score['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def process_and_analyze_csv(input_file_path, output_file_path):
    df = pd.read_csv(input_file_path)
    df['Sentiment'] = df['Tweet'].apply(analyze_sentiment)
    df.to_csv(output_file_path, index=False)

    total_positive = df[df['Sentiment'] == 'Positive'].shape[0]
    total_negative = df[df['Sentiment'] == 'Negative'].shape[0]
    total_neutral = df[df['Sentiment'] == 'Neutral'].shape[0]

    return total_positive, total_negative, total_neutral

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        input_file_path = request.form['input_file_path']
        output_file_path = request.form['output_file_path']

        total_positive, total_negative, total_neutral = process_and_analyze_csv(input_file_path, output_file_path)

        return render_template('result.html',
                               total_positive=total_positive,
                               total_negative=total_negative,
                               total_neutral=total_neutral)
    
@app.route("/profile.html")
def profile():
    return render_template("profile.html")

@app.route("/index")
def index():
    return render_template("index.html")     

@app.route("/inceregact", methods = ['GET','POST'])
def inceregact():
    if request.method == 'POST':    
        status = inc_reg(request.form['username'], request.form['password'], request.form['email'], request.form['mobile'])
        if status == 1:
            return render_template("user.html", m1="sucess")
        else:
            return render_template("increg.html", m1="failed")

@app.route("/atact", methods = ['GET','POST'])
def atact():
    if request.method == 'POST':    
        username = session['username']
        data = request.form['data']
        col_names = ['text']
        var = pd.DataFrame(columns=col_names)
        var.loc[len(var)] = [data]
        fileName = "input\inputdata.csv"
        var.to_csv(fileName, index=False)
        result = predict(data)
        pred = result 
        return render_template("at.html", m1="sucess", pred=pred, data=data)

@app.route("/uploadcsv", methods = ['GET','POST'])
def uploadcsv():
    if request.method == 'POST':    
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']

        if file.filename == '':
            return "No selected file"

        if file:
            file.save(file.filename)
            df = pd.read_csv(file.filename, encoding='unicode_escape')
            print(df.head())
        return render_template("at.html", m1="sucess")

@app.route('/uaact', methods = ['GET','POST'])
def upload():
    if not os.path.isdir("./audio"):
        os.mkdir("audio")
    if request.method == 'POST':
        file = request.files['file']
        fname = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], fname))
        import speech_recognition as sr
        r = sr.Recognizer()
        wav_file_pre = os.listdir("./audio")[0]
        wav_file_pre = f"{os.getcwd()}\\audio\\{wav_file_pre}"  
        wav_file = convert(wav_file_pre)
        os.remove(wav_file_pre)      
        print(wav_file)
        hellow = sr.AudioFile(wav_file)
        with hellow as source:
            audio = r.record(source)
        try:
            s = r.recognize_google(audio)
            print("Text: "+s)
            col_names = ['text']
            var = pd.DataFrame(columns=col_names)
            var.loc[len(var)] = [s]
            fileName = "input\inputdata.csv"
            var.to_csv(fileName, index=False)
            result = predict(s)
            pred = result
        except Exception as e:
            print("Exception: "+str(e))
        return render_template('ua.html', text=s, pred=pred)

def convert(audio_path):
    if not os.path.exists(audio_path):
        return "File Doesn't Exist"
    file_split_list = audio_path.split("/")
    filename = file_split_list[-1].split(".")[0]
    new_filename = f"{filename}_converted.wav"
    file_split_list[-1] = new_filename
    seperator = "/"
    target_path = seperator.join(file_split_list)
    if not audio_path.endswith(".wav"):
        return "Invalid File: Must be in .wav format"
    else:
        try:
            os.system(f"ffmpeg -i {audio_path} -ac 1 -ar 16000 {target_path}")
        except Exception as e:
            print(e)
            return
        return target_path 

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render dynamically sets this
    app.run(debug=False, host='0.0.0.0', port=port)
