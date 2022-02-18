# ZeusMusic

<h3>Requirements 📝</h3>

- FFmpeg
- NodeJS [nodesource.com](https://nodesource.com/)
- Python 3.7 or higher
- [PyTgCalls](https://github.com/pytgcalls/pytgcalls)
- [MongoDB](https://cloud.mongodb.com/)
- [2nd Telegram Account](https://telegram.org/blog/themes-accounts#multiple-accounts) (needed for userbot)

### 🧪 Get `SESSION_NAME` from below:

[![GenerateString](https://img.shields.io/badge/repl.it-generateString-yellowgreen)](https://replit.com/@sathish2004/Zeus-Clone-Repl)


## Features 🔮

- Thumbnail Support
- Playlist Support
- Youtube, Local playback support
- Settings panel
- Control with buttons
- Userbot auto join
- Keyboard selection support for youtube play
- Lyrics Scrapper
- Unlimited Queue
- Broadcast Bot
- Statistic Collector
- Block / Unblock (restrict user for using your bot)
- Check Bot statastic

## Commands 🛠

- `/play <song name>` - play song you requested
- `/playlist` - Show now playing list
- `/song <song name>` - download songs you want quickly
- `/search <query>` - search videos on youtube with details
- `/vsong <song name>` - download videos you want quickly
- `/lyric <song name>` - lyrics scrapper
- `/reload` - Refresh bot core
- `/uptime` - check the bot uptime status
- `/ping` - check the bot ping status
- `/stats` - see the bot statistic

#### Admins Only 👷‍♂️
- `/player` - open music player settings panel
- `/pause` - pause song play
- `/resume` - resume song play
- `/skip` - play next song
- `/end` - stop music play
- `/musicplayer on` - to disable music player in your group
- `/musicplayer off` - to enable music player in your group
- `/userbotjoin` - invite assistant to your chat
- `/userbotleave` - remove assistant from your chat
- `/auth` - authorized people to access the admin commands
- `/unauth` - deauthorized people to access the admin commands
- `/control` - open the music player control panel

### Sudo User 🧙‍♂️
- `/userbotleaveall` - order the assistant to leave all groups
- `/broadcast` - send a broadcast message from the bot
- `/block` - block people for using your bot
- `/unblock` - unblock people you blocked for using your bot
- `/blocklist` - show the list of all people who's blocked for using your bot
- `/frestart` - Restart heroku server
- `/update` - Update your bot to current version

## 🔎 Inline Search Support
- just type the bot username in any chat, example: "`@{BOT_USERNAME} Faded Alan Walker`", then bot will give you a results of the query you search in inline mode.

## VPS Deployment 📡

```sh
sudo apt update && apt upgrade -y
sudo apt install git curl python3-pip ffmpeg -y
pip3 install -U pip
curl -sL https://deb.nodesource.com/setup_16.x | bash -
sudo apt-get install -y nodejs
npm i -g npm
git clone https://github.com/ZeusNetworks/ZeusMusic # clone the repo.
cd ZeusMusic
pip3 install -U -r requirements.txt
cp example.env .env # use vim to edit ENVs
vim .env # fill up the ENVs (Steps: press i to enter in insert mode then edit the file. Press Esc to exit the editing mode then type :wq! and press Enter key to save the file).
python3 main.py # run the bot.
```


### Special Credits 💖
- [Laky](https://github.com/Laky-64) & [Andrew](https://github.com/AndrewLaneX): PyTgCalls
- [RojSerBest](https://github.com/rojserbest) CallsMusic Developer
- [TeamDaisyX](https://github.com/TeamDaisyX) for base code


## Heroku Deployment 
The easy way to host this bot, deploy to Heroku, Change the app country to Europe (it will help to make the bot stable).

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Riswanmd16/ZeusMusic)
