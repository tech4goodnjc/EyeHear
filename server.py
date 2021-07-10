import speech_recognition as sr
from flask import Flask, render_template, request, redirect, url_for

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

# Retrieves the corresponding device_id for the phone_id provided
def phoneid_to_glassid(phone_id):
    pass

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/recvaudio/<phone_id>", methods=["POST"])
#sends audio to glasses
def recv_audio(phone_id):
  try:
    audio = request.files["speech"]
    text = speech_to_text(audio)
    curr = text
    glasses_id = phone_to_glass(phone_id)
    return redirect(url_for(f"sendaudio/{glasses_id}"))
  except:
    return "A translation error has occurred"

@app.route("/sendaudio/<glasses_id>", methods=["GET"])
def send_audio(glasses_id):
  pass
 
app.run()
