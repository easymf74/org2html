def isLink_in(Inhalt):
	'''
	Teste ob die Syntax für einen Link innerhalb der Zeile ist.
	Benötigt: zu prüfenden String
	Gibt zurück: Tulpel mit folgenden Feldern:
		0: True, wenn Syntax eines Links erfüllt ist, sonnst False
		1: Index an dem der URL-Text im übergebnen String beginnt
		2: Index an dem der Linkname endet
		3: URL des Links
		4: LinkText
	
	Syntax eines Links:
	Ein Link beginnt mit "[[" und endet mit "]]"
	Zwischen den beiden Marken befindet sich 
		* eine schließende eckige Klammer und 
		* eine öffnede eckige Klammer
	'''
	
	link= False
	endLink=-1
	URL=''
	LinkName=''
	beginLink =Inhalt.find('[[')
	if beginLink >-1:
		beginLink+=2
		endLink = Inhalt[beginLink:].find(']]')
		if endLink > -1:
			endLink+=beginLink
			endURL = Inhalt[beginLink:endLink].find(']')
			if endURL > -1:
				endURL+=beginLink
				beginLinkName = Inhalt[endURL:endLink].find('[')
				if beginLinkName > -1:
					beginLinkName+=endURL
					# es ist ein Link
					beginLinkName+= 1
					URL= Inhalt[beginLink:endURL]
					LinkName = Inhalt[beginLinkName:endLink]
					link= True
			else:
				# Link mit einseitigem Körper
				URL= Inhalt[beginLink:endLink]
				LinkName = URL
				link=True
	return link, beginLink, endLink, URL, LinkName, 'geändert'

def isURL(Inhalt):
	'''
	Diese Funktion soll prüfen ob ein Linktext 
	die Merkmale einer Webadresse enthällt.
	Wenn ja soll True zurückgegeben werden, sonst False
	Folgende Merkmale soll eine Webadresse kennzeichen
	* url beginnt mit http:// oder https:// oder www.
	* url enthält einen Punkt direkt gefolgt von einem Buchstaben
	Regex: ^(http:\/\/|https:\/\/|www.).*\.\w{2}
	'''
	return test("^(http:\/\/|https:\/\/|www.).*\.\w{2}",Inhalt)
