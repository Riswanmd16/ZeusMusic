# ZeusMusic (Telegram bot project)
# Copyright (C) 2021  Sathishzus & Bharathi2003

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import os
from os import path
from typing import Callable

import aiofiles
import aiohttp
import ffmpeg
import requests
import wget
import pyrogram
from pyrogram.parser import html
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.types import Voice
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, Chat, CallbackQuery
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch
from asyncio.queues import QueueEmpty

from ZeusMusic.config import ARQ_API_KEY
from ZeusMusic.config import BOT_NAME as bn
from ZeusMusic.config import DURATION_LIMIT
from ZeusMusic.config import UPDATES_CHANNEL as updateschannel
from ZeusMusic.config import que
from ZeusMusic.config import SOURCE_CODE,ASSISTANT_NAME,PROJECT_NAME,SUPPORT_GROUP,BOT_USERNAME, OWNER
from ZeusMusic.function.admins import admins as a
from ZeusMusic.helpers.admins import get_administrators
from ZeusMusic.helpers.channelmusic import get_chat_id
from ZeusMusic.helpers.errors import DurationLimitError
from ZeusMusic.helpers.decorators import errors
from ZeusMusic.helpers.decorators import authorized_users_only
from ZeusMusic.helpers.filters import command, other_filters
from ZeusMusic.helpers.gets import get_file_name
from ZeusMusic.services.callsmusic import callsmusic
from ZeusMusic.services.callsmusic.callsmusic import client as USER
from ZeusMusic.services.converter.converter import convert
from ZeusMusic.services.downloaders import youtube
from ZeusMusic.services.queues import queues
from ZeusMusic.services.callsmusic.callsmusic import queues

aiohttpsession = aiohttp.ClientSession()
chat_id = None
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)
DISABLED_GROUPS = []
useer ="NaN"
def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        else:
            await cb.answer("You ain't allowed!", show_alert=True)
            return

    return decorator


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/Roboto-Regular.ttf", 58)
    draw.text((25, 535), f"Playing here", (0, 0, 0), font=font)
    font = ImageFont.truetype("etc/Roboto-Medium.ttf", 75)
    draw.text((25, 615),
        f"{title[:25]}..",
        (0, 0, 0),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


# ============================= Settings =========================================


def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        # if chat.id in active_chats:
        stats = "🎛️ Settings of **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "Volume : {}%\n".format(vol)
            stats += "**Songs in queue** : `{}`\n".format(len(que))
            stats += "**Playing song** : **{}**\n".format(queue[0][0])
            stats += "**Requested by** : {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats

def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
         [
                [
                    InlineKeyboardButton("⏹", "leave"),
                    InlineKeyboardButton("⏸", "puse"),
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏭", "skip"),
                ],
                [
                    InlineKeyboardButton("📜 Playlist", "playlist"),
                ],[
                    InlineKeyboardButton("🗑️ Close", "cls")
                ],
            ]
        )
    return mar

@Client.on_message(filters.command("current") & filters.group & ~filters.edited)
async def ee(client, message):
    if message.chat.id in DISABLED_GROUPS:
        return
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        await message.reply(stats)
    else:
        await message.reply("💡 **Please turn on voice chat first**")


@Client.on_message(filters.command("player") & filters.group & ~filters.edited)
@authorized_users_only
async def settings(client, message):
    if message.chat.id in DISABLED_GROUPS:
        await message.reply("**Music player turned off** 🔴")
        return    
    playing = None
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        playing = True
    queue = que.get(chat_id)
    stats = updated_stats(message.chat, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))

        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("**💡 Please turn on voice chat first!**")


@Client.on_message(
    filters.command("musicplayer") & ~filters.edited & ~filters.bot & ~filters.private
)
@authorized_users_only
async def hfmm(_, message):
    global DISABLED_GROUPS
    try:
        user_id = message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text(
            "💡**I only recognize** /musicplayer on and /musicplayer off"
        )
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await message.reply("Processing..")
        if not message.chat.id in DISABLED_GROUPS:
            await lel.edit("✅ **Music player is successfully active in this group**")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(
            f"🟢 **Music player** activated successfully for user in chat {message.chat.id}"
        )

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await message.reply("Processing...")
        
        if message.chat.id in DISABLED_GROUPS:
            await lel.edit("❎ **The music player has been turned off in this group**")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(
            f"🔴 **Music player** disabled successfully for user in chat {message.chat.id}"
        )
    else:
        await message.reply_text(
            "💡 **I only recognize** /musicplayer on and /musicplayer off"
        )    
        

@Client.on_callback_query(filters.regex(pattern=r"^(playlist)$"))
async def p_cb(b, cb):
    global que
    que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("❎ **Not playing a song**")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "💡 **Song currently playing** on {}".format(cb.message.chat.title)
        msg += "\n• " + now_playing
        msg += "\n• Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "🔢 **Song queue**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n• {name}"
                msg += f"\n• Req by {usr}\n"
        await cb.message.edit(msg)

