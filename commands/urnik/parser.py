from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests import get
from pandas import read_html
import datetime

# Naredi globalno spremenljivko urnik v kateri je shranjen pandas dataframe
def get_html(razred):	
	global global_razred
	global_razred = razred
	dataframe = read_html(f"https://www.easistent.com/urniki/30a1b45414856e5598f2d137a5965d5a4ad36826/razredi/{razredi[razred]}")
	global urnik
	urnik = dataframe[6]

# Vrne string datum, ki bo služil kot del ključa za urnik dataframe
def get_date(dan):
	match dan:
		case "danes":
			date = str(datetime.date.today()).split('-')
		case "jutri":
			date = str(datetime.date.today() + datetime.timedelta(days=1)).split('-')
		case "včeraj":
			date = str(datetime.date.today() + datetime.timedelta(days=-1)).split('-')

	if date[2][0] == "0":
		return f"{date[2]}. {date[1]}.".replace("0", "")
	else:
		date[1] = date[1].replace("0", "")
		return f"{date[2]}. {date[1]}."
	
# Vrne urnik dataframe
def get_table(dan):	
	dnevi = ["Ponedeljek", "Torek", "Sreda", "Četrtek", "Petek"]
	dan_index = datetime.datetime.today().weekday()
	
	match dan:
		case "danes":
			if dan_index not in [5, 6]:	
				ime_dneva = dnevi[dan_index]
			else:
				return False
		case "jutri":
			if dan_index + 1 not in [5, 6]:
				# Če je nedelja pol rab dobit podatke za naslednji teden zato uporab selenium magic
				if dan_index + 1 == 7:
					driver = webdriver.get(f"https://www.easistent.com/urniki/30a1b45414856e5598f2d137a5965d5a4ad36826/razredi/{razredi[global_razred]}")
					select = Select(driver.find_element_by_class('ednevnik-seznam_ur_teden-navigacija-teden'))
					
					soup = BeautifulSoup(driver.page_source, "html.parser")
					curr_option = soup.find("option", {"selected" : "selected"})
					select.select_by_value(curr_option.next_sibling['value'])
					driver.close()
					
					ime_dneva = dnevi[0]
				else:	
					ime_dneva = dnevi[dan_index + 1]
			else:
				return False
		case "včeraj":
			if dan_index - 1 not in [-1, 5]:	
				ime_dneva = dnevi[dan_index - 1]
			else:
				return False
	
	return urnik[f"{ime_dneva}  {get_date(dan)}"]

# Vrne tuple, ki ima v prvem elementu string predmetov, ur in ucilnic; v drugem pa ure za posamezen predmet
def parse_table(urnik):
	if type(urnik) == type(False):
		return False
	
	ure = []
	predmeti = []

	for i, ura in enumerate(urnik):
		if str(ura) != "nan":
			ure.append(i+1)
			predmeti.append(ura)

	return predmeti, ure

# kratka funckija ki vrne link iz katerega pridobimo podatke o urniku
def get_url(razred):
	return f"https://www.easistent.com/urniki/30a1b45414856e5598f2d137a5965d5a4ad36826/razredi/{razredi[razred]}"

# vse do 81 vrstice poskrbi da zapolnemo razredi dictionary, ki ima kot ključe vse razrede, za vrednosti pa njihove ID številke
razredi = {}
site = get("https://www.easistent.com/urniki/30a1b45414856e5598f2d137a5965d5a4ad36826/razredi/").text
soup = BeautifulSoup(site, "html.parser")

data = soup.find("select", id = "id_parameter")
options = data.find_all("option")

for option in options:
	razredi[option.text.lower()] = option['value']

čas_ur = [
	"7:30 - 8:15", 
	"8:20 - 9:05", 
	"9:10 - 9:55", 
	"10:00 - 10:45", 
	"11:05 - 11:50", 
	"11:55 - 12:40", 
	"12:45 - 13:30", 
	"13:35 - 14:20", 
	"14:25 - 15:10", 
	"15:30 - 16:15", 
	"16:20 - 17:05", 
	"17:10 - 17:55", 
	"18:00 - 18:45", 
	"18:50 - 19:35"
]