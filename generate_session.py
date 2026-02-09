import os
import logging
from pyrogram import Client
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

with Client(
    name="session_generator",
    api_id=API_ID,
    api_hash=API_HASH
) as app:
    print("\n==============================")
    print("✅ SESSION STRING GENERATED")
    print("==============================\n")
    print(app.export_session_string())
    print("\n==============================\n")
