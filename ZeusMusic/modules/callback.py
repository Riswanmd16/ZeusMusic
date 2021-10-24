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


from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from ZeusMusic.helpers.decorators import authorized_users_only
from ZeusMusic.config import BOT_NAME, BOT_USERNAME, OWNER, SUPPORT_GROUP, UPDATES_CHANNEL, ASSISTANT_NAME
from ZeusMusic.modules.play import cb_admin_check


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>👋 **𝗪𝗲𝗹𝗰𝗼𝗺𝗲**\n
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


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Hello there, welcome to the help menu !</b>
In this menu you can open several **Available Command** menus, in each command menu there is also a brief explanation of each **Command**
📝 by **@ZeusBotsNetwork**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 ʙᴀsɪᴄ ᴄᴍᴅ", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 ᴀᴅᴠᴀɴᴄᴇᴅ ᴄᴍᴅ", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 ᴀᴅᴍɪɴ ᴄᴍᴅ", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 sᴜᴅᴏ ᴜsᴇʀs", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📙 ᴏᴡɴᴇʀ ᴄᴍᴅ", callback_data="cbowner"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅ʙᴀᴄᴋ", callback_data="cbstart"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>📝 here is the basic commands</b>
🎧 [ GROUP VC CMD ]
/play (song name) - play song from youtube
/ytp (song name) - play song directly from youtube 
/stream (reply to audio) - play song using audio file
/player - show the list song in queue
/song (song name) - download song from youtube
/search (video name) - search video from youtube detailed
/vsong (video name) - download video from youtube detailed
/lyric - (song name) lyrics scrapper
🎧 [ CHANNEL VC CMD ]
/cplay - stream music on channel voice chat
/cplayer - show the song in streaming
/cpause - pause the streaming music
/cresume - resume the streaming was paused
/cskip - skip streaming to the next song
/cend - end the streaming music
/admincache - refresh the admin cache
/ubjoinc - invite the assistant for join to your channel
ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 : ℤ𝕖𝕦𝕤 𝔹𝕠𝕥𝕤 ℕ𝕖𝕥𝕨𝕠𝕣𝕜""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ʙᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>📝 here is the advanced commands</b>
/start (in group) - see the bot alive status
/reload - reload bot and refresh the admin list
/stats - show the bot statistic
/cache - refresh the admin cache
/restart - restart the bot without affecting music plays
/ping - check the bot ping status
/uptime - check the bot uptime status
ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 : ℤ𝕖𝕦𝕤 𝔹𝕠𝕥𝕤 ℕ𝕖𝕥𝕨𝕠𝕣𝕜""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ʙᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>📝 here is the admin commands</b>
/player - show the music playing status
/pause - pause the music streaming
/resume - resume the music was paused
/skip - skip to the next song
/end - stop music streaming
/userbotjoin - invite assistant join to your group
/auth - authorized user for using music bot
/deauth - unauthorized for using music bot
/control - open the player settings panel
/delcmd (on | off) - enable / disable del cmd feature
/musicplayer (on / off) - disable / enable music player in your group
/b and /tb (ban / temporary ban) - banned permanently or temporarily banned user in group
/ub - to unbanned user you're banned from group
/m and /tm (mute / temporary mute) - mute permanently or temporarily muted user in group
/um - to unmute user you're muted in group
ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 : ℤ𝕖𝕦𝕤 𝔹𝕠𝕥𝕤 ℕ𝕖𝕥𝕨𝕠𝕣𝕜""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ʙᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>📝 here is the sudo commands</b>
/userbotleaveall - order the assistant to leave from all group
/gcast - send a broadcast message trought the assistant
/rmr - to delete all the downloaded files and caches
/frestart - to force restart bots server
/logs - send logs file
/block (user id - duration - reason) - block user for using your bot
/unblock (user id - reason) - unblock user you blocked for using your bot
/blocklist - show you the list of user was blocked for using your bot
ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 : ℤ𝕖𝕦𝕤 𝔹𝕠𝕥𝕤 ℕ𝕖𝕥𝕨𝕠𝕣𝕜""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ʙᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbowner"))
async def cbowner(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>📝 here is the owner commands</b>
/broadcast - send a broadcast message from bot
📝 note: all commands owned by this bot can be executed by the owner of the bot without any exceptions.
ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 : ℤ𝕖𝕦𝕤 𝔹𝕠𝕥𝕤 ℕ𝕖𝕥𝕨𝕠𝕣𝕜""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ʙᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )





@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbback"))
@cb_admin_check
async def cbback(_, query: CallbackQuery):
    await query.edit_message_text(
        "**💡 here is the control menu of bot :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⏸ Pause", callback_data="cbpause"
                    ),
                    InlineKeyboardButton(
                        "▶️ Resume", callback_data="cbresume"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⏩ Skip", callback_data="cbskip"
                    ),
                    InlineKeyboardButton(
                        "⏹ End", callback_data="cbend"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⛔ Anti cmd", callback_data="cbdelcmds"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🛄 Group tools", callback_data="cbgtools"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Close", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbgtools"))
@cb_admin_check
@authorized_users_only
async def cbgtools(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>This is the feature information :</b>
💡 **Feature:** this feature contains functions that can ban, mute, unban, unmute users in your group.
and you can also set a time for the ban and mute penalties for members in your group so that they can be released from the punishment with the specified time.
❔ **usage:**
1️⃣ ban & temporarily ban user from your group:
   » type `/b username/reply to message` ban permanently
   » type `/tb username/reply to message/duration` temporarily ban user
   » type `/ub username/reply to message` to unban user
2️⃣ mute & temporarily mute user in your group:
   » type `/m username/reply to message` mute permanently
   » type `/tm username/reply to message/duration` temporarily mute user
   » type `/um username/reply to message` to unmute user
📝 note: cmd /b, /tb and /ub is the function to banned/unbanned user from your group, whereas /m, /tm and /um are commands to mute/unmute user in your group.
ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 : ℤ𝕖𝕦𝕤 𝔹𝕠𝕥𝕤 ℕ𝕖𝕥𝕨𝕠𝕣𝕜""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ʙᴀᴄᴋ", callback_data="cbback"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbdelcmds"))
@cb_admin_check
@authorized_users_only
async def cbdelcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>This is the feature information :</b>
        
**💡 Feature:** delete every commands sent by users to avoid spam in groups !
❔ usage:**
 1️⃣ to turn on feature:
     » type `/delcmd on`
    
 2️⃣ to turn off feature:
     » type `/delcmd off`
      
ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 : ℤ𝕖𝕦𝕤 𝔹𝕠𝕥𝕤 ℕ𝕖𝕥𝕨𝕠𝕣𝕜""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ʙᴀᴄᴋ", callback_data="cbback"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbhelps(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Hello there, welcome to the help menu !</b>
**In this menu you can open several available command menus, in each command menu there is also a brief explanation of each command**
🤖 Bots by **@ZeusBotsNetwork**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Basic Cmd", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 Advanced Cmd", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Admin Cmd", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Sudo Cmd", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📙 Owner Cmd", callback_data="cbowner"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📔 Fun Cmd", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏡 BACK TO HOME", callback_data="cbstart"
                    )
                ]
            ]
        )
    )