@Client.on_callback_query(
    filters.regex(pattern=r"^(closed)$")
)
@cb_admin_check
async def bt_cls(b, cb):
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    if type_ == "closed":
        await cb.answer("CLOSE")
        await cb.message.delete()

@Client.on_callback_query(
    filters.regex(pattern=r"^(play|pause|skip|leave|puse|resume|menu|cls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    if (
        cb.message.chat.title.startswith("Channel Music: ")
        and chat.title[14:].isnumeric()
    ):
        chet_id = int(chat.title[13:])
    else:
        chet_id = cb.message.chat.id
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "pause":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("Chat is not connected!", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("Music Paused!")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("play")
            )

    elif type_ == "play":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("Chat is not connected!", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Music Resumed!")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("Player is idle")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "💡 **Song currently playing** on {}".format(cb.message.chat.title)
        msg += "\n• " + now_playing
        msg += "\n• Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "🔢 **Song queue**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n• {name}"
                msg += f"\n• Req by {usr}\n"
        await cb.message.edit(msg)

    elif type_ == "resume":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("Chat is not connected or already playng", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Music Resumed!")
    elif type_ == "puse":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("Chat is not connected or already paused", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("Music Paused!")
    elif type_ == "cls":
        await cb.answer("Closed menu")
        await cb.message.delete()

    elif type_ == "menu":
        stats = updated_stats(cb.message.chat, qeue)
        await cb.answer("Menu opened")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "leave"),
                    InlineKeyboardButton("⏸", "puse"),
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏭", "skip")
                ],
                [
                    InlineKeyboardButton("📜 Playlist", "playlist"),
                ],[
                    InlineKeyboardButton("🗑️ Close", "cls")
                ],
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)
    elif type_ == "skip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer("Chat is not connected!", show_alert=True)
        else:
            callsmusic.queues.task_done(chet_id)

            if callsmusic.queues.is_empty(chet_id):
                callsmusic.pytgcalls.leave_group_call(chet_id)

                await cb.message.edit("- No More Playlist..\n- Leaving VC!")
            else:
                callsmusic.pytgcalls.change_stream(
                    chet_id, callsmusic.queues.get(chet_id)["file"]
                )
                await cb.answer("Skipped")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    f"- Skipped track\n- Now Playing **{qeue[0][0]}**\n\n⚡ **__Powered by @ZeusBotsNetwork__**"
                )

    elif type_ == "leave":
        if chet_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chet_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chet_id)
            await cb.message.edit("🔴 **__Assistant has been disconnected from voice chat__**")
        else:
            await cb.answer("assistant is not connected to voice chat!", show_alert=True)


