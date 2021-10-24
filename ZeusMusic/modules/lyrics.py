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


import requests
from pyrogram import Client
from ZeusMusic.config import BOT_USERNAME
from ZeusMusic.helpers.filters import command


@Client.on_message(command(["lyric", f"lyric@{BOT_USERNAME}"]))
async def lirik(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("**give a lyric name too !**")
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text("🔎 **searching lyrics...**")
        resp = requests.get(f"https://tede-api.herokuapp.com/api/lirik?l={query}").json()
        result = f"{resp['data']}"
        await rep.edit(result)
    except Exception:
        await rep.edit("**Lyrics not found.** please give a valid song name !")
