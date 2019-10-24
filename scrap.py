from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
def getChapter(link):
	html = urlopen(link)
	a = html.read().splitlines()
	arr = []
	for index in range(len(a)):
		if '<div class="col-md-12 versiculos">' in str(a[index]):
			souph2 = BeautifulSoup(a[index+2].decode('utf-8'),'lxml')
			h2 = souph2.h2
			souph2.a.decompose()
			arr.append(h2.get_text().lstrip().rstrip())
			i = index+3
			w = 0
			while True:
				soup = BeautifulSoup(a[i].decode('utf-8'),'lxml')
				p = soup.p
				soup.a.decompose()
				arr.append(p.get_text().lstrip().rstrip())
				if ("<br" in str(a[i+1])):
					break
				w += 1
				i += 1
			break
	return arr


def firstChapterLinks():
	html2 = urlopen("https://bo.net.br/pt/ntlh/Genesis/1/")
	links = []
	livrosElement = BeautifulSoup(html2.read().decode('utf-8'),'html.parser').find_all("select", {"class": "livros"})
	livrosOptions = BeautifulSoup(str(livrosElement[0]),"lxml").find_all("option", {"value": re.compile("^https")})
	for selects in range(len(livrosOptions)):
		links.append(str(BeautifulSoup(str(livrosOptions[selects]),"lxml").option["value"]))
	return links

def numeroDeCapitulos(link):
	html2 = urlopen(str(link))
	capitulosElement = BeautifulSoup(html2.read().decode('utf-8'),'html.parser').find_all("select", {"class": "capitulos"})
	capitulosOptions = BeautifulSoup(str(capitulosElement[0]),"lxml").find_all("option", {"value": re.compile("^https")})
	return len(capitulosOptions)

def getNomeCapEAbbr(link):
	relacoes = [("Gênesis","gn"),("Êxodo","ex"),("Levítico","lv"),("Números","nm"),("Deuteronômio","dt"),("Josué","js"),
("Juízes","jz"),("Rute","rt"),("1 Samuel","1sm"),("2 Samuel","2sm"),("1 Reis", "1rs"),("2 Reis","2rs"),("1 Crônicas","1cr"),
("2 Crônicas","2cr"),("Esdras","ed"),("Neemias","ne"),("Ester","et"),("Jó","jó"),("Salmos","sl"),("Provérbios","pv"),
("Eclesiastes","ec"),("Cânticos","ct"),("Isaías","is"),("Jeremias","jr"),("Lamentações","lm"),("Ezequiel","ez"),("Daniel","dn"),
("Oséias","os"),("Joel","jl"),("Amós","am"),("Obadias","ob"),("Jonas","jn"),("Miquéias","mq"),("Naum","na"),("Habacuque","hc"),
("Sofonias","sf"),("Ageu","ag"),("Zacarias","zc"),("Malaquias","ml"),("Mateus","mt"),("Marcos","mc"),("Lucas","lc"),("João","jo"),
("Atos","atos"),("Romanos","rm"),("1 Coríntios","1co"),("2 Coríntios","2co"),("Gálatas","gl"),("Efésios","ef"),("Filipenses","fp"),
("Colossenses","cl"),("1 Tessalonicenses","1ts"),("2 Tessalonicenses","2ts"),("1 Timóteo","1tm"),("2 Timóteo","2tm"),("Tito","tt"),
("Filemom","fm"),("Hebreus","hb"),("Tiago","tg"),("1 Pedro","1pe"),("2 Pedro","2pe"),("1 João","1jo"),("2 João","2jo"),
("3 João","3jo"),("Judas","jd"),("Apocalipse","ap")]

	html2 = urlopen(str(link))
	tituloPagina = str(BeautifulSoup(html2.read().decode('utf-8'),'html.parser').title.string)
	try:
		number = int(tituloPagina[0])
		titulo = re.findall("\d\s\S*\D",tituloPagina)[0]
		for t in range(len(relacoes)):
			if titulo.split(" ")[0] == relacoes[t][0].split(" ")[0] and titulo.split(" ")[1] == relacoes[t][0].split(" ")[1]:
                        	print(relacoes[t])
                        	return relacoes[t]

	except(ValueError):
		titulo = tituloPagina.split(" ")[0]
		for t in range(len(relacoes)):
			print(titulo, relacoes[t][0])
			if titulo == relacoes[t][0]:
				print(relacoes[t])
				return relacoes[t]

ind = 0
while ind <= len(firstChapterLinks()):
	fullBook = {}
	jsonBook = ""
	link = str(firstChapterLinks()[ind])
	print(getNomeCapEAbbr(link)[0])
	book = getNomeCapEAbbr(link)[0]
	if book == "Jó":
		break
	abbrev = getNomeCapEAbbr(link)[1]
	bookarray = []
	numeroCapitulos = numeroDeCapitulos(link)
	i = 1
	while i <= numeroCapitulos:
		capitulo = getChapter(link[:-2]+str(i)+"/")
		print (capitulo)
		bookarray.append(capitulo)
		i += 1;
	fullBook = {'abbrev':abbrev,'book':book,'chapters': bookarray}
	jsonBook = json.dumps(fullBook,ensure_ascii=False)
	with open("ntlh.json", 'a', encoding='utf-8') as file:
		file.write(jsonBook)
		file.close()
	ind += 1