@Client.on_message(command(["play", "p"]) & other_filters)
async def play(_, message: Message):
    global que
    global useer
    if message.chat.id in DISABLED_GROUPS:
        return    
    lel = await message.reply("🔁 `Processing...`")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "ZeusMusic"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        f"<b>please add {user.first_name} to your channel.</b>",
                    )
                    pass
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "💡 To use me, I need to be an Administrator with the following **permissions:**\n\n» ❌ **Delete messages**\n» ❌ **Ban users**\n» ❌ **Add users**\n» ❌ **Manage voice chat**\n» ❌ **Add new admins**\n\nThen **type** /reload\n📣 **Updates Channel :** @ZeusBotsNetwork",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "✅ I joined to play a song in **voice chat!**"
                    )
                    await lel.edit(
                        "<b>✅ **Helper userbot has successfully joined this group**\n\n**Subs Channel**: @ZeusBotsNetwork\n\n**Group Support**: @ZeusSupport</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 Flood Wait Error 🔴 \nUser {user.first_name} couldn't join your group due to heavy requests for userbot! Make sure user is not banned in group.."
                        f"\n\nOr manually add @{ASSISTANT_NAME} to your Group and try again</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<b>🔴 **Flood Wait Error** 🔴 \nUserBot {user.first_name} couldn't join your group call due to **Heavy Flood Request**. 🧑‍💻\nPlease Try After 2-3 Minutes. 🤧"
        )
        return
    text_links=None
    await lel.edit("🔁 **Processing..**")
    if message.reply_to_message:
        entities = []
        toxt = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [entity for entity in entities if entity.type == 'url']
        text_links = [
            entity for entity in entities if entity.type == 'text_link'
        ]
    else:
        urls=None
    if text_links:
        urls = True
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**❌ Videos longer than {DURATION_LIMIT} minute(s) aren't allowed to play!**"
            )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🖱️ ᴍᴇɴᴜ", callback_data="menu"),
                    InlineKeyboardButton("🗑 ᴄʟᴏsᴇ", callback_data="cls"),
                ],[
                    InlineKeyboardButton("⏺️ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/ZeusBotsNetwork")
                ],
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/18fe8a16eb1194e132c24.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("🔁 **Processing...**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:25]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "❎ **Song not found!** Try another song or maybe spell it properly."
            )
            print(str(e))
            return
        dlurl=url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
         [
                [
                    InlineKeyboardButton("⏹", "leave"),
                    InlineKeyboardButton("⏸", "puse"),
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏭", "skip"),
                ],
                [
                    InlineKeyboardButton("📜 Playlist", "playlist"),
                ],[
                    InlineKeyboardButton("🗑️ Close", "cls")
                ],
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))        
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await lel.edit("🔁 **Processing...**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        
        try:
          results = YoutubeSearch(query, max_results=5).to_dict()
        except:
          await lel.edit("**Give the title of the song to play!**")
        # Looks like hell. Aren't it?? FUCK OFF
        try:
            toxxt = "\n"
            j = 0
            useer=user_name

            emojilist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]
            while j < 5:
                toxxt += f"{emojilist[j]} [{results[j]['title']}](https://youtube.com{results[j]['url_suffix']})</b>\n"
                toxxt += f" ├ 💡 **Duration** - {results[j]['duration']}\n"
                toxxt += f" └ ⚡ ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 : ℤ𝕖𝕦𝕤 𝔹𝕠𝕥𝕤 ℕ𝕖𝕥𝕨𝕠𝕣𝕜\n\n"

                j += 1            
            koyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("1️⃣", callback_data=f'plll 0|{query}|{user_id}'),
                        InlineKeyboardButton("2️⃣", callback_data=f'plll 1|{query}|{user_id}'),
                        InlineKeyboardButton("3️⃣", callback_data=f'plll 2|{query}|{user_id}'),
                    ],
                    [
                        InlineKeyboardButton("4️⃣", callback_data=f'plll 3|{query}|{user_id}'),
                        InlineKeyboardButton("5️⃣", callback_data=f'plll 4|{query}|{user_id}'), 
                    ],
                    [
                        InlineKeyboardButton(text="🗑 ᴄʟᴏsᴇ", callback_data="cls")],
                ]
            )
     
            await message.reply_photo(
                photo="https://telegra.ph/file/18fe8a16eb1194e132c24.jpg",
                caption=toxxt, reply_markup=koyboard, 
            )
            await lel.delete()
            return
            # Returning to pornhub
        except:
            await lel.edit("🤖 **There are not enough results to choose from, start playing right away.**")
                        
            # print(results)
            try:
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:40]
                thumbnail = results[0]["thumbnails"][0]
                thumb_name = f"thumb{title}.jpg"
                thumb = requests.get(thumbnail, allow_redirects=True)
                open(thumb_name, "wb").write(thumb.content)
                duration = results[0]["duration"]
                results[0]["url_suffix"]
                views = results[0]["views"]

            except Exception as e:
                await lel.edit(
                "❎ **Song not found!** Try searching with the correct title\n**Example** » /play Taki Taki remix\n\n💡 **Subs Channel** : @ZeusBotsNetwork"
            )
                print(str(e))
                return
            dlurl=url
            dlurl=dlurl.replace("youtube","youtubepp")
            await message.reply(stats, reply_markup=r_ply("pause"))

            requested_by = message.from_user.first_name
            await generate_cover(requested_by, title, views, duration, thumbnail)
            file_path = await convert(youtube.download(url))   
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption = f"💡 **Track added to the queue**\n\n🏷 **Title:** [{title[:60]}]({url})\n⏱ **Duration:** `{duration}`\n🎧 **Request by:** {message.from_user.mention}\n" \
                    + f"\n🔢 **Track position:** » `{position}` «",
                   reply_markup=keyboard)
       
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            message.reply("**Group Call is not connected or I can't join it**")
            return
        await message.reply_photo(
            photo="final.png",
            caption = f"🏷 **Title:** [{title[:60]}]({url})\n⏱ **Duration:** `{duration}`\n💡 **Status:** Playing\n" \
                    + f"🎧 **Request by:** {message.from_user.mention}",
                   reply_markup=keyboard,)

    os.remove("final.png")
    return await lel.delete()


