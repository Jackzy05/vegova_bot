import discord
from .search import *

async def vfinder(message):
	args = message.content.split()

	if len(args) != 3:
		embed = discord.Embed(
			description = "Pravilen format: `veg/vfinder [I. Priimek]`",
			color = 0xFF0000
		)

		embed.set_author(
			name = "Napaka", 
			icon_url = "https://media.discordapp.net/attachments/737046647476846673/825812580912201748/cancel.png")

		await message.channel.send(embed = embed)
		return
	
	profesor = " ".join(args[1:])
	podatki = get_info(profesor)
	
	if podatki == "Ni zadetkov":
		embed = discord.Embed(
			title = f'Zadetki za {profesor}',
			description = "Ni zadetkov",
			color = message.author.color
		)

		await message.channel.send(embed = embed)
		return

	embed = discord.Embed(
		title = f'Zadetki za {profesor}',
		color = message.author.color
	)

	ura = podatki['ura'].split()[0]

	embed.add_field(
		name = "Učilnica",
		value = podatki['učilnica'],
		inline = False
	)
	
	embed.add_field(
		name = f"{ura}. ura",
		value = podatki['ura'].replace(ura, "").replace("[", "").replace("]", ""),
		inline = False
	)
	
	await message.channel.send(embed = embed)