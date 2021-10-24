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


import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, Chat, CallbackQuery
from ZeusMusic.config import SOURCE_CODE,ASSISTANT_NAME,PROJECT_NAME,SUPPORT_GROUP,UPDATES_CHANNEL,BOT_USERNAME, OWNER, BOT_NAME
logging.basicConfig(level=logging.INFO)
from ZeusMusic.helpers.filters import command
from time import time
from datetime import datetime
from ZeusMusic.helpers.decorators import authorized_users_only


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)



@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "🏓 `PONG!!`\n"
        f"⚡️ `{delta_ping * 1000:.3f} ms`"
    ) 


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@authorized_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Group Support", url=f"https://t.me/ZeusSupport"
                    )
                ]
            ]
        ),
    )

#alive
@Client.on_message(filters.command(["alive", f"alive@{BOT_USERNAME}"]))
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_photo(
        photo=f"https://telegra.ph/file/35e359d2f7b870b4d2dff.jpg",
        caption=f"""🔵 Holla I'am @{BOT_USERNAME}
🔵 I'm Working Properly
🔵 Bot : 1.0.1 LATEST
🔵 My AAssistant : [{BOT_NAME}](https://t.me/{ASSISTANT_NAME})
🔵 Service Uptime : {uptime}
Thanks For Using Me ♡""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🚨 Group", url=f"https://t.me/ZeusSupport"
                    ),
                    InlineKeyboardButton(
                        "📡 Channel", url=f"https://t.me/ZeusBotsNetwork"
                    )
                ]
            ]
        )
    )


@Client.on_message(
    filters.command(["start", f"start@{BOT_USERNAME}"])
    & filters.private
    & ~ filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋 **𝗪𝗲𝗹𝗰𝗼𝗺𝗲** {message.from_user.mention()}**\n
🗯️{BOT_NAME} 𝗮𝗹𝗹𝗼𝘄 𝘆𝗼𝘂 𝘁𝗼 𝗽𝗹𝗮𝘆 𝗺𝘂𝘀𝗶𝗰 𝗼𝗻 𝗴𝗿𝗼𝘂𝗽𝘀 𝘁𝗵𝗿𝗼𝘂𝗴𝗵 𝘁𝗵𝗲 𝗻𝗲𝘄 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺'𝘀 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁𝘀 !\n

💡 𝗙𝗶𝗻𝗱 𝗼𝘂𝘁 𝗮𝗹𝗹 𝘁𝗵𝗲 𝗕𝗼𝘁'𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗮𝗻𝗱 𝗵𝗼𝘄 𝘁𝗵𝗲𝘆 𝘄𝗼𝗿𝗸 𝗯𝘆 𝗰𝗹𝗶𝗰𝗸𝗶𝗻𝗴 𝗼𝗻 𝘁𝗵𝗲 » 📚 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !
<b>""",

        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ 𝙰𝚍𝚍 𝚖𝚎 𝚝𝚘 𝚢𝚘𝚞𝚛 𝙶𝚛𝚘𝚞𝚙 ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
                [
                    InlineKeyboardButton(
                        "📚 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !", callback_data="cbhelp")
                ],
                [
                   InlineKeyboardButton(
                       "👥 ᴏғғɪᴄɪᴀʟ ɢʀᴏᴜᴘ", url=f"https://t.me/ZeusSupport"
                   ),
                   InlineKeyboardButton(
                       "📣 ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/ZeusBotsNetwork"
                   )
                ],
                [
                    InlineKeyboardButton(
                        "👑ᴅᴇᴠᴇʟᴏᴘᴇʀ", callback_data="cbguide")
                ],
            ]
        ),
        disable_web_page_preview=True
        )
