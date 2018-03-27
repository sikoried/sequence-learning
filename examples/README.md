# Beispielprojekt

Dies ist ein weiteres kleines Beispielprojekt analog zum [Tutorium](https://github.com/hsro-wif-prg2/tutorial).
Versuchen Sie die Klasse `Bug` (`src/main/java/Bug.java`) so auszubessern, dass die Tests in `BugTests` (`src/test/java/BugTests.java`) korrekt durchlaufen.

1. Erstellen Sie wieder einen persönlichen Fork des Projekts.

2. Klonen Sie das Projekt lokal, in dem Sie in IntelliJ das Projekt von Git importieren lassen, oder "per Hand" in der Konsole: `git clone htps://github.com/IHR_BENUTZERNAME/example.git`

3. Erstellen Sie einen lokalen Branch `loesung` (oder einem anderen Namen Ihrer Wahl), entweder in IntelliJ (Git Schaltfläche rechts unten -> "+ New Branch") oder in der Konsole (Schaltfläche links unten: "Console"/"Konsole") `git checkout -b loesung`

4. Finden und beheben Sie den bzw. die Fehler.
	Tests werden mit den kleinen grünen Playschaltern links neben dem Editorfeld gestartet (oder mit Rechtsklick auf der Klasse).

5. Fügen Sie die geänderte Datei `Bug.java` Ihrem Commit hinzu, im IntelliJ mit Rechtsklick -> Git -> Add, oder in der Konsole mit `git add src/main/java/Bug.java`

6. Committen und pushen Sie die Änderungen, entweder via VCS -> Commit Changes -> Commit and Push, oder in der Konsole mit
	```
	git commit -m "Ihre Commit-Nachricht"
	git push -u origin loesung
	```

7. Erstellen Sie einen _pull request_ von Ihrem Branch `loesung` zum `master` Branch.

Glückwunsch, schon wieder ein Beispiel geschafft!


# Zusatzaufgabe

Erstellen Sie nun ein eigenes Repository, fügen Sie eine Datei hinzu, und lassen Sie eine FreundIn dieses forken, einen Branch erstellen, eine Änderung vornehmen, und einen Pull Request zu Ihnen erstellen.
