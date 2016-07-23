# org2html
Python-Script, das eine emacs-org-Datei in eine html-Datei umwandelt

* Idee
Die Idee, die hinter diesem Programm steckt war die, das ich
sehr gern meine eigne Dokumentation mit den Emacs-Org-Mode
erstelle.  Allerdings fehlt mir hier die Möglichkeit, dies
online anzuzeigen.  Hierfür muss dies in eine HTML-Datei
überführt werden.

* Problem
Hierfür bietet der Org-Mode eine eingebaute Funktion, die
aus dem Text eine html-Datei erstellt.  Allerdings
verschwindet dabei die vom Org-Mode her bekannte Möglichkeit
Text unter einer Überschrift auszublenden und dies
hierachisch zu gestalten.

* Lösung
Die Lösung dafür soll dieses Script sein. Es erstellt
ebenfalls eine Html-Datei, bindet allerdings einen
Java-Scriptteil ein, der dafür sorgt das Texte unter der
Überschrift durch anklicken der Überschrift ein- und
ausgeblendet werden. Hierzu versieht das Programm die
HTML-Datei mit einer passenden DIV-Struktur