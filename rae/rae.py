#! /usr/bin/python3
import bs4, pathlib, requests, sys, urllib.parse

if len(sys.argv) < 2:
	print('usage: python3 rae.py wordlist.txt [wordlist.txt ...]')

definitions = open('definitions.txt', 'w')
info = '''
En aquest document hi ha totes les paraules que hem de posar al mini-diccionari,
amb les definicions de la rae. No ho he fet a mà, no ho he revisat.
Això és literalment copiat i enganxat, surten totes les defiinicions de cada paraula (que hi ha a la rae).
S'ha de triar la que millor s'adapta al context del poema, i si no n'hi ha cap, adaptar-ne o buscar-ne una.
Si hi trobeu cap error, obriu-me.

'''.splitlines()

line_len = 0
for line in info:
	if len(line) > line_len:
		line_len = len(line)

info.insert(0, ''.center(line_len + 4, '#'))
info.append(''.center(line_len + 4, '#'))

for line in info:
	line = line.center(line_len + 2, ' ').center(line_len + 4, '#')
	line += '\n'
	definitions.write(line)


for wordlist in sys.argv[1:]:
	words = open(wordlist).readlines()


	for word in words:
		definitions.write('\n\n\n')

		query = urllib.parse.quote(word.strip('\\n'))
		if ('%0A' in query[-3:]):
			query = urllib.parse.quote(word.strip('\\n'))[:-3]
		print(query)
		res = requests.get('https://dle.rae.es/' + query)
		print('response code: ' + str(res.status_code)) 
		soup = bs4.BeautifulSoup(res.text, 'html.parser')
		definitions.write(word)
		try:
			definitions.write(soup.select_one('#resultados').select_one('article').getText())
		except Exception:
			definitions.write('\nnot found')


definitions.close()