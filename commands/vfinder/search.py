from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

def get_info(profesor, type = None):
	# definicija konstant za pol
	dnevi = ["Ponedeljek", "Torek", "Sreda", "Četrtek", "Petek", "Sobota", "Nedelja"]
	dan_index = datetime.today().weekday()
	time = datetime.now().strftime('%#H:%M')
	
	driver = webdriver.Chrome("C:/Users/Jaka/Documents/Path/chromedriver.exe")
	driver.get("https://vfinder.janhar.si/")

	search = driver.find_element_by_name("prof")
	# če je vikend pol izbere naslednji tedn v select boxu
	if dan_index in [5, 6]:
		select = Select(driver.find_element_by_id('selectBox'))
		soup = BeautifulSoup(driver.page_source, "html.parser")
		
		curr_option = soup.find("option", {"style" : "color: rgb(48, 138, 164);"})
		select.select_by_value(curr_option.next_sibling['value'])
	
	search.send_keys(profesor)
	search.send_keys(Keys.RETURN)

	soup = BeautifulSoup(driver.page_source, "html.parser")

	driver.quit()	
	
	# pregleda če smo našl tabelo s podatki
	data = soup.find("tbody")
	if data == None:
		return "Ni zadetkov"
	
	data = data.find_all("td")

	# zafila list v katermu so listi (ure) s podatki
	ure = []
	for day in data:
		for tag in day.next_siblings:
			if tag.get_text() in dnevi:
				data = []
				[data.append(tag.get_text()) for tag in tag.previous_siblings]
				data.append(tag.get_text())
				[data.append(tag.get_text()) for tag in tag.next_siblings]
					
				ure.append(data)

	# če smo kot type argument dobil dan v tednu pol nastavmo type na daily zato da se bo izvedla koda v switchu
	if type in dnevi:
		dan = type
		type = 'daily'
	
	
	# glede na vhodn type argument returnamo parsane podatke (trenutna ura, vse ure ali ure za specifičn dan)
	match type:
		case 'now':
			for ura in ure:
				if ura[1] != dnevi[dan_index]:
					continue
				
				čas = ura[2].split()
				začetek_ure = čas[1][1:]
				konec_ure = čas[-1][:-1]

				if začetek_ure <= time <= konec_ure:
					podatki = {
						"profesor": ura[0],
						"dan": ura[1],
						"ura": ura[2],
						"učilnica": ura[3]
					}
						
					return podatki
			
			return "Ni zadetkov"
		case 'daily':
			podatki = []
			for ura in ure:
				if ura[1] != dan:
					continue
			
				podatki.append(ura)
			
			return podatki

		case None:
			return ure