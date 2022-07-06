import discord
from .search import *

async def vfinder(message):
	args = message.content.split()
	optional_args = ["now", "Ponedeljek", "Torek", "Sreda", "Četrtek", "Petek"]
	error_msg = "https://media.discordapp.net/attachments/737046647476846673/825812580912201748/cancel.png"
	
	if len(args) > 4:
		embed = discord.Embed(
			description = "Pravilen format: `veg/vfinder [I. Priimek] (now/dan)`",
			color = 0xFF0000
		)

		embed.set_author(
			name = "Napaka", 
			icon_url = error_msg)

		await message.channel.send(embed = embed)
		return

	profesor = " ".join(args[1:3])

	if len(args) == 4:
		if args[3] not in optional_args:
			embed = discord.Embed(
				description = "Opcijski argumenti so lahko samo delovni dnevi ali `now`",
				color = 0xFF0000
			)

			embed.set_author(
				name = "Napaka", 
				icon_url = error_msg)

			await message.channel.send(embed = embed)
			return
		else:
			embed = discord.Embed(
				description = "Pridobivam podatke s spleta...",
				color = 0xFFFF00
			)

			msg = await message.channel.send(embed = embed)

			podatki = get_info(profesor, args[3])
			if podatki == "Ni zadetkov":
				embed = discord.Embed(
					title = f'Zadetki za {profesor}',
					description = "Ni zadetkov",
					color = 0x3bffd1
				)

				await msg.edit(embed = embed)
				return
			else:
				# NOW
				if args[3] == 'now':	
					embed = discord.Embed(
						title = f'Zadetki za {podatki["profesor"]}',
						color = 0x3bffd1
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
					
					await msg.edit(embed = embed)
				# DAILY
				else:
					embed = discord.Embed(
						title = f'Zadetki za {podatki[0][0]}',
						color = 0x3bffd1
					)
					
					for ura in podatki:
						cajt = ura[2].split()[0]
						čas_ure = " ".join(ura[2].split()[1:]).replace('[', "").replace(']', "")
						
						embed.add_field(
							name = f"{ura[1]} - {cajt}. ura",
							value = f"Čas: {čas_ure}\nUčilnica: {ura[3]}",
							inline = False
						)
		
					await msg.edit(embed = embed)
	# ALL
	else:
		embed = discord.Embed(
			description = "Pridobivam podatke s spleta...",
			color = 0xFFFF00
		)

		msg = await message.channel.send(embed = embed)
		
		podatki = get_info(profesor)
		if podatki == "Ni zadetkov":
			embed = discord.Embed(
				title = f'Zadetki za {profesor}',
				description = "Ni zadetkov",
				color = 0x3bffd1
			)

			await msg.edit(embed = embed)
			return
		
		embed = discord.Embed(
			title = f'Zadetki za {podatki[0][0]}',
			color = 0x3bffd1
		)

		for ura in podatki:
			cajt = ura[2].split()[0]
			čas_ure = " ".join(ura[2].split()[1:]).replace('[', "").replace(']', "")
			
			embed.add_field(
				name = f"{ura[1]} - {cajt}. ura",
				value = f"Čas: {čas_ure}\nUčilnica: {ura[3]}",
			)
		
		await msg.edit(embed = embed)