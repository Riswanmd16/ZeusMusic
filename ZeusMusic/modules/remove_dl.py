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



import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from ZeusMusic.helpers.filters import command
from ZeusMusic.helpers.decorators import sudo_users_only, errors

downloads = os.path.realpath("downloads")
raw = os.path.realpath("raw_files")

@Client.on_message(command(["reload", "clean", "restart"]) & ~filters.edited)
@errors
async def clear_downloads(_, message: Message):
    ls_dir = os.listdir(downloads)
    if ls_dir:
        for file in os.listdir(downloads):
            os.remove(os.path.join(downloads, file))
        await message.reply_text("✅ **Reloaded All Admins!**\n🛰**System Reboted Successfully!!**\n🔊 **Enjoy Your Music!!!**",
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
        ),
    )
    else:
        await message.reply_text("❌ **Unable To Reload All Admins!**\n🛰**Reboting Failure!!**\n🔊 **Enjoy Your Music!!!**",
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
        ),
    )
        
@Client.on_message(command(["cache", "wipe", "rmr"]) & ~filters.edited)
@errors
@sudo_users_only
async def clear_raw(_, message: Message):
    ls_dir = os.listdir(raw)
    if ls_dir:
        for file in os.listdir(raw):
            os.remove(os.path.join(raw, file))
        await message.reply_text("✅ **Deleted all raw files**")
    else:
        await message.reply_text("❌ **No raw files**")
        
