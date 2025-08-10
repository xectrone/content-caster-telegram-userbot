import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.enums import ChatType
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import Message
from pyrogram.types import Message
import asyncio


# Enable logging
logging.basicConfig(level=logging.INFO)

# Initialize Pyrogram client
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# Get admin IDs from environment variables
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(admin_id.strip()) for admin_id in ADMIN_IDS_STR.split(",") if admin_id.strip()]

app = Client(
    name="my_session",
    api_id=API_ID,
    api_hash=API_HASH, 
    # session_string=SESSION_STRING
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
        "`/schedule` <src_chat_id> <dest_chat_id> <start_message_id> <end_message_id> <start_time (YYYY-MM-DD-HH:MM:SS)> <interval in hrs> [custom_message] - Schedule messages from one chat to another.\n\n"
        "Example:\n"
        "/schedule 123456789 987654321 1 100 2024-06-30-10:00:00 1 \"Join our channel @YourChannel\"\n\n"
        "This command schedules messages from message ID 1 to 100 from chat ID 123456789 to chat ID 987654321, starting on June 30, 2024, at 10:00 AM, with a 1-hour interval between messages. If custom_message is provided, it will replace the caption for media messages.\n\n"
        "`/unban_all` - Unban all users who are currently banned in the group.\n\n"
        "Use `/info` in reply to a message to get the message ID and chat ID.\n\n"
        "Note: The schedule and unban_all commands can only be used by authorized administrators.\n\n"
        "Enjoy scheduling messages with Content Caster!"
    )
    await message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.command("info"))
def info_command(client, message):
    mess = f"Message ID : `{message.reply_to_message_id}`\nChat ID : `{message.chat.id}`"
    message.reply_text(text = mess, parse_mode =ParseMode.MARKDOWN)


@app.on_message(filters.command("unban_all"))
async def unban_all_command(client, message):
    try:
        # Check if user is an admin
        user_id = message.from_user.id
        if user_id not in ADMIN_IDS:
            await message.reply_text("You are not authorized to use this command.")
            return
            
        # Check if the command is used in a group
        if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await message.reply_text(f"This command can only be used in groups or supergroups. This is {message.chat.type}")
            return
            
        # Get the chat ID
        chat_id = message.chat.id
        
        # Send initial message
        status_message = await message.reply_text("Starting to unban all users in this group...")
        
        # Get the list of banned users
        async for banned_user in app.get_chat_members(chat_id, filter=ChatMembersFilter.BANNED):
            if banned_user.user is None:
                continue  # Skip deleted or inaccessible users
            try:
                await app.unban_chat_member(chat_id, banned_user.user.id)
            except Exception as e:
                logging.error(f"Failed to unban {banned_user.user.id}: {e}")

        
        if not banned_members:
            await status_message.edit_text("No banned users found in this group.")
            return
            
        # Unban all users
        # unban_count = 0
        # for user_id in banned_members:
        #     try:
        #         await app.unban_chat_member(chat_id, user_id)
        #         unban_count += 1
        #     except Exception as e:
        #         logging.error(f"Error unbanning user {user_id}: {e}")
        
        # Send completion message
        await status_message.edit_text(f"Successfully unbanned {unban_count} out of {len(banned_members)} users in this group.")
        
    except Exception as e:
        logging.error(f"Error in unban_all command: {e}")
        await message.reply_text(f"An error occurred: {e}")



async def fetch_and_schedule_messages(src_chat_id, dest_chat_id, start_message_id, end_message_id, start_time, interval, chat_id, custom_message=None):
    current_time = start_time
    message_id = start_message_id
    scheduler_counter = 0
    

    while message_id <= end_message_id:
        try:
            if scheduler_counter >= 95:
                current_time_str = current_time.strftime("%Y-%m-%d-%H:%M:%S")
                interval_hours = int(interval.total_seconds()/3600)
                command = f"/schedule {src_chat_id} {dest_chat_id} {message_id} {end_message_id} {current_time_str} {interval_hours}"
                if custom_message:
                    command += f" {custom_message}"
                await app.send_message(chat_id = chat_id, text=f"Scheduler limit has been reached. To continue from here, send the following command at {current_time}: \n`{command}`",parse_mode=ParseMode.MARKDOWN)
                await app.send_message(chat_id = chat_id, text=command, schedule_date=current_time, parse_mode=ParseMode.MARKDOWN)
                return

            message = await app.get_messages(src_chat_id, message_id)
            if message:
                if await schedule_message(message, dest_chat_id, current_time, custom_message):
                    logging.info(f"Scheduled message {message_id} for {current_time}")
                    current_time += interval
                    scheduler_counter += 1
                    
                
        except Exception as e:
            logging.warning(f"Error: {e}")
        message_id += 1


