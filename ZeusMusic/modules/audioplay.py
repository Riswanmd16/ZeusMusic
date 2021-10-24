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



# this module i created only for playing music using audio file, idk, because the audio player on play.py module not working
# so this is the alternative
# audio play function

from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from ZeusMusic.services.callsmusic import callsmusic, queues

from ZeusMusic.services.converter import converter
from ZeusMusic.services.downloaders import youtube

from ZeusMusic.config import BOT_NAME as bn, DURATION_LIMIT, UPDATES_CHANNEL,SUPPORT_GROUP
from ZeusMusic.helpers.filters import command, other_filters
from ZeusMusic.helpers.decorators import errors
from ZeusMusic.helpers.errors import DurationLimitError
from ZeusMusic.helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(command("stream") & other_filters)
@errors
async def stream(_, message: Message):

    lel = await message.reply("🔁 **Processing** sound...")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Support",
                        url=f"https://t.me/ZeusSupport"),
                    InlineKeyboardButton(
                        text="Updates",
                        url=f"https://t.me/ZeusBotsNetwork"),
                ],
                [
                    InlineKeyboardButton(
                        text="Created by",
                        url=f"https://t.me/ZeusBotsNetwork")
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Videos longer than {DURATION_LIMIT} minute(s) aren't allowed to play!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("you did not give me audio file or yt link to stream!")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"https://telegra.ph/file/03b7244c8901a3f0c55d3.jpg",
        reply_markup=keyboard,
        caption=f"💡 **Track added to the queue**\n\n🎧 **Request by**: {costumer}\n🔢 **Track position**: » `{position}` «")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"https://telegra.ph/file/03b7244c8901a3f0c55d3.jpg",
        reply_markup=keyboard,
        caption=f"💡 **Status**: **Playing**\n\n🎧 **Request by**: {costumer}\n🎛️ **Powered** by @ZeusBotsNetwork"
        )
        return await lel.delete()
