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


from pyrogram import Client, errors
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from youtubesearchpython import VideosSearch


@Client.on_inline_query()
async def inline(client: Client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "menu":
        await client.answer_inline_query(
            query.id,
            results=menus,
            switch_pm_text="Menu",
            switch_pm_parameter="help",
            cache_time=0,
        )
    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text="search a youtube video",
            switch_pm_parameter="help",
            cache_time=0,
        )
    else:
        search = VideosSearch(search_query, limit=50)

        for result in search.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=result["title"],
                    description="{}, {}.".format(
                        result["duration"], result["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "/play https://www.youtube.com/watch?v={}".format(result["id"])
                    ),
                    thumb_url=result["thumbnails"][0]["url"],
                )
            )

        try:
            await query.answer(results=answers, cache_time=0)
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: search timed out",
                switch_pm_parameter="",
            )


# ==================
# Tested

menus = [
    InlineQueryResultArticle(title="Start", description="Start a bot",
                             input_message_content=InputTextMessageContent("/start")),
    InlineQueryResultArticle(title="Info Bot", description="Info about this bot",
                             input_message_content=InputTextMessageContent("/info")),
]