async def schedule_message(message, dest_chat_id, schedule_time, custom_message=None):

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
            caption=custom_message if custom_message else message.caption,
            parse_mode=ParseMode.MARKDOWN,
            schedule_date=schedule_time
        )
        return True
    elif message.video:
        await app.send_video(
            chat_id=dest_chat_id,
            video=message.video.file_id,
            caption=custom_message if custom_message else message.caption,
            parse_mode=ParseMode.MARKDOWN,
            schedule_date=schedule_time
        )
        return True
    elif message.document:
        await app.send_document(
            chat_id=dest_chat_id,
            document=message.document.file_id,
            caption=custom_message if custom_message else message.caption,
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
        # Check if user is an admin
        user_id = message.from_user.id
        if user_id not in ADMIN_IDS:
            await message.reply_text("You are not authorized to use this command.")
            return
            
        chat_id = message.chat.id
        # Split by space but preserve quoted strings
        text_parts = message.text.split()
        args = []
        i = 0
        while i < len(text_parts):
            if text_parts[i].startswith('"') and not text_parts[i].endswith('"'):
                # Start of a quoted string
                quoted_string = text_parts[i]
                i += 1
                while i < len(text_parts) and not text_parts[i].endswith('"'):
                    quoted_string += ' ' + text_parts[i]
                    i += 1
                if i < len(text_parts):
                    quoted_string += ' ' + text_parts[i]
                args.append(quoted_string.strip('"'))
            else:
                args.append(text_parts[i].strip('"'))
            i += 1
        
        if len(args) < 7:
            await message.reply_text("Usage: /schedule <src_chat_id> <dest_chat_id> <start_message_id> <end_message_id> <start_time> <interval in hrs> [custom_message]")
            return

        src_chat_id = int(args[1])
        dest_chat_id = int(args[2])
        start_message_id = int(args[3])
        end_message_id = int(args[4])
        start_time_str = args[5]
        interval_hours = int(args[6])
        
        # Get custom message if provided
        custom_message = None
        if len(args) > 7:
            custom_message = args[7]

        start_time = datetime.strptime(start_time_str, "%Y-%m-%d-%H:%M:%S")
        interval = timedelta(hours=interval_hours)

        message_info = f"Scheduling messages from {start_message_id} to {end_message_id} from chat {src_chat_id} to {dest_chat_id} starting at {start_time} every {interval_hours} hours."
        if custom_message:
            message_info += f"\nCustom message: {custom_message}"
            
        await message.reply_text(message_info)
        
        await fetch_and_schedule_messages(src_chat_id, dest_chat_id, start_message_id, end_message_id, start_time, interval, chat_id, custom_message)
    
    except Exception as e:
        logging.error(f"Error in scheduling: {e}")
        await message.reply_text(f"An error occurred: {e}")





# At the top of your file
from pyrogram import filters
from pyrogram.types import Message
import asyncio

repeating_tasks = {}


@app.on_message(filters.command("repeat"))
async def repeat_message(client, message: Message):
    if not message.reply_to_message:
        await message.reply("⚠️ Please reply to a message to repeat.")
        return

    try:
        interval = message.text.split(maxsplit=1)[1]
    except IndexError:
        await message.reply("❌ Usage: `/repeat <interval>` (e.g., `/repeat 10s`, `/repeat 5m`)")
        return

    # Convert interval to seconds
    unit = interval[-1]
    value = int(interval[:-1])

    if unit == "s":
        delay = value
    elif unit == "m":
        delay = value * 60
    elif unit == "h":
        delay = value * 3600
    else:
        await message.reply("❌ Invalid time unit. Use `s`, `m`, or `h` (e.g., 10s, 2m, 1h)")
        return

    chat_id = message.chat.id

    # If already repeating, cancel first
    if chat_id in repeating_tasks:
        repeating_tasks[chat_id].cancel()

    # Start repeating
    async def repeater():
        while True:
            await client.send_message(chat_id, message.reply_to_message.text)
            await asyncio.sleep(delay)

    task = asyncio.create_task(repeater())
    repeating_tasks[chat_id] = task

    await message.reply(f"✅ Repeating message every {interval}. Use `/stoprepeat` to stop.")


@app.on_message(filters.command("stoprepeat"))
async def stop_repeat(client, message: Message):
    chat_id = message.chat.id
    task = repeating_tasks.get(chat_id)

    if task:
        task.cancel()
        del repeating_tasks[chat_id]
        await message.reply("🛑 Repeating stopped.")
    else:
        await message.reply("⚠️ No repeating task running in this chat.")


app.run()