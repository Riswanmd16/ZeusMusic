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
import traceback
from functools import wraps

from pyrogram import Client
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden

from ZeusMusic.config import LOG_CHANNEL


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    else:
        result.append(small_msg)

    return result


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await Client.leave_chat(message.chat.id)
            return
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            error_feedback = split_limits(
                "**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await Client.send_message(LOG_CHANNEL, x)
            raise err

    return capture
