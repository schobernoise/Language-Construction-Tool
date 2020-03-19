# lct
Language Construction Tool

## VOCBULARY

User öffnet Programm
Startup screen mit description und About = default view
1. Create new DB
DB File wird erstellt und geladen
was heißt "geladen"?
2. Load DB-FIle
Dass ein DB-File geladen ist, sieht man an folgenden Punkten:
- Der Titel enthält Namen und Informationen wie Word Count
- Die Tree View ist leer/befüllt, je nachdem
- Das Bild zeigt entweder den "empty"-platzhalter, oder das bild des markierten wortes

Also das Programm hat folglich zwei Modi:
- Start_up
- loaded

Immer wenn es nichts geladen hat, wird also der start_up screen gezeigt.
Wenn es etwas geladen hat:
- Start_up = False
- Model_Object lct_voc wird instanziiert
- Start_up = True
- Model_Object start_info

**TABLES**

### Vocabulary

- [generated_id] INTEGER PRIMARY KEY
- [word] text
- [translation] text
- [pos] text
- [example_sentence] text
- [example_translation] text
- [description] text
- [related_words] text
- [related_image] image

## LANGUAGE CONSTRUCTOR

-  Härtegrad der Betonung (B, P) (C,Z)
	
-  Öffnung des mundes (M, N, O)

-  Schärfegrad (des Zischens) (S, Z, C)

Es gibt dann regler, Die die toleranz der einzelnen buchstaben zu bestimmten Buchstaben-attributes bei nachfolgenden Buchstaben ändern können,
Um so die generierten worte tweaken zu können.
Am besten würde dies live auf einer wbesite funktionieren,
Aka python to javascript

--------------------------------
Parameter zur Erstellung (Optional):

	- Worte als Liste
	- Wenn ja, wie viele (max value)
	
Bei Verben:
	- Konjugation
	- Zeitformen

Bei Nomen:
	- Plural
	- Fälle

	- Grammatiktabelle, mit Bsp-Worte und den einzelnen Silben aufgeschlüsselt

Wenn diese Pramater angewählt werden, so generiert der Algorithmus vor der Wortgenerierung Silben um sie in die ausgewählten gramatikalischen Funktionen einsetzen zu können
	

## DATABASE MANAGER

Dieser ist zur Verwaltung der bereits generierten Worte da.

Im Lan_con Modul generierte Worte können hier automatisch übernommen werden. Entweder sie werden einzeln gepickt und manuell eingefügt,
Oder man kann sich gleich ein ganzes Basisset mit 500 wichtigen Wörtern wie 
Sein, haben, wollen, ich, etc,
Generieren lassen, auf dem dann aufgebaut werden kann.

Neben der Vokabelliste verfügt die csv auch über
	- Grammatikregeln
	- 


## TRANSLATOR

## TRANSCRIPTOR

## SENTENCE GENERATOR

Für den Translator muss mit Dictionaries gearbeitet werden. Dabei kann dieses Modul - genau wie die anderen module - die selbe csv benützen.

Eher ein Tool, um Sätze zu bilden, 
Um zu sehen wie sich die Sprache anfühlt.


## LANGUAGE MORPHER

Es wird ein Model integriert, welchen texte gefeedet werden können, 
und anhand dessen eine neue Sprache generiert werden kann - ein **MOPRH **
Wie bei Absynth
Werden verschiedene Sprachen in einem Batch reingefeedet, so werden 
diese miteinander vermorpht
Verschiedene Morphmodi und Paramater möglich