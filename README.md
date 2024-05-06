# Bulletin Board Telegram Bot

Python Aiogram 3.x

<p align="center">
<img src="https://i.imgur.com/ukqMmO7.jpg" width=600 height=510.4>
</p>

Telegram Bulletin Board Bot for a small audience.

There are SQLite databases on SQLAlchemy. The database contains information about ads and premium users. 30 days after the ad is submitted, it is automatically deleted. An regular user cannot submit more than 3 ads.

## Quick install
You can delete file database.db and change everything you need.

1. Create Virtual environment.
2. Install packages: pip install -r requirements.txt
3. Change filename ".env.dist" to ".env" and write your values (Bot token, Admins list etc).
4. Enter Virtual environment and run Bot by your code editor or terminal command: python main.py
5. Check it in Telegram.
6. Write command /image and set welcome image for command /start.
7. Enjoy!

## Features
Users can:
- add new advertisement for sale or offering some service
- check and delete your own advertisements
- search for advertisements of other users by category
- write to user`s advertisements by using only one button

Administrator can:
- edit and delete any advertisement
- manage the list of premium subscribers right in the bot
- add new premium users by their IDs
- delete premium users for some reasons
- prolong their premium subsriptions
- set and change start image

The ad includes:
- category
- description
- price
- one photo (Because when displaying ads, there is an Inline button that allows you to write to the user if you click on it.
This is done for easy of communication, since several photos in a Telegram are an album data type and it is impossible to attach an inline button to such a message)

## Commands
- /start - start command to begin work with bot or to restart bot if something gone wrong, update is not handled etc.
- /help - command that displays introductory information.
- /admin - command to log in to the admin panel only if your ID is in .env - ADMINS, if not nothing will happen.
- /image - command to change/set welcome image that appears with command "/start".

### User FSM Table

<p align="center">
<img src="https://i.imgur.com/0WBkgIS.png" width=426.7 height=683.3>
</p>

Thanks for watching. Hope you enjoy! Hope for your star!
