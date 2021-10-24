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

from functools import wraps
from time import time


def exec_time(func):
    @wraps(func)
    async def _time_it(*args, **kwargs):
        t1 = time()
        try:
            return await func(*args, **kwargs)
        finally:
            t2 = time()
            total = t2 - t1
            total = round(total, 3)
            print(f"{func.__name__} Took: {total} Seconds")
            return _time_it
