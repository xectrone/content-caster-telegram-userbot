import os
from dotenv import load_dotenv
import asyncio
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums.parse_mode import ParseMode


# Enable logging
logging.basicConfig(level=logging.INFO)

# Initialize Pyrogram client
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NO = os.getenv("PHONE_NO")

app = Client(
    name="my_session",
    api_id=API_ID, 
    api_hash=API_HASH, 
    phone_number=PHONE_NO
    )

@app.on_message(filters.command("start"))
async def start_command(client, message):
    response_text = (
        "Hello! I'm the Content Caster bot.\n\n"
        "I can help you schedule messages from one Telegram chat to another.\n\n"
        "Type `/help` to learn about available commands and how to use them.\n\n"
        "Enjoy scheduling messages with Content Caster!"
    )
    await message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.command("help"))
async def help_command(client, message):
    response_text = (
        "Here are the commands you can use with the Content Caster bot:\n\n"
        "`/start` - Start the bot and get a brief introduction.\n\n"
        "`/schedule` <src_chat_id> <dest_chat_id> <start_message_id> <end_message_id> <start_time (YYYY-MM-DD-HH:MM:SS)> <interval in hrs> - Schedule messages from one chat to another.\n\n"
        "Example:\n"
        "/schedule 123456789 987654321 1 100 2024-06-30-10:00:00 1\n\n"
        "This command schedules messages from message ID 1 to 100 from chat ID 123456789 to chat ID 987654321, starting on June 30, 2024, at 10:00 AM, with a 1-hour interval between messages.\n\n"
        "Use `/info` in reply to a message to get the message ID and chat ID.\n\n"
        "Enjoy scheduling messages with Content Caster!"
    )
    await message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.command("info"))
def start_command(client, message):
    mess = f"Message ID : `{message.reply_to_message_id}`\nChat ID : `{message.chat.id}`"
    message.reply_text(text = mess, parse_mode =ParseMode.MARKDOWN)


async def fetch_and_schedule_messages(src_chat_id, dest_chat_id, start_message_id, end_message_id, start_time, interval, chat_id):
    current_time = start_time
    message_id = start_message_id
    scheduler_counter = 0
    

    while message_id <= end_message_id:
        try:
            if scheduler_counter >= 95:
                current_time_str = current_time.strftime("%Y-%m-%d-%H:%M:%S")
                interval_hours = int(interval.total_seconds()/3600)
                command = f"/schedule {src_chat_id} {dest_chat_id} {message_id} {end_message_id} {current_time_str} {interval_hours}"
                await app.send_message(chat_id = chat_id, text=f"Scheduler limit has been reached. To continue from here, send the following command at {current_time}: \n`{command}`",parse_mode=ParseMode.MARKDOWN)
                await app.send_message(chat_id = chat_id, text=command, schedule_date=current_time, parse_mode=ParseMode.MARKDOWN)
                return

            message = await app.get_messages(src_chat_id, message_id)
            if message:
                if await schedule_message(message, dest_chat_id, current_time):
                    logging.info(f"Scheduled message {message_id} for {current_time}")
                    current_time += interval
                    scheduler_counter += 1
                    
                
        except Exception as e:
            logging.warning(f"Error: {e}")
        message_id += 1


async def schedule_message(message, dest_chat_id, schedule_time):
    if message.text:
        await app.send_message(
            chat_id=dest_chat_id,
            text=message.text,
            parse_mode=ParseMode.MARKDOWN,
            schedule_date=schedule_time
        )
        return True
    elif message.photo:
        await app.send_photo(
            chat_id=dest_chat_id,
            photo=message.photo.file_id,
            caption=message.caption,
            parse_mode=ParseMode.MARKDOWN,
            schedule_date=schedule_time
        )
        return True
    elif message.video:
        await app.send_video(
            chat_id=dest_chat_id,
            video=message.video.file_id,
            caption=message.caption,
            parse_mode=ParseMode.MARKDOWN,
            schedule_date=schedule_time
        )
        return True
    elif message.document:
        await app.send_document(
            chat_id=dest_chat_id,
            document=message.document.file_id,
            caption=message.caption,
            parse_mode=ParseMode.MARKDOWN,
            schedule_date=schedule_time
        )
        return True
    else:
        logging.warning(f"Unable to Schedule message : {message.id}")
        return False

@app.on_message(filters.command("schedule"))
async def schedule_handler(client, message):
    try:
        chat_id = message.chat.id
        args = message.text.split()
        
        if len(args) < 7:
            await message.reply_text("Usage: /schedule <src_chat_id> <dest_chat_id> <start_message_id> <end_message_id> <start_time> <interval in hrs>")
            return

        src_chat_id = int(args[1])
        dest_chat_id = int(args[2])
        start_message_id = int(args[3])
        end_message_id = int(args[4])
        start_time_str = args[5]
        interval_hours = int(args[6])

        start_time = datetime.strptime(start_time_str, "%Y-%m-%d-%H:%M:%S")
        interval = timedelta(hours=interval_hours)

        await message.reply_text(f"Scheduling messages from {start_message_id} to {end_message_id} from chat {src_chat_id} to {dest_chat_id} starting at {start_time} every {interval_hours} minutes.")
        
        await fetch_and_schedule_messages(src_chat_id, dest_chat_id, start_message_id, end_message_id, start_time, interval, chat_id)
    
    except Exception as e:
        logging.error(f"Error in scheduling: {e}")
        await message.reply_text(f"An error occurred: {e}")

app.run()