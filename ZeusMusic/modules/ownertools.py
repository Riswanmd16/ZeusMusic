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


import sys
import os
import time
import traceback
import asyncio
import shutil
import psutil
import heroku3

from pyrogram import Client, filters
from pyrogram.types import Message, Dialog, Chat
from pyrogram.errors import UserAlreadyParticipant
from datetime import datetime
from functools import wraps
from os import environ, execle, path, remove
from time import time

from ZeusMusic.services.callsmusic.callsmusic import client as pakaya
from ZeusMusic.helpers.database import db
from ZeusMusic.helpers.dbtools import main_broadcast_handler
from ZeusMusic.modules.song import humanbytes, get_text
from ZeusMusic.config import BOT_USERNAME, OWNER, SUDO_USERS, SUPPORT_GROUP, HEROKU_API_KEY, HEROKU_APP_NAME, HEROKU_URL
heroku_api = "https://api.heroku.com"
Heroku = heroku3.from_key(HEROKU_API_KEY)


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


# Stats Of Your Bot
@Client.on_message(filters.command("stats"))
async def botstats(_, message: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        text=f"**📊 stats Of** @{BOT_USERNAME} \n\n**🤖 Bot Version:** `v1.0.1` \n\n**🙎🏼 Users:** \n » **Users on PM:** `{total_users}` \n\n**💾 Disk Usage,** \n » **Disk Space:** `{total}` \n » **Used:** `{used}({disk_usage}%)` \n » **Free:** `{free}` \n\n**🎛 Hardware Usage,** \n » **CPU Usage:** `{cpu_usage}%` \n » **RAM Usage:** `{ram_usage}%`\n\n⏰ **Time** \n » **Start Time:** `{START_TIME_ISO}`\n » **Uptime:** `{uptime}`",
        parse_mode="Markdown",
        quote=True
    )
    disable_web_page_preview=True


@Client.on_message(filters.private & filters.command("broadcast") & filters.user(SUDO_USERS) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)


# Ban User
@Client.on_message(filters.command("block") & filters.user(SUDO_USERS))
async def ban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            "» This command for ban user from using your bot, read /help for more info !",
            quote=True,
        )
        return
    try:
        user_id = int(m.command[1])
        ban_duration = m.command[2]
        ban_reason = " ".join(m.command[3:])
        ban_log_text = f"🔁 Banning user... \n\nUser id: `{user_id}` \nDuration: `{ban_duration}` \nReason: `{ban_reason}`"
        try:
            await c.send_message(
                user_id,
                f"⚠️ **Sorry, you're Banned! From Using My Vc Music Services.** ⚠️ \n\nReason: `{ban_reason}` \nDuration: `{ban_duration}` day(s). \n\n**💬 Message from **Zeus Network Admins**: Ask in **@{SUPPORT_GROUP}** if you think this restriction on you for using Vc Music service was an mistake.",
            )
            ban_log_text += "\n\n✅ This notification was sent to that user"
        except:
            traceback.print_exc()
            ban_log_text += f"\n\n❌ **Failed sent this notification to that user** \n\n`{traceback.format_exc()}`"
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(ban_log_text, quote=True)
    except:
        traceback.print_exc()
        await m.reply_text(
            f"❌ An error occoured, Traceback is given below:\n\n`{traceback.format_exc()}`",
            quote=True,
        )




# Unban User
@Client.on_message(filters.command("unblock") & filters.user(SUDO_USERS))
async def unban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            "» This command for unban user, read /help for more info !", quote=True
        )
        return
    try:
        user_id = int(m.command[1])
        unban_log_text = f"🔁 Unbanning user... \n\n**user id:**{user_id}"
        try:
            await c.send_message(user_id, f"🎊 Congratulations, you were allowed to use Vc Music Services Again.\n\nThank you for reaching us **@{SUPPORT_GROUP}**")
            unban_log_text += "\n\n✅ This notification was sent to that user"
        except:
            traceback.print_exc()
            unban_log_text += f"\n\n❌ **Failed sent this notification to that user** \n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(unban_log_text, quote=True)
    except:
        traceback.print_exc()
        await m.reply_text(
            f"❌ An error occoured, traceback is given below:\n\n`{traceback.format_exc()}`",
            quote=True,
        )


