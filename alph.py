import discord
import os, sys
import configparser


if os.path.isfile('./config.ini'):
	Config = configparser.ConfigParser()
	Config.read('config.ini')
else:
	Token= input("please enter your NON-BOT Token: ")
	f1=open('./config.ini', 'w+')
	f1.write('[Config]\ntoken: '+Token+"\n")
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
		print("With 1 command")
		print("--Info--")
		print("Alright, whose ready to catch some bad guys?")
	async def on_message(self, message):
		if message.guild == None and message.author != self.user:
			print(str(message.author.name + " has messaged me."))
			try:
				print(str(message.author.id))
				await client.get_guild(412360553361833984).get_member(message.author.id).ban()
			except discord.errors.Forbidden:
				if message.content.startswith("restart"):
					await message.author.send("I'm restarting now.")
					os.execl(sys.executable, sys.executable, *sys.argv)
				elif message.content.startswith("shutdown"):
					await message.author.send("Goodnight.")
					sys.exit(0)
				else:
					print("..But they're an admin. That's okay.")
					embed = discord.Embed(colour=discord.Colour(0x4a90e2))
					embed.set_author(name="Project Alphanus - A Honeytrap for Aegis")
					embed.add_field(name="By", value="KioˣAegis", inline=True)
					embed.add_field(name="Version", value="1.12", inline=True)
					embed.add_field(name="Commands", value="``restart`` ", inline=False)
					await message.author.send(embed=embed)
				return
			embed = discord.Embed()
			embed.set_author(name="Autoban Triggered.")
			embed.add_field(name="Text", value=message.content, inline=False)
			embed.add_field(name="ID", value=str(message.author.id))
			client.get_channel(433383852304629760).send(embed=embed) 
	async def on_relationship_add(self, rel):
		print("No thanks, " + rel.user.name + ". I don't need friends.")
		await rel.delete()
client = aclient()
client.run(Config.get("Config","token"), bot=False)
