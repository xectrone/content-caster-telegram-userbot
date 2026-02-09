import os
import json
import asyncio
from pyrogram import Client
from handlers import register_handlers
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

ADMIN_IDS = [
    int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x
]

app = Client(
    name="userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

register_handlers(app, ADMIN_IDS)

async def handle(update):
    await app.start()
    await app.process_update(update)
    await app.stop()

def lambda_handler(event, context):
    update = json.loads(event["body"])
    asyncio.run(handle(update))
    return {"statusCode": 200, "body": "ok"}
