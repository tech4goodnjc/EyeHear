import speech_recognition as sr
from flask import Flask, render_template, request, redirect, url_for

curr = ""
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


app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/recvaudio", methods=["POST"])
#sends audio to glasses
def recv_audio():
  try:
    audio = request.files["speech"]
    text = speech_to_text(audio)
    curr = text
    return redirect(url_for("sendaudio"))
  except:
    return "A translation error has occurred"

@app.route("/sendaudio", methods=["GET"])
def send_audio():
  return curr
 
app.run()
