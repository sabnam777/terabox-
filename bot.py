import pyrogram

import os

import teraboxbypasser as bypasser

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

# links

@app.on_message()

def receive(client, message):

    if message.text:

        bypass_link(message)

# start command

@app.on_message(pyrogram.filters.command("start"))

def start_command(client, message):

    app.send_message(

        chat_id=message.chat.id,

        text=f"Hello {message.from_user.first_name}! I am a bot to bypass Terabox links. Just send me a Terabox link and I'll bypass it for you. For more information, send /help."

    )

# help command

@app.on_message(pyrogram.filters.command("help"))

def help_command(client, message):

    app.send_message(

        chat_id=message.chat.id,

        text="Just send me a Terabox link and I'll bypass it for you. That's it. 😀"

    )

# start the bot

app.run()

