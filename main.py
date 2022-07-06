from commands import *
import discord

client = discord.Client()

with open("token.txt", "r") as f:
	token = f.read()

@client.event
async def on_ready():
	print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
	if message.content.startswith("veg/"):
		args = message.content[len("veg/"):]
		command = args.split()
		
		if command[0] in commands:
			await commands[command[0]](message)
		else:
			embed = discord.Embed(
				description = f"`{command[0]}` ni veljavna komanda. Uporabite `veg/help` za celoten seznam komand", 
				color = 0xFF0000)
			embed.set_author(
				name = "Napaka", 
				icon_url = "https://media.discordapp.net/attachments/737046647476846673/825812580912201748/cancel.png")

			await message.channel.send(embed = embed)

commands = {
	"urnik": table,
	"ucilnica": ucilnica,
	"vfinder": vfinder,
	"help": help
}

client.run(token)