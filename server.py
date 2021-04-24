import speech_recognition as sr
from flask import Flask, render_template

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

#receives audio from microphone
def recv_audio():
  pass

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/audio")
#sends audio to glasses
def send_audio_to_esp():
  try:
    audio = recv_audio()
    text = speech_to_text(audio)
    return text
  except:
    return "A translation error has occurred"

app.run()
