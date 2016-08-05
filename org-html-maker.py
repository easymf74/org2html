#! /usr/bin/env python3
import sys # um Komandozeilen-Argumente auszulesen
from re import search as test # Teste auf RegularExpression
from os import path as pfad # um den Pfad zu ermitteln
from os import listdir as ls#Gibt eine Liste zurück, die alle Dateien und Unterordner des Ordners angibt, der mit path übergeben wurde.

''' Dieses Programm soll eine org-Datei einlesen und
in eine HTML-Datei umwandeln.
Dabei soll die Struktur der org-Datei so umgesetzt werden,
dass die HTML-Datei mit Hilfe von Java-Script die Funktion
des ein und ausblendens von Text durch Anklicken der Überschrift
ähnlich des Verhaltens im Emacs erhält.

ToDo:
- Innerhalb von pre-Blöcken sollen die Zeilen 1:1 übernommen werden.  
- Möglichkeit schaffen, Zeichen zu maskieren, damit sie nicht
	interpretiert werden, sonder 1:1 ausgegeben
- verschachtelte Listen testen


'''

#Konstanten
UEBERSCHRIFT=1
LISTE=2
TABELLE=4
ABSATZ=8
NOCOMMENT=999


def schreibeDocFus():
	'''
	Diese Funktion soll das abschließende Ende des Dokumentes schreiben.
	'''
	puffer.append('</div> <!-- Inhalt -->\n')
	puffer.append('</body>\n')
	puffer.append('</html>\n')

def schreibeDoctype():
	'''
	Diese Funktion soll den Standard Header der
	HTML-Datei in den Puffer schreiben.
	folgende Variabeln werden wenn gesetzt in dieser Funktion verarbeitet:

	listeCSS _______: Liste mit den Pfaden aller zugehörigen CSS-Dateien
	inCSS __________: Liste mit den Zeilen von zu intigrierenden CSS
	scripte ________: Liste mit den Pfadnamen aller zugehörigen Scripte
	inScript _______: Liste mit den Zeilen von zu intigrierenden Javascript
	onloadScript ___: Funktionsname, der beim Laden der HTML-Datei automatisch aufgerufen werden soll
	scriptHinweis __: Hinweis der Angezeigt wird, wenn JavaScript deaktiviert ist
	headline _______: Überschrift des Dokuments
	NaviLinks ______: Links der Navigationsleiste in Tupel Linkadresse im Feld 0, Linkname im Feld 1
	LoginPHP _______: Pfad zur Login-Datei
	LogoutPHP ______: Pfad der logout.php-Datei
	'''
	global tab, header, inCSS, inScript, CSSeinbetten, SCRIPTeinbetten, LoginPHP, LogoutPHP

	tab=0
	if privat:
		header.append(tab*' '+'<?php\n')
		tab+=2
		header.append(tab*' '+'session_start();\n')
		header.append(tab*' '+'if ( !isset($_SESSION["user"]) ) {\n')
		tab+=2
		header.append(tab*' '+'$url = "Location: '+LoginPHP+'?FEHLER=noLogin";\n')
		header.append(tab*' '+'header($url);\n')
		header.append(tab*' '+'exit;\n')
		tab-=2
		header.append(tab*' '+'}\n')
		tab-=2
		header.append(tab*' '+'?>\n')
		tab=0
	header.append('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n')
	header.append('<html xmlns="http://www.w3.org/1999/xhtml" lang="de" xml:lang="de">\n')
	header.append('<head>\n')
	tab+=2
	header.append(tab*' '+'<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n')
	header.append(tab*' '+'<title> ' + docTitel + ' </title>\n')

	if len(listeCSS):
		for css in listeCSS:
			if css:
				header.append(tab*' '+ '<link type="text/css" rel="stylesheet" href="'+css+'" />\n')
	else:
		CSSeinbetten=True
	
	if CSSeinbetten:
		inCSS=[
		'.grad1',
		'{',
		'	border-bottom: 2px solid black;',
		'	font-size: 2em;',
		'	font-weight:bold;',
		'	color: black;',
		'}',
		'.grad2',
		'{',
		'	border-bottom: 2px solid navy;',
		'	font-size: 1.8em;',
		'	color: navy;',
		'}',
		'.grad3',
		'{',
		'	border-bottom: 2px solid blue;',
		'	font-size: 1.6em;',
		'	font-weight:normal;',
		'	color: blue;',
		'}',
		'.grad4',
		'{'
		'	border-bottom: 2px solid green;',
		'	font-size: 1.4em;',
		'	color: green;',
		'}',
		'.grad5',
		'{',
		'	border-bottom: 1px solid maroon;',
		'	font-size: 1.2em;',
		'	color: maroon;',
		'}',
		'.grad6',
		'{',
		'	border-bottom: 1px solid purple;',
		'	font-size: 1.2em;',
		'	color: purple;',
		'}',
		'.grad7',
		'{',
		'	border-bottom: 1px dashed yellow;',
		'	font-size: 1.2em;',
		'	color: yellow;',
		'}',
		'.grad8',
		'{',
		'	border-bottom: 1px dashed teal;',
		'	font-weight:bold;',
		'	color: teal;',
		'}',
		'.grad9',
		'{',
		'	border-bottom: 1px dotted olive;',
		'	font-style:oblique;',
		'	color: olive;',
		'}',
		'.grad10',
		'{',
		'	border-bottom: 1px dotted aqua;',
		'	letter-spacing:0.3em;',
		'	color: aqua;',
		'}',
		'#Navi', 
		'{',
		'	position: fixed;',
		'	width: 250px;',
		'	font-size:14px;'
		'}',
		'#Inhalt',
		'{',
		'	margin-left: 300px;',
		'}',
		'#Kopf',
		'{',
		'	text-align: center;',
		'}'
		'.grad1, .grad2, .grad3, .grad4, .grad5, .grad6, .grad7, .grad8, .grad9, .grad10 ',
		'{',
		'	text-decoration: none;',
		'}'
		]

	if len(inCSS):
		header.append(tab*' '+'<style type="text/css">\n')
		tab+=2
		for zeile in inCSS:
			header.append(tab*' '+zeile+'\n')
		tab-=2
		header.append(tab*' '+'</style>\n')

	if len(scripte):
		for script in scripte:
			if script:
				header.append(tab*' '+'<script type="text/javascript" src="'+script+'"></script>\n')
	else:
		SCRIPTeinbetten=True

	if SCRIPTeinbetten:
		inScript=[
		'function Sicht(Text)',
		'{',
		"	if (document.getElementById(Text).style.display == 'none')",
		'	{',
		"		document.getElementById(Text).style.display='block';",
		'	}else',
		'	{',
		"		document.getElementById(Text).style.display='none';",
		'	}',
		'}',
		'',
		'function start()',
		'{',
		"	var ausblenden = document.getElementsByClassName('ausblenden');",
		'	var i = ausblenden.length;',
		'	while (i--)',
		'	{',
		"		ausblenden[i].style.display='none';",
		'	}',
		"	var inhalt = document.getElementById('Inhalt');",
		"	inhalt.style.marginLeft= '30px';",
		'}'
		]

	if len(inScript):
		header.append(tab*' '+'<script type="text/javascript">\n')
		tab+=2
		for zeile in inScript:
			header.append(tab*' '+zeile+'\n')
		tab-=2
		header.append(tab*' '+'</script>\n')
	tab=0
	header.append('</head>\n')
	header.append('<body onload="javascript:'+onloadScript+';">\n')
	if privat:
		tab+2
		header.append(tab*' '+'<p style="margin:0; margin-right:0.5em; text-align: right;"><a href="'+LogoutPHP+'">Logout</a></p>\n')
	#Hauptüberschrift
	header.append(tab*' '+'<h1 id="Kopf">'+headline+'</h1>\n')
	
	# Navigationsleiste
	header.append(tab*' '+'<div id="Navi">\n')
	tab+=2
	header.append(tab*' '+'<ul>\n')
	tab+=2
	for link in NaviLinks:
		header.append(tab*' '+'<li>\n')
		tab+=2
		header.append(tab*' '+'<a href="'+link[0]+'">'+link[1]+'</a>\n')
		tab-=2
		header.append(tab*' '+'</li>\n')
	tab-=2
	header.append(tab*' '+'</ul>\n')
	tab-=2
	header.append(tab*' '+'</div><!-- Navi -->\n')

	#Start Inhaltsbereich <- in den wird dann der puffer geschrieben
	header.append(tab*' '+'<div id="Inhalt">\n')
	
	# Hinweis der Angezeigt wird, wenn JavaScript deaktiviert ist
	tab+=2
	header.append(tab*' '+'<p class="ausblenden">\n')
	tab+=2
	header.append(tab*' '+scriptHinweis+'\n')
	tab-=2
	header.append(tab*' '+'</p>\n')
	
	if ToC:
		inhaltsVerzeichnis()

