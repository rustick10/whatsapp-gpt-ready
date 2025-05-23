from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    msg = form.get("Body")
    sender = form.get("From")

    if msg:
        response_text = await generate_gpt_response(msg)
        twilio_response = MessagingResponse()
        twilio_response.message(response_text)
        return PlainTextResponse(str(twilio_response), media_type="application/xml")

    return PlainTextResponse("")

async def generate_gpt_response(message):
    try:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"

@app.get("/")
def read_root():
    return {"status": "online"}
