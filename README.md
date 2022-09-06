# Discord-bot written by Ezekiel Penrod 9/6/2022

Discord bot using the wavelink/lavalink combo and nextcord.

This bot can play music from Youtube. 

If you use this bot please keep it on a small server or only use with a group of friends.

This bot is not hosted you will have to run it locally.

You will have to set up your own bot on discord (https://discord.com/developers/docs/intro) and plug in the bot key at the bottom of the code.

With this bot you can:
start/stop
pause/resume
play/skip
disconnect/join
queue

the prefix is "!"
example: 
!play or !p (song name)
!skip or !s- (to skip song)

-to queue up songs just keep adding them by using the play command.

the bot will post a thumbnail and song title in discord when playing a song


Overall this was a fun project. I ran into some hickups involving the wavelink library as one of their predefined functions was always returning True thus causing my code to error out. Once that was solved, figuring out how to skip a song took longer then I'd like to admit but it was good learning.

I hope you enjoy :)
