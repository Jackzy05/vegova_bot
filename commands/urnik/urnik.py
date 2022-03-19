from .parser import *
import discord
import datetime

# Vrne datum za včeraj, danes ali jutri
def datum(dan):
	match dan:
		case "danes":
			date = str(datetime.date.today()).split('-')
		case "jutri":
			date = str(datetime.date.today() + datetime.timedelta(days=1)).split('-')
		case "včeraj":
			date = str(datetime.date.today() + datetime.timedelta(days=-1)).split('-')

	return f"{date[2]}. {date[1]}. {date[0]}"

async def table(message):
	args = message.content.split()

	if len(args) != 3:
		embed = discord.Embed(
			description = "Pravilen format: `ea/urnik [razred] [včeraj/danes/jutri]`",
			color = 0xFF0000
		)

		embed.set_author(
			name="Napaka", 
			icon_url="https://media.discordapp.net/attachments/737046647476846673/825812580912201748/cancel.png")

		await message.channel.send(embed = embed)
		return

	if args[2] not in ["včeraj", "danes", "jutri"]:
		embed = discord.Embed(
			description = "Urnik lahko pošljem samo za `včeraj`, `danes` in `jutri` !",
			color = 0xFF0000
		)

		embed.set_author(
			name = "Napaka", 
			icon_url = "https://media.discordapp.net/attachments/737046647476846673/825812580912201748/cancel.png")

		await message.channel.send(embed = embed)
		return

	try:	
		get_html(args[1])
	except KeyError as error:
		embed = discord.Embed(
			description = f"KeyError: {error}",
			color = 0xFF0000
		)

		embed.set_author(
			name="Napaka", 
			icon_url="https://media.discordapp.net/attachments/737046647476846673/825812580912201748/cancel.png")

		await message.channel.send(embed = embed)
		return
	
	urnik = parse_table(get_table(args[2]))
	
	if type(urnik) == type(False):
		match args[2]:
			case "včeraj":
				msg = f"{args[2].capitalize()} ni bilo pouka."
			case _:
				msg = f"{args[2].capitalize()} ni pouka."
		
		embed = discord.Embed(
			description = msg,
			color = 0xFF0000
		)

		embed.set_author(
			name="Napaka", 
			icon_url="https://media.discordapp.net/attachments/737046647476846673/825812580912201748/cancel.png")

		await message.channel.send(embed = embed)
		return

	embed = discord.Embed(
		title = f"{args[1].upper()} urnik za {datum(args[2])}",
		url = get_url(args[1]),
		color = 0x007bac
	)

	embed.set_thumbnail(url="https://www.gim-idrija.si/files/2020/09/index.png")

	predmeti = urnik[0]
	ure = urnik[1]

	for i, predmet in enumerate(predmeti):
		embed.add_field(
			name = f"{str(ure[i])}. Ura, {čas_ur[ure[i]-1]}", 
			value = predmet, 
			inline = False
		)
	
	await message.channel.send(embed = embed)