from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_html(profesor):
	driver = webdriver.Chrome("C:/Users/Jaka/Documents/Path/chromedriver.exe")
	driver.get("https://vfinder.janhar.si/")

	search = driver.find_element_by_name("prof")
	search.send_keys(profesor)
	search.send_keys(Keys.RETURN)

	soup = BeautifulSoup(driver.page_source, "html.parser")

	driver.quit()

	return soup

def time_in_range(start, end, current):
    return start <= current <= end

def get_info(profesor):	
	soup = get_html(profesor)
	dnevi = ["Ponedeljek", "Torek", "Sreda", "Četrtek", "Petek", "Sobota", "Nedelja"]
	
	dan_index = datetime.today().weekday()
	time = datetime.now().strftime('%#H:%M')
	
	data = soup.find("tbody")
	if data == None:
		return "Ni zadetkov"
	
	data = data.find_all("td", text = dnevi[dan_index])

	if data == None:
		return "Ni zadetkov"

	for day in data:
		next = day.next_siblings

		podatki = [day.get_text()]
		[podatki.append(tag.get_text()) for tag in next]
			
		čas = podatki[1].split()
		začetek_ure = čas[1][1:]
		konec_ure = čas[-1][:-1]
		
		if time_in_range(začetek_ure, konec_ure, time):
			podatki = {
				"ura": podatki[1],
				"učilnica": podatki[2]
			}
			
			return podatki

	return "Ni zadetkov"