# This Bot is Nuts!
This Bot Is Nuts! is a Project Moon-themed reaction proxy, made as a prank for a good friend. 

## Information
Whether or not the bot reacts to a user's messages is completely opt-in on the user's side. Other users cannot make the bot start reacting to your messages. 
This bot stores Discord numerical User IDs, and only Discord User IDs, in a .json file for the express purpose of determining which messages to react to.

## Features 
This Bot is Nuts! is a reaction macro. Its primary purpose is to react to messages that a user sends with a specified reaction.
This reaction, and whether or not the bot reacts to a user at all, is fully opt-in and configurable by the user. 

## Showcase 

## Self-Hosting
Create an application on the Discord Developer portal. 
When generating a Bot token, include the "Send Messages" and "Add Reactions" privileges, along with the Message Content Privileged Intent.
Store your token inside a .env file in the same folder as main.py, and name the environmental variable BOT_TOKEN.

You should be good now! All that's needed is to run main.py.

## License
This bot is licensed under The Unlicense. 
