speicherDatei = open("explanations/speicherDatei.txt", "a")
speicherDatei.write("Neuer Eintrag in Datei")
speicherDatei = open("explanations/speicherDatei.txt", "r")
print(speicherDatei.read())
