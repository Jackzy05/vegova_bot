import json
import discord
import requests

client = discord.Client()

@client.event
async def ucilnica(message):
	content = message.content.split()
	ucilnica = content[1]
	
	try:	
		data = json.loads(requests.get("http://193.2.190.182:6969/api/curnex/"+ucilnica).text)
	except Exception:
		await message.channel.send("Nekaj je šlo narobe pri requestih. Ali si dal pravo učilnico?")
		return 		

	trenutna_ura = data['current']
	naslednja_ura = data['next']

	embed = discord.Embed(
		title = "Zasedenost učilnice "+str(ucilnica),
		color = 0xf6c1ff
	)

	match len(trenutna_ura):
		case 0:
			embed.add_field(
				name = "Trenutna ura",
				value = "Učilnica je prazna.",
				inline = False
			)
		case 6:
			embed.add_field(
				name = "Trenutna ura",
				value = ":sandwich: Malica",
				inline = False
			)
		case _:				
			embed.add_field(
				name = "Trenutna ura",
				value = "・Razred: "+"`"+trenutna_ura[0]['className']+"`\n"+"・Profesor: "+"`"+trenutna_ura[0]['teacher']+"`\n"+"・Predmet: "+"`"+trenutna_ura[0]['name']+"`",
				inline = False
			)
	
	match len(naslednja_ura):
		case 0:
			embed.add_field(
				name = "Naslednja ura",
				value = "Učilnica bo prazna.",
				inline = False
			)
		case 6:
			embed.add_field(
				name = "Naslednja ura",
				value = ":sandwich: Malica",
				inline = False
			)
		case _:				
			embed.add_field(
				name = "Naslednja ura",
				value = "・Razred: "+"`"+naslednja_ura[0]['className']+"`\n"+"・Profesor: "+"`"+naslednja_ura[0]['teacher']+"`\n"+"・Predmet: "+"`"+naslednja_ura[0]['name']+"`",
				inline = False
			)

	await message.channel.send(embed = embed)