def teste_aufVariable(Zeile): 
	'''
	soll Testen ob die Konfiguratonszeile eine Variablen enthält
	und falls dem so ist den Variablennamen zurückgeben.
	'''
	VariablenName="" # Rückgabevariable
	dollar=Zeile.find('$')
	if dollar > -1:
		dollar2 = Zeile[dollar+1:].find('$')
		VariablenName= Zeile[dollar+1:dollar+1+dollar2]
	return VariablenName

def getVariable(VariablenName):
	'''
	soll den Wert der Variable aus der Konfigurationsdatei im Home-Verzeichnis 
	des Nutzers auslesen und zurückgeben
	'''
	Konfigurationsdatei=pfad.expanduser("~")+'/.tohtml.cfg'
	Wert=""
	conf = open(Konfigurationsdatei)
	for zeile in conf:
		variable_inZeile=zeile.find(VariablenName)
		if variable_inZeile>-1:
			Wert= zeile[variable_inZeile:].split('=')[1].strip()
	conf.close
	return Wert

def set_Wert(VariablenName,Zeile):
	'''
	soll die Variable der Zeile durch Ihren Wert ersetzen
	'''
	start=Zeile.find('$')
	ende=Zeile[start+1:].find('$')+start
	wert=getVariable(VariablenName)
	return Zeile[:start]+wert+Zeile[ende+2:]
	
def formInhalt(Inhalt,Indikator,Tag, Flag,Indikatorlaenge=1,Style=''):

	marke=-1
	while Inhalt.find(Indikator, marke+1)>-1:
		marke= Inhalt.find(Indikator,marke+1)
		if Flag and marke>-1:
			if  Inhalt[marke-1] !=' ':
				Flag= False
				if marke+Indikatorlaenge<len(Inhalt):
					Inhalt=Inhalt[:marke]+'</'+Tag+'>'+Inhalt[marke+Indikatorlaenge:]
				else:
					Inhalt=Inhalt[:marke]+'</'+Tag+'>'
				marke+=Indikatorlaenge+3 # </Indikatorlaenge>

		elif not Flag and marke+Indikatorlaenge<len(Inhalt):
			if Indikatorlaenge>1:
				Flag=True
				Inhalt=Inhalt[:marke]+'<'+Tag + ' ' + Style + '>'+Inhalt[marke+Indikatorlaenge:]
			elif Inhalt[marke+1].isalnum() and (Inhalt[marke-1] ==' ' or marke==0):
				Flag=True
				Inhalt=Inhalt[:marke]+ '<'+ Tag + ' ' + Style +'>'+Inhalt[marke+1:]
	return Inhalt, Flag

