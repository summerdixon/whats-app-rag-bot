from fastapi import FastAPI, Request, HTTPException
import os
from dotenv import load_dotenv
import httpx
from llm import generate_response

load_dotenv()
app = FastAPI()

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Required by WhatsApp to verify your server."""
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if token == os.getenv("VERIFY_TOKEN"):
        return int(challenge)
    raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/webhook")
async def whatsapp_handler(request: Request):
    data = await request.json()
    try:
        # Extract message and phone number
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            message_text = entry['messages'][0]['text']['body']
            sender_id = entry['messages'][0]['from']

            # Get AI response
            ai_reply = await generate_response(message_text)

            # Send back to WhatsApp
            await send_whatsapp_msg(sender_id, ai_reply)
    except KeyError:
        pass # Ignore status updates
    return {"status": "success"}

async def send_whatsapp_msg(to, text):
    url = f"https://graph.facebook.com/v17.0/{os.getenv('WHATSAPP_PHONE_ID')}/messages"
    headers = {"Authorization": f"Bearer {os.getenv('WHATSAPP_TOKEN')}"}
    json_data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=json_data, headers=headers)