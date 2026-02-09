import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

logging.basicConfig(level=logging.INFO)

def register_handlers(app: Client, admin_ids):

    @app.on_message(filters.command("start"))
    async def start(_, message):
        await message.reply_text(
            "Hello! I'm the Content Caster userbot.\n\n"
            "Use /help to see available commands.",
            parse_mode=ParseMode.MARKDOWN
        )

    @app.on_message(filters.command("help"))
    async def help(_, message):
        await message.reply_text(
            "`/schedule <src_chat_id> <dest_chat_id> "
            "<start_msg_id> <end_msg_id> "
            "<YYYY-MM-DD-HH:MM:SS> <interval_hrs> [custom_message]`",
            parse_mode=ParseMode.MARKDOWN
        )

    @app.on_message(filters.command("info"))
    async def info(_, message):
        if not message.reply_to_message:
            await message.reply_text("Reply to a message.")
            return
        await message.reply_text(
            f"Message ID: `{message.reply_to_message.id}`\n"
            f"Chat ID: `{message.chat.id}`",
            parse_mode=ParseMode.MARKDOWN
        )

    @app.on_message(filters.command("schedule"))
    async def schedule(_, message):
        if message.from_user.id not in admin_ids:
            await message.reply_text("Not authorized.")
            return

        args = message.text.split()
        if len(args) < 7:
            await message.reply_text("Invalid usage.")
            return

        src = int(args[1])
        dest = int(args[2])
        start_id = int(args[3])
        end_id = int(args[4])
        start_time = datetime.strptime(args[5], "%Y-%m-%d-%H:%M:%S")
        interval = timedelta(hours=int(args[6]))
        custom = " ".join(args[7:]) if len(args) > 7 else None

        await message.reply_text("Scheduling started...")

        current = start_time
        for mid in range(start_id, end_id + 1):
            msg = await app.get_messages(src, mid)
            if not msg:
                continue

            await forward_message(app, msg, dest, current, custom)
            current += interval


async def forward_message(app, msg, dest, time, custom):
    if msg.text:
        await app.send_message(dest, msg.text, schedule_date=time)
    elif msg.photo:
        await app.send_photo(dest, msg.photo.file_id,
                             caption=custom or msg.caption,
                             schedule_date=time)
    elif msg.video:
        await app.send_video(dest, msg.video.file_id,
                             caption=custom or msg.caption,
                             schedule_date=time)
    elif msg.document:
        await app.send_document(dest, msg.document.file_id,
                                caption=custom or msg.caption,
                                schedule_date=time)
