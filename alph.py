import discord
import os, sys
import configparser
import requests
import random
import time
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging
import logging
handler = SentryHandler('https://ae2772c9ec7f4668bb92a12aa5ec932a:013a2755e15f457a9d7a68c490ff45e5@sentry.io/1188281')
handler.setLevel(logging.DEBUG)
setup_logging(handler)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
sys.stderr = logger.error
version = 2.01

if "update" in sys.argv:
	config = configparser.ConfigParser()
	config.read('config.ini')
	if len(config.sections()) == 0:
		config.add_section("Config")
	if config.get("Config","token", fallback=False) is False:
		Token= input("please enter your NON-BOT (selfbot) Token: ")
		config.set("Config", "token", Token)
	if config.get("Config","server", fallback=False) is False:
		Server= input("Please enter your Server's 18 digit ID: ")
		config.set("Config", "server", Server)
	if config.get("Config","chan", fallback=False) is False:
		Channel= input("Please enter the 18 digit ID of the channel P.A. will log to: ")
		config.set("Config", "chan", Channel)
	with open('config.ini', 'w') as configfile:
		config.write(configfile)
	print("Updated. Restarting.")
	os.execl(sys.executable, sys.executable, os.path.basename(__file__))

r = requests.get("https://raw.githubusercontent.com/AegisTeam/Project-Alphanus/master/version?" + str(random.randint(18,88)))

if os.path.isfile('./config.ini'):
	Config = configparser.ConfigParser()
	Config.read('config.ini')
else:
	Token= input("please enter your NON-BOT Token: ")
	Server= input("Please enter your Server's 18 digit ID: ")
	Channel= input("Please enter the 18 digit ID of the channel P.A. will log to: ")

	f1=open('./config.ini', 'w+')
	f1.write('[Config]\ntoken: '+Token+"\nserver:"+Server+"\nchan:"+Channel+"\n")
	f1.close()
	print("Restarting.")
	os.execl(sys.executable, sys.executable, *sys.argv)

async def menu(message):


	if message.content.startswith("restart"):
		await message.author.send("I'm restarting now.")
		os.execl(sys.executable, sys.executable, *sys.argv)


	elif message.content.startswith("shutdown"):
		await message.author.send("Goodnight.")
		sys.exit(0)


	elif message.content.startswith("update"):
		r = requests.get("https://raw.githubusercontent.com/AegisTeam/Project-Alphanus/master/version?" + str(random.randint(18,88)))
		if float(r.text) == version:
			await message.author.send("I'm already at the latest version. I don't need to update.")
		else:
			await message.author.send("Downloading...")
			r = requests.get("https://raw.githubusercontent.com/AegisTeam/Project-Alphanus/master/alph.py")
			await message.author.send("Updating...")
			f1 = open('./alph.py', 'w+')
			f1.write(r.text)
			f1.close()
			await message.author.send("Restarting...")
			os.execl(sys.executable, sys.executable, *sys.argv, "update")


	elif message.content.startswith("ping"):
		channel = message.channel
		t1 = time.perf_counter()
		await message.channel.trigger_typing()
		t2 = time.perf_counter()
		embed = discord.Embed()
		embed.set_author(name="Pong")
		embed.add_field(name="Time", value='{}ms'.format(round((t2-t1)*1000)))
		await message.author.send(embed=embed)


	elif message.content.startswith("inv"):
		if message.content == "inv" or message.content == "inv help":
			embed = discord.Embed(colour=discord.Colour(0x4a90e2))
			embed.set_author(name="Project Alphanus - A Honeytrap for Aegis")
			embed.add_field(name="Command - inv", value="Allows you to invite Alphanus into your server.")
			await message.author.send(embed=embed)
			n = message.content.strip("inv ")
			r = requests.post("https://discordapp.com/api/v6/invite/" + n, headers={"Authorization":Config.get("Config","token"), "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.5 Chrome/56.0.2924.87 Discord/1.6.15 Safari/537.36", "Content-Type":"application/json"})
	else:
		print("..But they're an admin. That's okay.")
		embed = discord.Embed(colour=discord.Colour(0x4a90e2))
		embed.set_author(name="Project Alphanus - A Honeytrap for Aegis")
		embed.add_field(name="By", value="KioˣAegis", inline=True)
		embed.add_field(name="Version", value=version, inline=True)
		embed.add_field(name="Commands", value="``restart``, ``shutdown``, ``update``, ``ping``", inline=False)
		await message.author.send(embed=embed)
	return
	embed = discord.Embed()
	embed.set_author(name="Autoban Triggered.")
	embed.add_field(name="Text", value=message.content, inline=False)
	embed.add_field(name="ID", value=str(message.author.id))
	client.get_channel(int(Config.get("Config","chan"))).send(embed=embed)

class aclient(discord.Client):


	async def on_ready(self):
		print(chr(27) + "[2J")
		print("Project Alphanus - Copyright, KioˣAegis")
		print("--Info--")
		print("I am user " + client.user.name + "#" + str(client.user.discriminator))
		print("On " + str(len(client.guilds)) + " guilds")
		print("With 5 commands")
		print("Current Version: " + str(version))
		if float(r.text) != version:
			print("Version " + r.text + " is available! please update ASAP!")
		print("--Info--")
		print("Alright, whose ready to catch some bad guys?")
	async def on_message(self, message):
		if message.guild == None and message.author != self.user:
			print(str(message.author.name + " has messaged me."))
			try:
				if message.author in client.get_guild(209566902522085376).members:
					await menu(message)
					return
				for guild in client.guilds:
					await guild.ban(discord.Object(id=message.author.id))
			except discord.errors.Forbidden:
					await menu(message)

	async def on_relationship_add(self, rel):
		r = requests.post('https://discordapp.com/api/v6/users/@me/relationships', data='{"username":"'+ rel.user.name +'","discriminator":'+str(rel.user.discriminator)+'}', headers={"Authorization":Config.get("Config","token"), "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.5 Chrome/56.0.2924.87 Discord/1.6.15 Safari/537.36", "Content-Type":"application/json"})
		print("Sure, I'll be your friend, " + rel.user.name + ".")
client = aclient()
client.run(Config.get("Config","token"), bot=False)
