import discord
import os, sys
import configparser
import requests
import random


version = 1.3

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

class aclient(discord.Client):
	async def on_ready(self):
		print(chr(27) + "[2J")
		print("Project Alphanus - Copyright, AegisXKio")
		print("--Info--")
		print("I am user " + client.user.name + "#" + str(client.user.discriminator))
		print("On " + str(len(client.guilds)) + " guilds")
		print("With 2 commands")
		print("Current Version: " + str(version))
		if float(r.text) != version:
			print("Version " + r.text + " is available! please update ASAP!")
		print("--Info--")
		print("Alright, whose ready to catch some bad guys?")
	async def on_message(self, message):
		if message.guild == None and message.author != self.user:
			print(str(message.author.name + " has messaged me."))
			try:
				await client.get_guild(int(Config.get("Config","server"))).get_member(message.author.id).ban()
			except discord.errors.Forbidden:
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
						r = requests.get("https://raw.githubusercontent.com/AegisTeam/Project-Alphanus/master/alph.py")
						f1 = open('./alph.py', 'w+')
						f1.write(r.text)
						f1.close()
						print("Restarting.")
						os.execl(sys.executable, sys.executable, *sys.argv, "update")

				else:
					print("..But they're an admin. That's okay.")
					embed = discord.Embed(colour=discord.Colour(0x4a90e2))
					embed.set_author(name="Project Alphanus - A Honeytrap for Aegis")
					embed.add_field(name="By", value="KioˣAegis", inline=True)
					embed.add_field(name="Version", value=version, inline=True)
					embed.add_field(name="Commands", value="``restart``, ``shutdown``", inline=False)
					await message.author.send(embed=embed)
				return
			embed = discord.Embed()
			embed.set_author(name="Autoban Triggered.")
			embed.add_field(name="Text", value=message.content, inline=False)
			embed.add_field(name="ID", value=str(message.author.id))
			client.get_channel(int(Config.get("Config","chan"))).send(embed=embed) 
	async def on_relationship_add(self, rel):
		print("No thanks, " + rel.user.name + ". I don't need friends.")
		await rel.delete()
client = aclient()
client.run(Config.get("Config","token"), bot=False)
