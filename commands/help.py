from discord import Embed

async def help(message):
	embed = Embed(
		title = "Vegova Asistent help page",
		description = """
			`< >` - Ti argumenti so nujni in jih je treba dodati. (Ne dodajajte < > v komande!) \n 
			`[ ]` - Ti argumenti niso nujni in jih ni potrebno dodajati. (Ne dodajajte [ ] v komande!) \n
			Izvorna koda: https://github.com/JakaSmrkolj/vegova_asistent
		""",
		color = 0x3bffd1
	)

	embed.add_field(
		name = "Vfinder",
		value = """
			`veg/vfinder <I. Priimek> [now/dnevi v tednu]` \n
			Primer: `veg/vfinder K. Kastelic Ponedeljek` \n
			Notes: 
			・Če boš to komando pošiljal med vikendom, bodo prikazani podatki za prihajajoči teden
			・Ta komanda je počasna ker uporablja knjižnico [selenium](https://selenium-python.readthedocs.io/)
		""",
		inline = False
	)

	embed.add_field(
		name = "Urnik",
		value = """
			`veg/urnik <razred> <včeraj/danes/jutri>` \n
			Primer: `veg/urnik r2c danes`
		""",
		inline = False
	)

	await message.channel.send(embed = embed)