
import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import bypasser
import os
import ddl
import requests
import threading
from texts import HELP_TEXT
from ddl import ddllist

# bot
bot_token = os.environ.get("TOKEN", "")
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")
app = pyrogram.Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# bypass function
def bypass_link(message):
    urls = []
    for ele in message.text.split():
        if "http://" in ele or "https://" in ele:
            urls.append(ele)
    if len(urls) == 0: return

    msg = app.send_message(message.chat.id, "🔎 __Bypassing...__", reply_to_message_id=message.message_id)

    link = ""
    for ele in urls:
        try: 
            temp = bypasser.bypass_link(ele)
            link = link + temp + "\n\n"
        except Exception as e: 
            link = link + "**Error**: " + str(e) + "\n\n"
        
    try: 
        app.edit_message_text(message.chat.id, msg.message_id, f'__{link}__', disable_web_page_preview=True)
    except:
        try: app.edit_message_text(message.chat.id, msg.message_id, "__Failed to bypass.__")
        except:
            try: app.delete_messages(message.chat.id, msg.message_id)
            except: pass
            app.send_message(message.chat.id, "__Failed to bypass.__")

# ddl function
def ddl_links(message):
    urls = []
    for ele in message.text.split():
        if "http://" in ele or "https://" in ele:
            urls.append(ele)
    if len(urls) == 0: return

    msg = app.send_message(message.chat.id, "🔎 __Processing...__", reply_to_message_id=message.message_id)

    link = ""
    for ele in urls:
        try: 
            link = link + f"\n\n**Direct link for {ele}:**\n"
            for i in ddllist:
                temp = ddl.process(i, ele)
                if temp: link = link + f"[{i}]({temp})\n"
            if len(link) <= 20: link = "**No direct links found.**"
        except Exception as e: 
            link = link + "**Error**: " + str(e) + "\n\n"
        
    try: 
        app.edit_message_text(message.chat.id, msg.message_id, f'__{link}__', disable_web_page_preview=True)
    except:
        try: app.edit_message_text(message.chat.id, msg.message_id, "__Failed to process.__")
        except:
            try: app.delete_messages(message.chat.id, msg.message_id)
            except: pass
            app.send_message(message.chat.id, "__Failed to process.__")

# links
@app.on_message()
def receive(client, message):
    if message.text:
        bypass_link(message)
        ddl_links(message)

# start command
@app.on_message(filters.command("start"))
def start_command(client, message):
    app.send_message(
        chat_id=message.chat.id,
        text=f"Hello {message.from_user.first_name}! I am a bot to bypass Terabox links and find direct download links. Just send me a Terabox link and I'll bypass it for you. For more information, send /help."
    )


    # help command
@app.on_message(filters.command("help"))
def help(_, message):
    message.reply_text(
        HELP_TEXT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📚 Commands", callback_data="commands"),
                    InlineKeyboardButton("❤️ Support", url="https://t.me/DirectLinksChannel"),
                ],
                [
                    InlineKeyboardButton("🤖 About", callback_data="about"),
                    InlineKeyboardButton("📣 Updates", url="https://t.me/DirectLinksUpdates"),
                ],
            ]
        ),
    )

# callback queries
@app.on_callback_query()
def callback_handlers(_, query):
    if query.data == "about":
        text = "This bot was created by [SenuGamerBoy](https://t.me/SenuGamerBoy). It is open source and its source code is available on [GitHub](https://github.com/SenuGamerBoy/TeraboxBypassBot)."
        query.answer()
        query.edit_message_text(text, disable_web_page_preview=True, parse_mode="markdown")
    elif query.data == "commands":
        text = "Here are the available commands:\n\n"
        for command, description in HELP_TEXT.items():
            text += f"▶️ /{command}: {description}\n"
        query.answer()
        query.edit_message_text(text, disable_web_page_preview=True)
        

        
# doc
@app.on_message(filters.document)
def docfile(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = threading.Thread(target=lambda:docthread(message),daemon=True)
    bypass.start()


# server loop
print("Bot Starting")
app.run()
