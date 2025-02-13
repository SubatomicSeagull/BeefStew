# BEEFSTEW has been updated!

## Beefstew version 1.4 patchnotes:

## Features:
- A fully functional music player! (its quite fragile still so please be careful)
- You can now gamble your joker score, please gamble responsibly...

## Fixes:
- A huge refactor implementing command cogs, this makes development a lot easier as now commands are abstracted into classes and a whole lot easier to keep track of
- disallowed the use of commands in DMs, where they wont work
- /ping hosts file is now refreshed every day
- +2 will now save your current nickname as well as just your score
- fixed permissions so now /set_logs cant be used by just anyone
- fixed some spelling errors

## Misc:
- set up an async loop for future commands to be multithreaded which should speed up CPU heavy commands like /ping drastically
- scrapped joke of the week :(

the music player was very hard to make and its still quite unstable so dont get your hopes up too much lol, I added the reboot command for a reason 
