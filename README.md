# telegram-bot-template
Python Aiograme 3.x
Telegram Bulletin Board Bot for a small audience.
There are SQLite databases on SQLAlchemy. The database contains information about ads and premium users. 30 days after the ad is submitted, it is automatically deleted. An regular user cannot submit more than 3 ads.

Users can:
- add/delete/view your own ads
- search for ads by category

Administrator can:
- edit/delete ads
- add/remove/renew premium for users

The ad includes:
- category
- description
- price
- one photo (Because when displaying ads, there is an Inline button that allows you to write to the user if you click on it.
This is done for ease of communication, since several photos in a telegram are an album data type and it is impossible to attach an inline button to such a message)

There is a /help command that displays introductory information.