@Client.on_message(filters.command("ytp") & filters.group & ~filters.edited)
async def ytplay(_, message: Message):
    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    lel = await message.reply("💡 **Processing song..**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "ZeusMusic"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        f"<b>Remember to add helper to your channel</b>",
                    )
                    pass
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>add me as admin first.</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**I joined this group to play songs in voice chat**"
                    )
                    await lel.edit(
                        "<b>Helper userbot has successfully joined this group</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 Flood Wait Error 🔴 \nUser {user.first_name} couldn't join your group due to heavy requests for userbot! Make sure user is not banned in group.."
                        f"\n\nOr manually add @{ASSISTANT_NAME} to your Group and try again</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i>{user.first_name} **banned in this group,** ask admin to unban! @{ASSISTANT_NAME}</i>"
        )
        return
    await lel.edit("🔎 **Processing..**")
    user_id = message.from_user.id
    user_name = message.from_user.first_name
     

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    await lel.edit("🎵 **Processing song..**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        # print(results)
        title = results[0]["title"][:30]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        await lel.edit(
            "Found Literally Nothing!, You Should Work On Your English"
        )
        print(str(e))
        return
    dlurl=url
    dlurl=dlurl.replace("youtube","youtubepp")
    keyboard = InlineKeyboardMarkup(
         [
                [
                    InlineKeyboardButton("⏹", "leave"),
                    InlineKeyboardButton("⏸", "puse"),
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏭", "skip"),
                ],
                [
                    InlineKeyboardButton("📜 Playlist", "playlist"),
                ],[
                    InlineKeyboardButton("🗑️ Close", "cls")
                ],
            ]
        )


    requested_by = message.from_user.first_name
    await generate_cover(requested_by, title, views, duration, thumbnail)
    file_path = await convert(youtube.download(url))
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption = f"💡 **Track added to the queue**\n\n🏷 **Title:** [{title[:30]}]({url})\n⏱ **Duration:** `{duration}`\n🎧 **Request by:** {message.from_user.mention}\n" \
                    + f"\n🔢 **Track position:** » `{position}` «",
                   reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            message.reply("**Group call is not connected of I can't join it**")
            return
        await message.reply_photo(
            photo="final.png",
            caption = f"🏷 **Title:** [{title[:30]}]({url})\n⏱ **Duration:** {duration}\n💡 **Status:** Playing\n" \
                    + f"🎧 **Request by:** {message.from_user.mention}",
                   reply_markup=keyboard,)
        os.remove("final.png")
        return await lel.delete()
    

@Client.on_callback_query(filters.regex(pattern=r"plll"))
async def lol_cb(b, cb):
    global que
    cbd = cb.data.strip()
    chat_id = cb.message.chat.id
    typed_=cbd.split(None, 1)[1]
    try:
        x,query,useer_id = typed_.split("|")      
    except:
        await cb.message.edit("❌ song not found")
        return
    useer_id = int(useer_id)
    if cb.from_user.id != useer_id:
        await cb.answer("you are not people who requested this song !", show_alert=True)
        return
    await cb.message.edit(f"**Connecting to voice chat...**\n\n⏰ **Estimated Time:** `50 sec`")
    x=int(x)
    try:
        useer_name = cb.message.reply_to_message.from_user.first_name
    except:
        useer_name = cb.message.from_user.first_name
    results = YoutubeSearch(query, max_results=5).to_dict()
    resultss=results[x]["url_suffix"]
    title=results[x]["title"][:30]
    thumbnail=results[x]["thumbnails"][0]
    duration=results[x]["duration"]
    views=results[x]["views"]
    url = f"https://youtube.com{resultss}"
    
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul) 
            secmul *= 60   
        duuration= round(duration / 60)
        if duuration > DURATION_LIMIT:
            await cb.message.edit(f"Music longer than {DURATION_LIMIT}min are not allowed to play")
            return
    except:
        pass
    try:
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    except Exception as e:
        print(e)
        return
    dlurl=url
    dlurl=dlurl.replace("youtube","youtubepp")
    keyboard = InlineKeyboardMarkup(
         [
                [
                    InlineKeyboardButton("⏹", "leave"),
                    InlineKeyboardButton("⏸", "puse"),
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏭", "skip"),
                ],
                [
                    InlineKeyboardButton("📜 Playlist", "playlist"),
                ],[
                    InlineKeyboardButton("🗑️ Close", "cls")
                ],
            ]
        )

    requested_by = useer_name
    await generate_cover(requested_by, title, views, duration, thumbnail)
    file_path = await convert(youtube.download(url))  
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await cb.message.delete()
        await b.send_photo(chat_id,    photo="final.png",
            caption = f"💡 **Track added to the queue**\n\n🏷 **Title:** [{title[:60]}]({url})\n⏱ **Duration:** `{duration}`\n🎧 **Request by:** {r_by.mention}\n" \
                    + f"\n🔢 **Track position:** » `{position}` «",
                   reply_markup=keyboard,
        )
        os.remove("final.png")
        
    else:
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)

        callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        await cb.message.delete()
        await b.send_photo(chat_id,
            photo="final.png",
            caption = f"🏷 **Title:** [{title}]({url})\n⏱ **Duration:** {duration}\n💡 **Status:** Playing\n" \
                    + f"🎧 **Request by:** {r_by.mention}",
                    reply_markup=keyboard,
        )
        os.remove("final.png")

