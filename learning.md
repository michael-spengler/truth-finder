# Learnings
Hier möchten wir die Learnings und den Gedankenprozess hinter der Entwicklung des Truth-Finders darstellen und getroffene Entscheidungen begründen.

## Modell

### Modellart
Transformer, weil cool.

### Score
Das Thema "Fake News Detection" ist keine einfache Aufgabe und konnte aus unserer Ansicht nicht durch eine Binärklassifikation gelöst werden.
Es ist nicht immer eindeutig zu bestimmen ob ein Artikel "wahr" oder "falsch" ist, weil unter Umständen einfach Details fehlen oder Sachverhalte zu wage beschrieben werden.
Solche Dinge werden üblicherweise auf von Menschen geführten Fact-Checking geprüft und in deutlich detaillierte Kategorien eingeordnet. Diese möchten wir uns zu nutze machen,
indem wir die dort recherchierten Artikel über ein Scraping, unterstützt durch [][], sammeln. Die dort verwendeten Scores können dann in einen einheitlichen kontinuierlichen
Score übersetzt werden. So kann das Modell auf eine Regression trainiert werden. 

## Website

### Artikel
Artikel werden nicht auf der Seite direkt gehostet, weil wir keine Rechte an diesen haben und den Seiten keinen Traffic streitig machen möchten. User geben lediglich den Titel,
die Url und einen zusätzlichen Kommentar zu dem genannten Artikel an. In dem Kommentar kann beispielsweise die Aussage, die fragwürdig erscheint zitiert werden oder der Artikel
kurz zusammengefasst werden

### 

## Betting

### Verdeckter Score
