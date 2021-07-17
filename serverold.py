import speech_recognition as sr
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

server_cache = {} # locally store translation temporarily

# converts audio to text
def speech_to_text(speech):
    r = sr.Recognizer()
    speech2 = sr.AudioFile(speech)
    with speech2 as source:
        r.adjust_for_ambient_noise(source)
        audio_data = r.record(source)
        print("Recognizing audio")
        writetext = r.recognize_google(audio_data)
    return writetext

# retrieve product key corresponding to username from database
def retrieve_product_key(username):
  conn = sqlite3.connect("database.db")
  cur = conn.execute("SELECT product_key FROM users WHERE username = ? ",(username,))
  rows = cur.fetchall()
  conn.close()
  return rows[0][0]

app = Flask(__name__)

# home page - serves as the login form
@app.route("/")
def home():
  return render_template("login.html")

# Add cookie to indicate logged in user
def cookie():
  pass

# handle user login
@app.route("/login/submit")
def login_submit():
  if correct: # if credentials are correct, start recording audio
    return redirect(url_for("/record"))
  else: # else redirect to login page
    return redirect(url_for("/")) #Wrong username/password

#create form
@app.route("/create")
def create_account():
  return render_template("create.html")

# store username pwd and product key in database when user is creating account
@app.route("/create/submit", methods=["POST"])
def create_submit():
  conn = sqlite.connect("database.db")
  cur = conn.execute("INSERT INTO users (username, password, product_key,) VALUES (?,?,?,)",(username,password,product_key,))
  conn.close()
  return redirect(url_for("/"))

# records audio and sends it to recv_audio()
@app.route("/recordaudio") 
def record_audio():
  return render_template("record.html")

# receive audio from record_audio() and store it locally temporarily
@app.route("/recvaudio", methods=["POST"])
def recv_audio():
  try:
    #Get username from cookie
    phone_id = request.form["key"]
    audio = request.files["speech"]
    text = speech_to_text(audio)
    product_key = retrieve_product_key(username)
    server_cache[product_key] = text
    return redirect(url_for("/recordaudio"))
  except:
    return "A translation error has occurred"

# ESP will GET the translation from this function
@app.route("/sendaudio/<product_key>", methods=["GET"])
def send_audio(product_key):
  return server_cache[product_key]
 
app.run()
