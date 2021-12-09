
    

    #!./.venv/bin/python

#Copyright 2021, Dascalu Stefan-Teodor
#	This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/\>.

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--token", help="show token")
args = parser.verbosity
if args.verbosity:
    print("OTEyODY4MTQ0NDE3MjQzMTg2.YZ2MtQ.yxeuda3MApC9zgiTeCf0WIsP1EQ")

import discord      # base discord module
import code         # code.interact
import os           # environment variables
import inspect      # call stack inspection
import random       # dumb random number generator
import youtube_dl

from discord.ext import commands    # Bot class and utils

################################################################################
############################### HELPER FUNCTIONS ###############################
################################################################################

# log_msg - fancy print
#   @msg   : string to print
#   @level : log level from {'debug', 'info', 'warning', 'error'}
def log_msg(msg: str, level: str):
    # user selectable display config (prompt symbol, color)
    dsp_sel = {
        'debug'   : ('\033[34m', '-'),
        'info'    : ('\033[32m', '*'),
        'warning' : ('\033[33m', '?'),
        'error'   : ('\033[31m', '!'),
    }

    # internal ansi codes
    _extra_ansi = {
        'critical' : '\033[35m',
        'bold'     : '\033[1m',
        'unbold'   : '\033[2m',
        'clear'    : '\033[0m',
    }

    # get information about call site
    caller = inspect.stack()[1]

    # input sanity check
    if level not in dsp_sel:
        print('%s%s[@] %s:%d %sBad log level: "%s"%s' % \
            (_extra_ansi['critical'], _extra_ansi['bold'],
             caller.function, caller.lineno,
             _extra_ansi['unbold'], level, _extra_ansi['clear']))
        return

    # print the damn message already
    print('%s%s[%s] %s:%d %s%s%s' % \
        (_extra_ansi['bold'], *dsp_sel[level],
         caller.function, caller.lineno,
         _extra_ansi['unbold'], msg, _extra_ansi['clear']))

################################################################################
############################## BOT IMPLEMENTATION ##############################
################################################################################

# bot instantiation
bot = commands.Bot(command_prefix='!')

# on_ready - called after connection to server is established
@bot.event
async def on_ready():
    log_msg('logged on as <%s>' % bot.user, 'info')

# on_message - called when a new message is posted to the server
#   @msg : discord.message.Message
@bot.event
async def on_message(msg):
    # filter out our own messages
    if msg.author == bot.user:
        return

    log_msg('message from <%s>: "%s"' % (msg.author, msg.content), 'debug')

    # overriding the default on_message handler blocks commands from executing
    # manually call the bot's command processor on given message
    await bot.process_commands(msg)

# roll - rng chat command
#   @ctx     : command invocation context
#   @max_val : upper bound for number generation (must be at least 1)
@bot.command(brief='Generate random number between 1 and <arg>')
async def roll(ctx, max_val: int):
    # argument sanity check
    if max_val < 1:
        raise Exception('argument <max_val> must be at least 1')

    await ctx.send(random.randint(1, max_val))

# roll_error - error handler for the <roll> command
#   @ctx     : command that crashed invocation context
#   @error   : ...
@roll.error
async def roll_error(ctx, error):
    await ctx.send(str(error))
    
# implementing the music part
@bot.command()
async def playYT(ctx, url : str):
	song_there = os.path.isfile("song.mp3")
	try:
		if song_there:
			os.remove("song.mp3")
	except PermissionError:
		await ctx.send("Wait for the current playing music to end or use the 'stop' command")
		return

	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	await voiceChannel.connect()
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])

	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			os.rename(file, "song.mp3")

	voice.play(discord.FFmpegPCMAudio("song.mp3"))

@bot.command()
async def play(ctx, url : str):
	channel = ctx.message.author.voice.channel
	voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
	voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if voice_client == None:
		await channel.connect()
		bt = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	bt.play(discord.FFmpegPCMAudio(url))
	await ctx.send("Playing: " + url)
	del bt

@bot.command()
async def scram(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client != None:
        await voice_client.disconnect)
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def list(ctx):
	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			await ctx.send(file)

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot,voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()



################################################################################
############################# PROGRAM ENTRY POINT ##############################
################################################################################

if __name__ == '__main__':
  
    # launch bot (blocking operation)
    bot.run('OTEyODY4MTQ0NDE3MjQzMTg2.YZ2MtQ.yxeuda3MApC9zgiTeCf0WIsP1EQ')
