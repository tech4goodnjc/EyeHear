import speech_recognition as sr
from flask import Flask, session, render_template, request, redirect, url_for
import sqlite3
from flask_login import login_required, current_user, login_user, logout_user
from user import UserModel, db, login

app = Flask(__name__)
app.secret_key = "eyehear"

#Set users.db as database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Initialise db
db.init_app(app)
@app.before_first_request
def create_table():
    db.create_all()

#Initialise login manager
login.init_app(app)
login.login_view = "login"

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

# redirect to record page
@app.route("/")
def home():
    return redirect("/recordaudio")

# records audio and sends it to recv_audio()
# if not logged in, redirect to login page
@app.route("/recordaudio")
@login_required
def record_audio():
    return render_template("record.html")

# check username with password in db
# login if valid (redirect to record)
# else return login page
@app.route("/login", methods = ["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/recordaudio")
    error = "" 
    if request.method == "POST":
        username = request.form["username"]
        user = UserModel.query.filter_by(username = username).first()
        if user is not None and user.check_password(request.form["password"]):
            if request.form.get("remember"): #If user selects Remember Me, ticked by default
                login_user(user, remember=True)
            else:
                login_user(user, remember=False)
            return redirect("/recordaudio")
        error = "Invalid Username/Password"
     
    return render_template("login.html", error=error)

# register using username, password, product key
# go back to registration page if username or product key in db
@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect("/recordaudio")
    error = ""
    if request.method == "POST":
        productkey = request.form["productkey"]
        username = request.form["username"]
        password = request.form["password"]
 
        if UserModel.query.filter_by(username=username).first():
            error = "Username has already been taken"
        elif UserModel.query.filter_by(productkey=productkey).first():
            error = "Product Key has already been registered"
        else:             
            user = UserModel(productkey=productkey, username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
    return render_template("register.html", error=error)

# receive audio from record_audio() and store it locally temporarily
# need to test this once on cloud
@app.route("/recvaudio", methods=["POST"])
@login_required
def recv_audio():
    try:
      #Get username from cookie
      phone_id = request.form["key"]
      audio = request.files["speech"]
      text = speech_to_text(audio)
      productkey = current_user.productkey
      server_cache[productkey] = text
      return redirect("/recordaudio")
    except:
      return "A translation error has occurred"

# ESP will GET the translation from this function
@app.route("/sendaudio/<productkey>", methods=["GET"])
def send_audio(productkey):
  return server_cache[productkey]

#logout user
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/recordaudio")

app.run()
