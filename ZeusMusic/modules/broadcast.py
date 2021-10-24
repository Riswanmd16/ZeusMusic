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




import asyncio

from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant

from ZeusMusic.services.callsmusic.callsmusic import client as TodorokiProject
from ZeusMusic.config import SUDO_USERS

@Client.on_message(filters.command(["gcast"]))
async def broadcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        wtf = await message.reply("`starting broadcast...`")
        if not message.reply_to_message:
            await wtf.edit("please reply to a message to start broadcast!")
            return
        lmao = message.reply_to_message.text
        async for dialog in TodorokiProject.iter_dialogs():
            try:
                await TodorokiProject.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"`broadcasting...` \n\n**sent to:** `{sent}` chats \n**failed in:** {failed} chats")
                await asyncio.sleep(3)
            except:
                failed=failed+1
        await message.reply_text(f"`gcast succesfully` \n\n**sent to:** `{sent}` chats \n**failed in:** {failed} chats")
