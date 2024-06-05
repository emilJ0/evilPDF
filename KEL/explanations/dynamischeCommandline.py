def test(): # 'def' gibt an das es sich um eine Funktion handelt; 'test' ist der Name; '()' beinhaltet die verwendeten Argumente
    print("1,2,3, Test") # 'print' gibt Text aus

befehle = { # Name des Dictionary
    "check": test, # verbindet die Eingabe "test" mit der oben beschriebenen Funktion test.
}

while True: # definiert die unendliche Schleife
    befehl = input("Gib deinen Befehl ein: ") # wartet auf Text-Input durch den Nutzer und speichert diesen in der Variable "befehl"
    if befehl in befehle:
        befehle[befehl]()
