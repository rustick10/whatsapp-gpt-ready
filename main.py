from flask import Flask, request, jsonify
import openai
import requests
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.form
    msg_body = data.get("Body", "").strip()
    from_number = data.get("From", "")

    # Processamento de áudio
    if "MediaUrl0" in data:
        media_url = data["MediaUrl0"]
        audio_response = requests.get(media_url)
        with open("audio.ogg", "wb") as f:
            f.write(audio_response.content)
        audio_file = open("audio.ogg", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)["text"]
        prompt = transcript
    else:
        prompt = msg_body

    # ChatGPT resposta
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = completion.choices[0].message["content"]
    return f"<Response><Message>{reply}</Message></Response>", 200, {"Content-Type": "application/xml"}