# Banned User List
@Client.on_message(filters.command("blocklist") & filters.user(SUDO_USERS))
async def _banned_usrs(_, m: Message):
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ""
    async for banned_user in all_banned_users:
        user_id = banned_user["id"]
        ban_duration = banned_user["ban_status"]["ban_duration"]
        banned_on = banned_user["ban_status"]["banned_on"]
        ban_reason = banned_user["ban_status"]["ban_reason"]
        banned_usr_count += 1
        text += f"⫸ **User ID**: `{user_id}` \n⫸ **Ban Duration**: `{ban_duration}` \n⫸ **Banned Date**: `{banned_on}` \n⫸ **Ban Reason**: `{ban_reason}`\n\n"
    reply_text = f"⫸ **Total Banned Users:** `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open("banned-user-list.txt", "w") as f:
            f.write(reply_text)
        await m.reply_document("banned-user-list.txt", True)
        os.remove("banned-user-list.txt")
        return
    await m.reply_text(reply_text, True)

#heroku
async def edit_or_send_as_file(
    text: str,
    message: Message,
    client: Client,
    caption: str = "`Result!`",
    file_name: str = "result",
    parse_mode="md",
):
    """Send As File If Len Of Text Exceeds Tg Limit Else Edit Message"""
    if not text:
        await message.edit("`there is something other than text, aborting...`")
        return
    if len(text) <= 1024:
        return await message.edit(text, parse_mode=parse_mode)

    await message.edit("`output is too large, sending as file!`")
    file_names = f"{file_name}.text"
    open(file_names, "w").write(text)
    await client.send_document(message.chat.id, file_names, caption=caption)
    await message.delete()
    if os.path.exists(file_names):
        os.remove(file_names)
    return


heroku_client = heroku3.from_key(HEROKU_API_KEY) if HEROKU_API_KEY else None


def _check_heroku(func):
    @wraps(func)
    async def heroku_cli(client, message):
        heroku_app = None
        if not heroku_client:
            await message.reply_text("`Please Add Heroku API Key To Use This Feature!`")
        elif not HEROKU_APP_NAME:
            await edit_or_reply(
                message, "`Please Add Heroku APP Name To Use This Feature!`"
            )
        if HEROKU_APP_NAME and heroku_client:
            try:
                heroku_app = heroku_client.app(HEROKU_APP_NAME)
            except:
                await message.reply_text(
                    message,
                    "`Heroku Api Key And App Name Doesn't Match! Check it again`",
                )
            if heroku_app:
                await func(client, message, heroku_app)

    return heroku_cli


#restart bot
@Client.on_message(filters.command("frestart") & filters.user(SUDO_USERS))
@_check_heroku
async def restart(client: Client, message: Message, hap):
    await message.reply_text("`Restarting now, Please Wait...`")
    hap.restart()

#logs
@Client.on_message(filters.command("logs") & filters.user(SUDO_USERS))
@_check_heroku
async def logswen(client: Client, message: Message, happ):
    msg = await message.reply_text("`Please wait for a moment!`")
    logs = happ.get_log()
    capt = f"Heroku logs of `{HEROKU_APP_NAME}`"
    await edit_or_send_as_file(logs, msg, client, capt, "logs")

#Usage
@Client.on_message(filters.command("dynos") & filters.user(SUDO_USERS))
async def dyno_usage(client: Client, message: Message, happp):
    if dyno.fwd_from:
        return
    if dyno.sender_id == SUDO_USERS:
        pass
    else:
        return
    """
    Get your account Dyno Usage
    """
    die = await dyno.reply("**Processing...**")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await die.edit(
            "`Error: something bad happened`\n\n" f">.`{r.reason}`\n"
        )
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await die.edit(
        "**Dyno Usage**:\n\n"
        f" -> `Dyno usage for`  **{HEROKU_APP_NAME}**:\n"
        f"     •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
        f"**|**  [`{AppPercentage}`**%**]"
        "\n\n"
        " -> `Dyno hours quota remaining this month`:\n"
        f"     •  `{hours}`**h**  `{minutes}`**m**  "
        f"**|**  [`{percentage}`**%**]"
    )