def isLink_in(Inhalt):
	'''
	Teste ob die Syntax für einen Link innerhalb der Zeile ist.
	Benötigt: zu prüfenden String
	Gibt zurück: Tulpel mit folgenden Feldern:
		0: True, wenn Syntax eines Links erfüllt ist, sonst False
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
	return link, beginLink, endLink, URL, LinkName

def isWebAdresse(url):
	'''
	Diese Funktion soll prüfen ob ein Linktext 
	die Merkmale einer Webadresse enthällt.
	Wenn ja soll True zurückgegeben werden, sonst False
	Folgende Merkmale sollen eine Webadresse kennzeichen
	* url beginnt mit http:// oder https:// oder www.
	* dannach folgen beliebige Zeichen (mindestens 1)
	* url enthält einen Punkt direkt gefolgt von mindestens zwei Buchstaben
	Regex: ^(http:\/\/|https:\/\/|www\.).+\.[a-zA-Z]{2,}
	'''
	merkmaleErfuellt = False
	if test("^(http:\/\/|https:\/\/|www\.).+\.[a-zA-Z]{2,}",url):
		merkmaleErfuellt = True
	return merkmaleErfuellt

def setLink_in(Text,Link):
	'''
	Diese Funktion soll den Link im Text durch den zugehörigen HTML-Code
	ersetzen.
	
	Sie erwartet einmal den komletten Text 
	und einen Tulpel aus 
		0: True, wenn Syntax eines Links erfüllt ist, sonst False
		1: Index an dem der URL-Text im übergebnen String beginnt
		2: Index an dem der Linkname endet
		3: URL des Links
		4: LinkText
		
	Zurückgegeben wird der Text in dem der Link durch den eingebetteten 
	HTML-Code ersetzt ist.
	
	Folgende Globale Variablen werden genutzt:
	IDs: Liste aller Sprungmarken
	'''
	neuerText=''
	url=Link[3]
	if isWebAdresse(url):
		neuerText = Text[:Link[1]-2]\
		+ '<a href="'\
		+ url\
		+ '">'\
		+ Link[4]\
		+ '</a>'\
		+ Text[Link[2]+2:]
		
	else:
		id=zusammenfassen(url.split())
		id+='_a'
		neuerText = Text[:Link[1]-2]\
		+ '<a href="#'\
		+ id\
		+ '">'\
		+ Link[4]\
		+ '</a>'\
		+ Text[Link[2]+2:]
	return neuerText
	
def setAnker_in(Zeile, Anker):
	'''
	Diese Funktion soll einen Anker setzen, auf den
	verlinkt werden kann.
	Ihr wird die Zeile und ein Tulpel namens Anker übergeben.
	Anker enthält folgende Felder:
		0: True, wenn Syntax eines Ankers erfüllt ist, sonst False
		1: Index an dem der Anker-Text im übergebenen String beginnt
		2: Index an dem der Anker-Text im übergebenen String endet
		3: Text des Ankers
	'''
	id=zusammenfassen(Anker[3].split())
	# <<Text>> => <span id="text">Text</span>
	neuerText = Zeile[:Anker[1]-8]\
		+ '<span id="'\
		+ id\
		+ '_a">'\
		+ Anker[3]\
		+ '</span>'\
		+ Zeile[Anker[2]+8:]
	return  neuerText

def isAnker_in(Inhalt):
	'''
	Teste ob die Syntax für einen Anker innerhalb der Zeile ist.
	Benötigt: zu prüfenden String
	Gibt zurück: Tulpel mit folgenden Feldern:
		0: True, wenn Syntax eines Ankers erfüllt ist, sonst False
		1: Index an dem der Anker-Text im übergebenen String beginnt
		2: Index an dem der Anker-Text im übergebenen String endet
		3: Text des Ankers
	
	Syntax eines Ankers:
	Ein Anker beginnt mit "<<" und endet mit ">>"
	Achtung die 
	"<<" werden durch &lt;&lt; und die
	">>" werden durch &gt;&gt;
	ersetzt.
	Zwischen den beiden Marken befindet sich der Ankertext
	'''
	
	anker= False
	endAnker=-1
	txtAnker=''
	beginAnker =Inhalt.find('&lt;&lt;')
	if beginAnker >-1:
		beginAnker+=8
		endAnker = Inhalt[beginAnker:].find('&gt;&gt;')
		if endAnker > -1:
			#es ist ein Anker
			endAnker+=beginAnker
			txtAnker= Inhalt[beginAnker:endAnker]
			anker= True
	return anker, beginAnker, endAnker, txtAnker

def formatiere(Inhalt):
	'''
	Der in Zeile übergebene Text soll nach Formatierungszeichen durchsucht werden.
	Diese sollen durch den entsprechnden HTML-Format-Code ersetzt werden.
	Die so veränderte Zeile soll zurück gegeben werden
	'''
	global fett, stark, icode, kursiv
	global hervorgehoben, unterstrichen, durchgestrichen
	global code

	# *Text* => Text fett => <b>Text</b>
	Inhalt,fett=formInhalt(Inhalt,'*','b',fett)
	# !Text! => Text stark => <strong>Text</strong>
	Inhalt,stark=formInhalt(Inhalt,'!','strong',stark)
	# =Code= => Codeformat=> <code>Code</code>
	Inhalt,icode=formInhalt(Inhalt,'=','code',icode)
	# _Text_ => Text unterstrichen => <u>Text</u>
	Inhalt,unterstrichen=formInhalt(Inhalt,'_','span',unterstrichen, Style='style="text-decoration: underline;"')
	# +Text+ => Text durchgestrichen => <s>Text</s>
	Inhalt,durchgestrichen=formInhalt(Inhalt,'+','span',durchgestrichen, Style='style="text-decoration: line-through;"')
	# ~Text~ => Text hervorgehoben => <em>Text</em>
	Inhalt,hervorgehoben=formInhalt(Inhalt,'~','em',hervorgehoben)
	# \\Text\\ => Text italic => <i>Text</i>
	Inhalt,kursiv=formInhalt(Inhalt,2*'\\','i',kursiv,2)
	
	if not code:
		# <<Text>> => <span id='text'>Text</span>
		anker= isAnker_in(Inhalt)
		while anker[0]:
			Inhalt=setAnker_in(Inhalt,anker)
			anker= isAnker_in(Inhalt)

		# [[Link][Linkname]]  => <a href="Link">Linkname</a>
		
		link = isLink_in(Inhalt)
		while link[0]:
			Inhalt=setLink_in(Inhalt,link)
			link = isLink_in(Inhalt)
	
	return Inhalt

def anzahlSterne(strZeile):
	''' Diese Funktion soll zählen wieviel Sternsymbole am Anfang
	der Zeile sind und diese Menge zurückgeben.
	Dazu muss der Funktion die zu Untersuchende Zeile übergeben werden.
	'''
	return strZeile.split(' ')[0].count('*')

def alphaNum(Wort):
	'''
	Diese Funktion löscht alle Sonderzeichen aus einem übergebenen Wort
	'''
	filter=''
	for Buchstabe in Wort:
		if Buchstabe.isalnum():
			filter+=Buchstabe
	return filter
	
def zusammenfassen(woerter):
	'''
	Diese Funktion fasst alle Wörter der Liste woerter zu einem
	Text ohne Leerzeichen zusammen, bei dem jedes neue Wort mit einem 
	Großbuchstaben beginnt.
	'''
	id=''
	for wort in woerter:
		wort=alphaNum(wort)
		id+=wort.capitalize()
	return id

def idZahlNachHinten(id):
	'''
	Diese Funktion soll falls ein übergebener String mit einer Zahl beginnt,
	diese an das Ende des Strings stellen.
	'''
	newID=id
	zaehler=0
	while newID[0].isdigit():
		newID=newID[1:]+newID[0]
		zaehler+=1
		if zaehler > len(id):
			'''
			Verhindern einer Endloss-Schleife, 
			wenn die ID nur aus Zahlen besteht
			'''
			newID = 'A' + newID[:]
			
	return newID

def mkID(Zeile):
	'''Diese Funktion entfernt alle Sonderzeichen und
	gibt den Text ohne Leerzeichen zurück,
	wobei jedes neue Wort mit Großbuchstaben beginnt
	Der Funktion muss eine Überschrift übergeben werden,
	die zur ID für den auszublendenden Text umgewandelt werden soll
	'''
	
	ueberschrift=Zeile[ len( Zeile.split(' ')[0] )+1 : -1 ]
	woerter= ueberschrift.split(' ')
	id=zusammenfassen(woerter)
	if(id==""):
		id="Sonderzeichen_ersetzt"
	idZaehler=0
	tmpId=id
	while id in IDs:
		idZaehler+=1
		id=tmpId+str(idZaehler)
	id=idZahlNachHinten(id)
	IDs.append(id)
	return id

def testUeberschrift(Zeile):
	'''
	Diese Funktion soll Testen, ob es sich um eine Überschrift handelt,
	und den Text der Überschrift zurückgeben.
	Eine Überschrift beginnt dabei immer mit Sternen gefolgt von
	einem Leerzeichen
	'''
	global DokumentUeberschrift

	strTest= Zeile.split(' ')[0]
	ueberschrift=0
	if anzahlSterne(strTest) == len(strTest) and len(strTest)>0:
		#es handelt sich um eine Überschrift
		ueberschrift = maskiereSonderzeichen(Zeile[len(strTest)+1:-1])
		#Sonderbehandlung Dokumentenüberschrift
		if not DokumentUeberschrift:
			DokumentUeberschrift=True
			dokname=pfad.split('/')[-1]
			puffer.append(tab*' '+'<h1>'+dokname+'</h1>\n')

	return ueberschrift

def isKommentar(Zeile):
	'''
	Hier soll geprüft werden, ob es sich um einen
	Kommentar handelt
	'''
	comment=False
	Raute = Zeile.find('#')
	if Raute > -1:
		if Zeile[:Raute] == Raute*' ' and Zeile.find('#+') != Raute:
			comment=True
	return comment

def kommentarUeberschrift(Zeile):
	'''
	Hier soll geprüft werden, ob es sich um eine Überschrift handelt,
	die als Kommentar zu behandeln ist
	'''
	comment=False
	if testUeberschrift(Zeile):
		if Zeile.split(' ')[1] == 'COMMENT':
			comment=True
	return comment

def testListe(Zeile):
	'''
	Diese Funktion soll Testen, ob es sich um eine Liste handelt,
	und den Text des Listenpunktes,
	die Menge vorhergehnder Leerzeichen
	und das Listenzeichen zurückgeben.
	Eine Liste beginnt dabei entweder mit
	einem Minuszeichen, einem Pluszeichen, oder auch mit Zahlen gefolgt von
	einem Leerzeichen. Dabei können auch Leerzeichen davor vorhanden sein.
	Ist ein Listenpunkt weiter eingerückt als der vorhergehnde ist es ein Unterpunkt.
	'''
	Tiefe =-1
	Listenzeichen = ''
	Minus= Zeile.find('- ')
	Plus = Zeile.find('+ ')
	Stern= Zeile.find('* ')
	Punkt= Zeile.find('. ')
	Klammer= Zeile.find(') ')
	Listenpunkt=''
	if Zeile[:Minus] == Minus*' ':
		#Erstes Zeichen der Zeile ist ein Minus
		Listenpunkt=Zeile[Minus+2:-1]
		Listenzeichen ='-'
		Tiefe=Minus
	elif Zeile[:Plus] == Plus*' ':
		#Erstes Zeichen der Zeile ist ein Plus
		Listenpunkt=Zeile[Plus+2:-1]
		Listenzeichen='+'
		Tiefe=Plus
	elif Zeile[:Stern] == Stern*' ' and Stern>0:
		#Erstes Zeichen der Zeile ist ein Stern
		Listenpunkt=Zeile[Stern+2:-1]
		Listenzeichen='*'
		Tiefe = Stern
	elif Punkt or Klammer:
		#prüfen ob Ziffern davor die ersten Zeichen der Zeile sind
		ZifferPkt=Zeile[:Punkt].strip()
		ZifferKl=Zeile[:Klammer].strip()
		if ZifferPkt.isdigit():
			Listenpunkt=Zeile[Punkt+2:-1]
			Listenzeichenxb=ZifferPkt+'.'
			Tiefe=Punkt-len(ZifferPkt)
		elif ZifferKl.isdigit():
			Listenpunkt=Zeile[Klammer+2:-1]
			Listenzeichen=ZifferKl+')'
			Tiefe=Klammer-len(ZifferKl)
	return Tiefe, Listenzeichen, maskiereSonderzeichen(Listenpunkt)

def FortsetzungListe(orgZeile,Vorzeile):
	'''
	Diese Funktion soll die Fortsetzung eines Listenpunktes
	anhand der Einrücktiefe indentifizieren.
	Dazu wird der Funktion die aktuelle Zeile und die Vorzeile 
	übergeben. 
	Das Flag isListenPunkt zeigt an, ob es sich um einen 
	Listen-Block handelt.
	Ist die Einrücktiefe identisch, ist es eine Fortsetzung
	und es wird True zurück gegeben, andernfalls False
	'''
	TeilEinerListe=False
	if isListenPunkt:
		if len(orgZeile.strip())!=0: # keine Leerzeile
			ersterBuchstabe=orgZeile.strip()[0]
			einrueckTiefe= orgZeile.index(ersterBuchstabe)
			
			Listenpunkt= testListe(Vorzeile)
			if Listenpunkt[0]>-1:
				einrueckTiefeVorzeile = Vorzeile.index(Listenpunkt[1])+2
			else:
				ersterBuchstabe=Vorzeile.strip()[0]
				einrueckTiefeVorzeile= Vorzeile.index(ersterBuchstabe)
				
			if einrueckTiefe >= einrueckTiefeVorzeile:
				TeilEinerListe=True # Fortsetzung
			#~ if einrueckTiefe == einrueckTiefeVorzeile+3:
				#~ TeilEinerListe=True # Fortsetzung Definitionsliste
				
	return TeilEinerListe

def liTag(listenKennzeichen, listenText):
	'''
	Diese Funktion soll den entsprechenden Tag der Liste zurückgeben.
	Mögliche Werte sind 'ul','ol' und 'dl'
	Der Funktion ist das Listenkennzeichen und
	um für die Def-Liste nach doppelten Doppelpunkten zu suchen
	der Listentext zu übergeben.
	'''
	Tag=''
	if listenKennzeichen in ['-','+','*']:
		if '::' in listenText:
			# Definitionsliste
			Tag='dl'
		else:
			# normale Liste
			Tag='ul'
	else:
		# orderd List
		Tag='ol'
	return Tag

def maskiereSonderzeichen(inhalt):
	'''
	Hier soll dafür gesorgt werden, dass im HTML-Code, deutsche
	Sonderzeichen entsprechend maskiert werden, um eine
	saubere Darstellung zu erhalten.
	in : Text der von Sonderzeichen gesäubert werden soll
	out: Text in dem die Sonderzeichen ersetzt sind.
	
	Änderung vom 26.02.2014:
	mit dem neuen charset utf-8 im header ist die Maskierung der
	deutschen Umlaute nicht mehr notwendig.
	Für eine bessere Lesbarkeit des html-Quellcode, werde ich diese
	jetzt hier wieder abschalten.
	
	ListeSonderzeichen=[
	('ä','&auml;'),
	('ö','&ouml;'),
	('ü','&uuml;'),
	('Ä','&Auml;'),
	('Ö','&Ouml;'),
	('Ü','&Uuml;'),
	('ß','&szlig;'),
	'''
	'''
	Es ist wichtig, dass dass &-Zeichen zuerst ersetzt wird, damit
	ein später durch die Ersetzung gesetztes & nicht erneut ersetzt wird!!!
	'''
	ListeSonderzeichen=[
	('&','&amp;'),
	('>','&gt;'),
	('<','&lt;')]

	for Sonderzeichen in ListeSonderzeichen:
		inhalt=inhalt.replace(Sonderzeichen[0],Sonderzeichen[1])
	if not code:
		if firstUeberschrift:
			inhalt=formatiere(inhalt)
		else:
			inhalt=inhalt.strip('*')
	return inhalt

def istTabellenZeile(Zeile):
	'''
	Diese Funktion soll eine Zeile darauf prüfen,
	ob das Format einer Tabelle enthalten ist.
	in : Zeile die zu prüfen ist
	out:
	0 ->keine Tabelle
	1 ->Datenzeile
	2 ->Trennzeile
	'''

	DATENZEILE=1
	TRENNZEILE=2
	istTabelle = 0
	Strich = Zeile.find('| ')
	if Strich>-1:
		if Zeile[:Strich] == Strich*' ':
			#Erstes Zeichen der Zeile ist ein Strich
			if Zeile[Strich:].count(' |') > 1:
				istTabelle = DATENZEILE
	Strich = Zeile.find('|-')
	Plus = Zeile[Strich:].find('-+-')
	EndStrich = Zeile[Plus:].find('-|')
	if Strich>-1:
		if Zeile[:Strich] == Strich*' ':
			if Plus and EndStrich:
				istTabelle = TRENNZEILE
	return istTabelle

def setzeTabellenZeile(pos,zellen):
	'''
	Diese Funktion soll eine Tabellenzeile in den Puffer schreiben.
	in:
	 pos = 'th' -> Spaltenüberschrift oder 'td' --> Zellendaten
	 zellen = Liste der Zelleninhalte
	'''

	global tab
	puffer.append(tab*' '+'<tr>\n') # neue Zeile öffnen
	tab+=2
	for zelle in zellen:
		puffer.append(tab*' '+'<'+pos+'>\n')
		tab+=2
		puffer.append(tab*' '+maskiereSonderzeichen(zelle)+'\n')
		tab-=2
		puffer.append(tab*' '+'</'+pos+'>\n')
	tab-=2
	puffer.append(tab*' '+'</tr>\n') # neue Zeile öffnen

def inlineSchliessen():
	global fett, stark, icode, kursiv, unterstrichen, durchgestrichen
	global hervorgehoben, fLinkadresse, fLinkname

	#Formatierung aus
	if fett:
		fett=False
		puffer.append('</b>\n')

def schliessen(was):
	'''
	Diese Funktion soll falls nötig eine Struktur schließen
	'''
	global tab, absatz, isListenPunkt

	if was & TABELLE:
		if istTabellenZeile(Vorzeile):
			#Tabelle schließen
			tab-=2
			puffer.append(tab*' '+'</table>\n')
			inlineSchliessen()

	if was & LISTE:
		# kompette Listen-Struktur schließen
		while Listenpunkte[-1][0] > -1:
			vorgaenger=Listenpunkte.pop()
			EndeListenPunkt = liEnder.pop()
			tab-=2
			puffer.append(tab*' ' + EndeListenPunkt)
			tab-=2
			puffer.append(tab*' '+'</'+ liTag(vorgaenger[1], vorgaenger[2])+'>'+'\n')
			inlineSchliessen()
		isListenPunkt=False
		
	if was & ABSATZ:
		#Absatz schließen, wenn offen
		if absatz:
			absatz=False
			tab-=2
			puffer.append(tab*' '+'</p>\n')
			inlineSchliessen()

def isCode(Zeile):
	'''
	Diese Funktion soll die aktuelle Zeile prüfen, ob hier
	ein Codeblock beginnt oder endet.
	Bei Beginn soll die globale Variable code auf True gesetzt werden
	und auch True zurückgegeben werden
	wenn der Code endet, soll die globale Variable code auf False gesetzt werden
	aber True zurückgegeben werden.
	außerdem soll der Tag gesetzt werden
	'''
	global code

	codeZeile=False
	if Zeile.find('#+BEGIN_SRC')==0:
		#Ein Code-Block beginnt
		code=True
		codeZeile=True
		schliessen(LISTE+TABELLE+ABSATZ)
		puffer.append('<pre>\n')
	elif Zeile.find('#+END_SRC')==0:
		#Ein Code-Block endet
		code=False
		codeZeile=True
		puffer.append('</pre>\n')
	elif code:
		codeZeile=True
		puffer.append(maskiereSonderzeichen(Zeile)) 
	return codeZeile

def isSetting(Zeile,einstellen=True):
	'''
	Diese Funktion soll die eingelesene Zeile auf Informationen prüfen,
	die für die Erstellung der HTML-Seite notwendig sind:
	listeCSS _______: Liste mit den Pfaden aller zugehörigen CSS-Dateien
	inCSS __________: Liste mit den Zeilen von zu intigrierenden CSS
	scripte ________: Liste mit den Pfadnamen aller zugehörigen Scripte
	inScript _______: Liste mit den Zeilen von zu intigrierenden Javascript
	onloadScript ___: Funktionsname, der beim Laden der HTML-Datei automatisch aufgerufen werden soll
	scriptHinweis __: Hinweis der Angezeigt wird, wenn JavaScript deaktiviert ist
	headline _______: Überschrift des Dokuments
	NaviLinks ______: Links der Navigationsleiste in Tupel Linkadresse im Feld 0, Linkname im Feld 1
	Zieldatei ______: Name zum Speichern der erstellten Datei
	Zielpfad _______: Pfad zum Speichern der erstellten Datei
	ToC ____________: Tiefe des Inhaltsverzeichnis (0 zum Ausschalten; Voreinstellung ist 2)
	LoginPHP _______: Dateipfad der Login-Datei
	LogoutPHP ______: Dateipfad der Logout-Datei
	privat _________: True, wenn die Seite nur mit Login sichtbar sein soll
	'''
	global listeCSS, inCSS , scripte, inScript, onloadScript
	global scriptHinweis, headline, NaviLinks, docTitel, Zieldatei, Zielpfad, ToC
	global LoginPHP,LogoutPHP, privat

	setting=True
	
	# ersetze Variablen in den Settings
	if einstellen:
		if Zeile.find('#+')>-1:
			if Zeile.find(':')>-1\
			and Zeile.count('$')>1:
				while len(teste_aufVariable(Zeile)):
					Zeile=set_Wert(teste_aufVariable(Zeile),Zeile)
	
	# reagiere auf Setting		
	if Zeile.find('#+PFAD_CSS')>-1:
		if einstellen:
			css=Zeile.split(':')[1].strip()
			if css[-3:] != 'css':
				css+='css'
			listeCSS.append(css)
	elif Zeile.find('#+IN_CSS')>-1:
		if einstellen:
			inCSS.append(Zeile.split(':')[1].strip())
	elif Zeile.find('#+PFAD_SCRIPT')>-1:
		if einstellen:
			sc=Zeile.split(':')[1].strip()
			if sc[-3:] != '.js':
				sc+='.js'
			scripte.append(sc)
	elif Zeile.find('#+IN_SCRIPT')>-1:
		if einstellen:
			inScript.append(Zeile.split(':')[1].strip())
	elif Zeile.find('#+ONLOAD_SCRIPT')>-1:
		if einstellen:
			onloadScript=Zeile.split(':')[1].strip()
			if onloadScript.find('(')==-1:
				onloadScript+='()'
	elif Zeile.find('#+HINWEIS_SCRIPT')>-1:
		if einstellen:
			scriptHinweis=Zeile.split(':')[1].strip()
	elif Zeile.find('#+DOC_TITEL')>-1:
		if einstellen:
			docTitel=Zeile.split(':')[1].strip()
	elif Zeile.find('#+DOC_HEADLINE')>-1:
		if einstellen:
			headline=Zeile.split(':')[1].strip()
	elif Zeile.find('#+NAVI_LINK')>-1:
		if einstellen:
			link=Zeile.split(':')
			if len(link)>2:
				NaviLinks.append((link[1].strip(),link[2].strip().strip('\n')))
	elif Zeile.find('#+ZIEL_DATEI')>-1:
		if einstellen:
			Zieldatei=Zeile.split(':')[1].strip()
	elif Zeile.find('#+ZIEL_PFAD')>-1:
		if einstellen:
			Zielpfad=Zeile.split(':')[1].strip()
			if Zielpfad[-1:] !='/':
				Zielpfad+='/'	
	elif Zeile.find('#+TOC')>-1:
		if einstellen:
			ToC=int(Zeile.split(':')[1].strip())
	elif Zeile.find('#+LOGIN')>-1:
		if einstellen:
			LoginPHP=Zeile.split(':')[1].strip()
			LogoutPHP=LoginPHP[:-9]+'logout.php'
			privat=True
	elif Zeile.find('#+SCRIPT_EINBETTEN')>-1:
		if einstellen:
			SCRIPTeinbetten=True
	elif Zeile.find('#+CSS_EINBETTEN')>-1:
		if einstellen:
			CSSeinbetten=True
	else:
		setting=False
	return setting

def mkComment(Zeile):
	'''
	Diese Funktion soll den einen Kommentar zusammenstellen.
	Somit sind Fehler in Kommentaren immer über diese Funktion
	zu beheben.
	'''
	#Minuszeichen umformen
	Minus=Zeile.find('-')
	while Minus>-1:
		Zeile=Zeile[:Minus]+'*'+Zeile[Minus+1:]
		Minus=Zeile.find('-')
	
	# html-Auszeichnung
	start=Zeile[:-1].strip().find('-->')
	if start !=-1:
		comment=Zeile[:start]+Zeile[start+3:-1]
		comment=comment.strip()
	else:
		comment=Zeile
	ende= comment.find('<--')
	if ende != -1:
		comment=comment[:ende]+comment[ende+3:]
	comment='<!--'+comment +' -->'
	return comment
	
def textAbsatz(Zeile):
	# Textabsätze
	global absatz, tab
	schliessen(LISTE+TABELLE)
	if absatz:
		puffer.append(tab*' '+maskiereSonderzeichen(Zeile))
	else:
		puffer.append(tab*' '+'<p>\n')
		tab+=2
		puffer.append(tab*' '+maskiereSonderzeichen(Zeile))
		absatz=True
	 
def inhaltsVerzeichnis():
	'''
	Diese Funktion soll ein Inhaltsverzeichnis an den 
	Anfang des Inhaltsbereiches setzen, welches ausgeblendet wird,
	wenn JavaScript aktiviert ist. 
	Somit ist gewährlistet, dass die Seite auch ohne JavaScript,
	einfacher zu navigieren ist.
	Im Überschriftenbereich des Auslesebereichs wird 
	mit Ueberschriften.append((Grad, ueberschrift, divID)) eine Liste
	aller Überschriften in der Variable Ueberschriften erstellt.
	Diese gilt es jetz bis zu einem gewissem Grad in der Tiefe
	in eine Linkliste umzuwandeln.
	Diese wird über header.append im oberen Bereich eingehängt.
	'''	
	global tab
	
	header.append(tab*' '+'<div id="content" class="ausblenden">\n')
	vorGrad=0
	menuPunkte=[]
	for thema in Ueberschriften:
		grad, lText, lID = thema
		if grad <= ToC:
			if grad > vorGrad:
				#neuer Unterpukt
				tab+=2
				header.append(tab*' '+'<ul>\n')
				tab+=2
				vorGrad=grad
				
			elif grad < vorGrad:
				# neuer übergeordneter Punkt
				# alle Menüpunkte bis zum selben Grad schließen
				mPunkt,vorGrad=menuPunkte.pop()
				header.append(tab*' '+'</li> <!-- ' + mPunkt + ' -->\n') 
				while vorGrad > grad:
					tab-=2
					header.append(tab*' '+'</ul>\n')
					tab-=2
					mPunkt,vorGrad=menuPunkte.pop()
					header.append(tab*' '+'</li> <!-- ' + mPunkt + ' -->\n') 
			else:
				# neuer Listenpunkt gleichen Grades
				# alten Menüpunkt schließen
				mPunkt,vorGrad=menuPunkte.pop()
				header.append(tab*' '+'</li> <!-- ' + mPunkt + ' -->\n') 
				
			menuPunkte.append((lText,vorGrad))
			header.append(tab*' '+ '<li> <!-- '+ lText + ' -->\n')
			tab+=2
			header.append(tab*' '+ '<a href="#'+lID+'_a">'+ lText +'</a>\n')
			tab-=2
	#Alle Listenpunkte schließen:
	# jeder Listenpunkt wurde in die Liste menuPunkte hinzugefügt
	# geschlossene werden jeweils der Liste entnommen
	# ggf. kann ein Schließen so lange erfolgen, wie es Menüpunkte gibt
	while len(menuPunkte):
		mPunkt,vorGrad=menuPunkte.pop()
		header.append(tab*' '+'</li> <!-- '+ mPunkt + ' -->\n') 
		if vorGrad > 0:
			tab-=2
			header.append(tab*' '+'</ul>\n')
			tab-=2
	
	header.append(tab*' '+'</div> <!-- content -->\n')
			
def hilfe():
	'''
	Diese Funktion soll einfach die Beschreibung der Bedienung
	dieses Programms in der Konsole ausgeben.
	'''
	na='<ENTER>: weiter  |  <q>+<ENTER>: beenden'
	Ausgabe=[
	'Beschreibung:',
	'Dies Programm erstellt aus einer Klartext-Datei,',
	'wie sie mit dem emacs org-mode geschrieben werden kann,',
	'eine HTML-Datei.',
	'Die erstellte Datei hat dann die Fähigkeit,',
	'mit Hilfe von Javascript den Inhalt durch Anklicken',
	'der Überschriften auf- und zuzublättern.',
	na,
	'1. Bedienung:',
	'Die Datei sollte die Strukturanweisungen',
	'des emacs-org-mode enthalten:',
	'Überschriften werden dabei mit *-Symbolen,',
	'Listen durch voranstellen von Plus- oder Minus-Zeichen',
	'und Tabellen durch mit Pips getrennte Spalten gekennzeichnet.',
	'Links werden als [[Linkadresse][Linkname]] eingegeben.',
	'Einem einzeiligen Kommentar wird # vorangestellt,',
	'Eine Überschrift mit "* COMMENT" behandelt alles,',
	'was folgt als Kommentar.',
	na,
	'2. Formatierungen:',
	'2.1. Textstiele können wie folgt eingestellt werden:',
	'*Text* => Text fett => <b>Text</b>',
	'!Text! => Text stark => <strong>Text</strong>',
	'=Code= => Codeformat=> <code>Code</code>',
	'_Text_ => Text unterstrichen => <u>Text</u>',
	'+Text+ => Text durchgestrichen => <s>Text</s>',
	'~Text~ => Text hervorgehoben => <em>Text</em>',
	'\\\Text\\\ => Text italic => <i>Text</i>',
	'Sie orientieren sich weitgehend an der Eingabe im emacs.',
	'Da die kursive Schrift im emacs allerdings durch die',
	'Einbettung zwischen je einem Slash gekennzeichnet wird,',
	'die gerade bei HTML-Seiten besondere Bedeutung haben,',
	'habe ich die kursive Schrift durch Einbetten in',
	'je 2 Backslashes ermöglicht.',
	na,
	'2.2. Codeblöcke:',
	'Codeblöcken werden zwischen den Zeilen',
	'#+BEGIN_SR und #+END_SRC eingebettet.',
	'Alles, was zwischen diesen beiden Zeilen steht,',
	'wird in ein pre-Element eingebettet.',
	'Somit wird der Code genau in der gleichen',
	'Formatierung ausgegeben, in der er',
	'im Dokument erfasst wurde.',
	na,
	'2.3 Dokumentüberschrift:',
	'Eine Dokumentüberschrift kann erfasst werden,',
	'indem vor die erste Überschrift ein normaler,',
	'gern auch mit Sternchensymbol fett gemachter Text steht.',
	'Die Sternsymbole werden später', 
	'nicht in die html-Datei übernommen.',
	na,
	'3. Einstellungen:',
	'Die Einstellungen für die Erstellung der Webseite',
	'werden direkt in der Textdatei vorgenommen.',
	'Dazu werden der Einstellung Schlüsselworte',
	'jeweils gefolgt von einem Doppelpunkt ":" vorangestellt.',
	'Es können durch weitere Zeilen',
	'mit entsprechenden vorangestelltem Key,',
	'weitere Zeilen oder Dateien an das Programm',
	'zum Einbetten übergeben werden.',
	na,
	'3.1. Einbetten von Links:',
	'Links werden durch Linkadresse : Linkname',
	'hinter #+NAVI_LINK: angegeben.',
	'Dabei ist zu beachten, dass die Pfade relativ',
	'zum Pfad der Zieldatei angegeben werden müssen.',
	'Es folgt eine Liste der verwendbaren Schlüsselworte:',
	na,
	'3.2. Einstellungs-Schlüsselworte:',
	'#+PFAD_CSS _____: Pfad einer einzubettenden CSS-Datei',
	'#+IN_CSS _______: Zeile von zu integrierendem CSS',
	'#+PFAD_SCRIPT __: Pfad einer einzubettenden Java-Script-Datei',
	'#+IN_SCRIPT ____: Zeile von zu inegrierendem Java-Script-Code',
	'#+ONLOAD_SCRIPT : Funktion, die beim Laden der Seite aufgerufen wird',
	'#+HINWEIS_SCRIPT: Hinweis, falls JavaScript deaktiviert ist',
	'#+DOC_TITEL ____: Titel der Webseite',
	'#+DOC_HEADLINE _: Überschrift der Webseite',
	'#+NAVI_LINK ____: Link für die Navigationsleiste',
	'#+ZIEL_DATEI ___: Name der zu erstellenden Datei',
	'#+ZIEL_PFAD ____: Pfad der zu erstellenden Datei',
	'#+TOC __________: Tiefe des Inhaltsverzeichnis',
	'#+LOGIN ________: Wenn privat, wo ist die Login-Datei',
	na, 
	'3.3. Standardverhalten:',
	'Wird nichts angegeben, so wird der Dateinamen, durch die Überschrift gesetzt.', 
	'Das gilt auch für DOC_TITEL und DOC_HEADLINE.',
	'ONLOAD_SCRIPT und HINWEIS_SCRIPT sind sinnvoll vorbelegt.',
	'Für TOC ist die Voreinstellung 2,',
	'zum Ausschlaten setzt mann es auf 0.'
	'Somit sollten zum einbetten in eine Dateistruktur: ',
	'* ZIEL_PFAD, ',
	'* NAVI_LINK, ',
	'* PFAD_SCRIPT und ',
	'* PFAD_CSS ',
	'gesetzt werden.',
	'Alles andere ist sinnvoll vorbelgt,',
	'kann aber nach Bedarf mit eignen Werten übersteuert werden.',
	'Ohne jedliche Einstellung wird die Datei im Ordner',
	'der Quelldatei mit eingebettetem CSS und Javascript angelegt,',
	'so dass auch hier eine funktionierende Seite entsteht.',
	na,
	'3.4. Variablen:',
	'Um in den Einstellungen flexibel auf den Einsatz der Datei',
	'auf unterschiedlichen Systemen mit entsprechend unterschiedlicher',
	'Ordnerstruktur reagieren zu können, kann man Variabeln benutzen.',
	'Variabeln definiert man in der Datei ~/.tohtml.cfg indem',
	'man Variabelnnamen=Variabelnwert in jeweils eine Zeile schreibt.',
	'Eine so für das System definierte Variable, kann dann in den Einstellungen',
	'genutzt werden indem man sie zwischen zwei $-Zeichen einbettet,',
	'also $Variabelnnamen$. Dies wird dann bei der Übername der Einstellungen',
	'durch das Script durch den Variabelnwert ersetzt.',
	'Um auf einem anderen System mit der Datei arbeiten zu können,',
	'muss dort die verwendete Variabel mit den für dieses System',
	'geltenden Anpassungen in der Datei ~/.tohtml.cfg definiert werden.',
	na,
	'4. Dem Programm muss beim Aufruf die umzuwandelnde',
	'Datei als Parameter übergeben werden.',
	'Lässt man die Angabe der Quelldatei weg,',
	'wird dieser Hilfetext angezeigt.',
	'Es kann auch ein Ordner als Parameter übergeben werden.',
	'in dem Fall werden alle Dateien, die auf .org enden',
	'innerhalb des Ordners abgearbeitet.']

	i=0
	for zeile in Ausgabe:
		if (zeile != na):
			print(zeile)
		else:
			a=input('\n'+na+'\n')
			if a=='q':
				sys.exit() # Programmende
	a=input('Das Programm wird nach Enter beendet. Beim nächsten Start bitte die Quelldatei übergeben!')
	sys.exit() # Programmende

#Quellen definieren
Quelle =''  # den Argumenten die Quelle entnehmen
Quellen=[] # Liste aller Quelldateien
if len(sys.argv)>1:
	if sys.argv[1]=='-p':
		privat=True
		if len(sys.argv)>2:
			Quelle=sys.argv[2:]
		else:
			hilfe()
	else:
		Quelle=sys.argv[1:]
else:
	hilfe()
for dat in Quelle:
	if pfad.isdir(dat):
		#Quelle ist ein Verzeichnis
		Dateien=ls(dat)
		VQuellen=Dateien[:]
		for Datei in Dateien:
			if Datei[-4:] != '.org':
				VQuellen.remove(Datei)
		dat=' '+dat
		VQuellen='{1}{0}'.format(dat.join(VQuellen),dat).split()
		for VQuelle in VQuellen:
			Quellen.append(VQuelle)
	else:
		Quellen.append(dat)
		
for Quelle in Quellen:
	# Variablen
	divID ='' # ID des auszublendenden Elements / gebildt aus der Überschrift ohne Leerzeichen
	puffer= [] # in diesen Puffer sollen zunächst die Zeilen für die html-Datei geschrieben werden
	header= [] # Puffer für den Kopf der Webseite
	pZeile= 0 # aktuelle Zeile in die als nächstes geschrieben wird
	tab=2 # Einrücktiefe zur besseren Übersicht in der HTML-Datei
	Vorzeile='' # enthälte die zuletzt bearbeitete Zeile der Orginal-Datei
	docTitel='' # soll den Titel des HTML-Dokuments aufnehmen
	listeCSS=[] # soll die Pfade zu den CSS-Dateien aufnehmen
	LoginPHP='login.php' # Pfad der Logindatei
	LogoutPHP='logout.php'# Pfad der Logoutdatei
	CSSeinbetten=False # wenn True wird die inCSS mit einer Standardbelegung versehen
	SCRIPTeinbetten=False # wenn True wird inSCRIPT mit einer Standardbelegung versehen.
	inCSS=[] # Liste mit den Zeilen von zu intigrierenden CSS
	scripte=[] # Liste mit den Pfadnamen aller zugehörigen Scripte
	inScript=[] # Liste mit den Zeilen von zu intigrierenden Javascript
	onloadScript='start()' #Funktionsname, der beim Laden der HTML-Datei automatisch aufgerufen werden soll
	headline='' # Überschrift des Dokuments
	NaviLinks=[] # Links der Navigationsleiste in Tupel Linkadresse im Feld 0, Linkname im Feld 1
	scriptHinweis='Die Übersichtlichkeit der Seite wird durch Javascript erhöht.'
	scriptHinweis+=' Ist dies aktiviert, werden die Texte unter den Überschriften durch'
	scriptHinweis+=' Anklicken der Überschriften ein- und ausgeblendet.'# Hinweis der Angezeigt wird, wenn JavaScript deaktiviert ist
	Zieldatei='out.html' # Dateiname für die Zieldatei
	Zielpfad='' #Pfad zum Ordner der Zieldatei
	IDs=[] # Liste der Überschriften-IDs, um Doppelte IDs zu vermeiden
	Ueberschriften=[] # Liste aller Überschriften, um ein Inhaltsverzeichnis erstellen zu können
	ToC=2 # Gibt an wie tief das Inhaltsverzeichnis verzweigen soll (Grad der Überschrift)


	#Flags
	code=False # Flag, das anzeigt, dass diese Zeile zu einem Codeblock gehört
	absatz=False #Flag, das anzeigt, das diese Zeile zu einem Textabsatz gehört
	DokumentUeberschrift=False # Flag, dass zeigt, ob es bereits eine Überschrift geschrieben wurde
	fett=False # Fettdruck
	stark = False # stark hervorheben
	icode = False # Inlinecode
	kursiv=False # Kursivschrift
	unterstrichen=False # unterstrichener Text
	durchgestrichen=False # durchgestrichener Text
	hervorgehoben=False # hervorgehobener Text
	firstUeberschrift=False # Flag false, solange noch keine Überschrift gesetzt wurde
	KommentarBlock=False #soll true sein, solange ein Kommentarblock bearbeitet wird
	isListenPunkt=False # wird auf True gesetzt, wenn die Zeile ein Listenelement ist
	privat=False # Flag das Anzeigt ob die Ziel-Datei privat ist
	
	#init
	Grad=0
	Sektion=(0,'','')
	Sektionen=[Sektion]
	Listenpunkt=(-1,'','')
	Listenpunkte=[Listenpunkt]
	org = open(Quelle)
	oTeil1_d='''<div id="'''
	oTeil2_d= '''" class="ausblenden" >'''
	kGrad=NOCOMMENT
	liEnder=[] # Der Listenabschluss wird hier zwischengespeichert, um verschachtelte Listen zu ermöglichen
	Zielpfad= pfad.dirname(Quelle)
	if len(Zielpfad) and Zielpfad[-1] !='/':
		Zielpfad+='/'
	
	
	for orgZeile in org:
		ueberschrift=testUeberschrift(orgZeile)
		Listenpunkt=testListe(orgZeile)
		tabelle=istTabellenZeile(orgZeile)
		if isCode(orgZeile):#Code
			# Der Codeblock wird in der Prüffunktion in den Puffer geschrieben
			pass
		elif isKommentar(orgZeile): #einzelne Kommentarzeile
			puffer.append(tab*' '+'<!--'+orgZeile[:-1].strip()+' -->\n')
		elif kommentarUeberschrift(orgZeile):#Kommentarüberschrift
			puffer.append(tab*' '+mkComment(orgZeile)+'\n')
			kGrad=anzahlSterne(orgZeile)
			KommentarBlock=True
			schliessen(LISTE+TABELLE+ABSATZ)
		elif KommentarBlock and not ueberschrift and not isSetting(orgZeile, einstellen=False):
			puffer.append(tab*' '+mkComment(orgZeile)+'\n')
		elif ueberschrift:
			schliessen(TABELLE+LISTE+ABSATZ)
			Grad=anzahlSterne(orgZeile)
			if not(KommentarBlock and Grad>kGrad):
				kGrad=NOCOMMENT
				KommentarBlock=False
				divID=mkID(orgZeile)
				gr='grad'+str(Grad)
				if Grad == Sektionen[-1][0]:
					# Vorgänger-DIV schließen
					vorgaenger= Sektionen.pop()
					kommentar= mkComment(vorgaenger[1])
					puffer.append(tab*' '+'<p class="hoch"><a href="#Kopf">nach oben</a></p>\n')
					tab-=2
					puffer.append(tab*' '+'</div>'+kommentar+'\n')
				elif Grad < Sektionen[-1][0]:
					#alle vorherigen Grade schließen
					while Grad <= Sektionen[-1][0]:
						#Immer die Vorgänger-Sektion aus dem Puffer holen und schließen
						vorgaenger=Sektionen.pop()
						kommentar= mkComment(vorgaenger[1])
						if Grad == Sektionen[-1][0]:
							puffer.append(tab*' '+'<p class="hoch"><a href="#Kopf">nach oben</a></p>\n')
						tab-=2
						puffer.append(tab*' '+'</div>'+kommentar+'\n')
					gr='grad'+str(Grad)
				# neues DIV öffnen
				if firstUeberschrift:
					pass
				puffer.append(tab*' ' + '<p class="H">\n')
				tab+=2
				#~ #a-Überschrift-Element
				puffer.append(\
				tab*' '\
				+'<a class="'\
				+gr\
				+'" id="'\
				+divID+'_a'\
				+'" href="#'\
				+divID+'_a"'\
				+' onclick="javascript:Sicht('\
				+"'"+divID+"');"\
				+'">\n')
				tab+=2
				puffer.append(tab*' '+ueberschrift+'\n')
				tab-=2
				puffer.append(tab*' '+'</a>\n')
				tab-=2
				puffer.append(tab*' '+'</p>\n')
				puffer.append(tab*' '+oTeil1_d+divID+oTeil2_d+'\n')
				puffer.append(tab*' '+mkComment(ueberschrift)+'\n')
				tab+=2 
				#Sektion puffern
				Sektion = (Grad, ueberschrift, divID)
				Sektionen.append(Sektion)
				Ueberschriften.append(Sektion)
				firstUeberschrift=True
		elif Listenpunkt[0]>-1: # Liste
			#Es handelt sich um einen Listeneintrag
			#Listenpunkt[0] enthält die Einrücktiefe
			#Listenpunkt[1] enthält das Listenzeichen
			#Listenpunkt[2] enthält den Text des Listenpunktes
			isListenPunkt=True
			nachAbsatz=absatz
			schliessen(TABELLE+ABSATZ)
			Tag='<'+ liTag(Listenpunkt[1], Listenpunkt[2])+'>'
			vTag='<'+ liTag(Listenpunkte[-1][1], Listenpunkte[-1][2])+'>'
			Unterpunkt = Listenpunkt[0] > Listenpunkte[-1][0]
			if Unterpunkt:
				if \
				not \
				(testUeberschrift(Vorzeile) \
				or nachAbsatz\
				or len(Vorzeile.strip())==0\
				or len(Listenpunkte)):
					tab+=2 
				puffer.append(tab*' '+ Tag +'\n')
				tab+=2
				Listenpunkte.append(Listenpunkt)
			elif Listenpunkt[0]<Listenpunkte[-1][0] or Tag != vTag:
				# Unterpunkte schließen
				while Listenpunkt[0] < Listenpunkte[-1][0]:
					#die Vorgänger-Listenpunkte aus dem Puffer holen und schließen
					vorgaenger=Listenpunkte.pop()
					EndeListenPunkt = liEnder.pop()
					tab-=2
					puffer.append(tab*' ' + EndeListenPunkt)
					tab-=2
					puffer.append(tab*' '+'</'+ liTag(vorgaenger[1], vorgaenger[2])+'>'+'\n')
				# Listenpunkt schließen
				EndeListenPunkt = liEnder.pop()
				tab-=2
				puffer.append(tab*' ' + EndeListenPunkt)
				#eine Ebene aber ggf. unterschiedliche Listenart
				vTag='<'+ liTag(Listenpunkte[-1][1], Listenpunkte[-1][2])+'>'
				if Tag != vTag:
					vorgaenger=Listenpunkte.pop()
					#vorgaenger schließen
					tab-=2
					puffer.append(tab*' '+'</'+ liTag(vorgaenger[1], vorgaenger[2])+'>'+'\n')
					#neuen Eintrag öffnen
					puffer.append(tab*' '+ Tag +'\n')
					tab+=2
					Listenpunkte.append(Listenpunkt)
			else:
				EndeListenPunkt = liEnder.pop()
				tab-=2
				puffer.append(tab*' ' + EndeListenPunkt)
			if '::' in Listenpunkt[2]:
				Eintrag= Listenpunkt[2].split('::')
				puffer.append(tab*' ' + '<dt>'+Eintrag[0]+'</dt>\n')
				puffer.append(tab*' ' + '<dd>\n')
				tab+=2
				puffer.append(tab*' ' + Eintrag[1]+'\n')
				liEnder.append('</dd>\n')
			else:
				#puffer.append(tab*' ' + '<li>'+Listenpunkt[2]+'</li>\n')
				puffer.append(tab*' ' + '<li>\n')
				tab+=2
				puffer.append(tab*' ' + Listenpunkt[2]+'\n')
				#tab-=2
				liEnder.append('</li>\n')
		elif FortsetzungListe(orgZeile,Vorzeile):#Fortsetzung einer Liste
			puffer[-1]+=tab*' '+ maskiereSonderzeichen(orgZeile.strip()) +'\n'
		elif tabelle:#Tabelle
			# Aussgeschlossen sind hier Überschriften, Listen, und Fortsetzungen von Listen
			# hier geht es weiter, wenn es eine Tabellenzeile ist
			schliessen(LISTE+ABSATZ)
			pos=''
			zellen = orgZeile[:-1].strip('|').strip().split(' | ')
			if not istTabellenZeile(Vorzeile):
				#Tabellenbeginn / Tabellenkopf
				puffer.append(tab*' '+'<table>\n')
				tab+=2
				pos='th'
			else:
				pos='td'
			if tabelle==1:
				#DatenZeile schreiben
				setzeTabellenZeile(pos,zellen)
		elif len(orgZeile.strip())==0:#Leerzeile
			schliessen(LISTE+TABELLE+ABSATZ)
		elif isSetting(orgZeile): # übergibt Settings für die Erstellung der HTML-Datei
			# Verarbeitung erfolgt direkt in der Funktion isSetting
			schliessen(LISTE+TABELLE+ABSATZ)
		elif not DokumentUeberschrift:
			DokumentUeberschrift=True
			docTitel=maskiereSonderzeichen(orgZeile[:-1])
			headline=docTitel
			Zieldatei=docTitel
		else:
			# Textabsätze
			schliessen(LISTE+TABELLE)
			textAbsatz(orgZeile)
		#Vorzeile merken
		Vorzeile=orgZeile
	org.close()
	#Struktur schließen
	while Sektionen[-1][0] != 0:
		#Immer die Vorgänger-Sektion aus dem Puffer holen und schließen
		vorgaenger=Sektionen.pop()
		kommentar= '<!--'+vorgaenger[1]+' -->'
		if Sektionen[-1][0] == 0:
			puffer.append(tab*' '+'<p class="hoch"><a href="#Kopf">nach oben</a></p>\n')
		tab-=2
		puffer.append(tab*' '+'</div>'+kommentar+'\n')

	schreibeDoctype()
	schreibeDocFus()
	#html-Datei schreiben
	typ = '.php' if privat else '.html'
	if Zieldatei.find('/')==-1:
		Zieldatei=Zielpfad+Zieldatei
	if Zieldatei[-len(typ):] != typ:
		Zieldatei+=typ
	html = open(Zieldatei,"w")
	for pZeile in header:
		html.write(pZeile)
	for pZeile in puffer:
		html.write(pZeile)
	html.close()
	print(Zieldatei,'geschrieben')
	
