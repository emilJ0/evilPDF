# evilPDF

Das Projekt schafft eine einfache Bedienung des "/windows/fileformat/adobe_pdf_embedded_exe"-Exploits von dem Metasploitframework. Dabei können die evilPDFs noch an angegebene Email-Adressen versendet werden.

## Inhaltsverzeichnis
1. [Motivation](#Motivation)
1. [Installation](#installation)
2. [Nutzung](#nutzung)
3. [Beispiele](#beispiele)
4. [Beitrag](#beitrag)
5. [Lizenz](#lizenz)
6. [Autoren](#autoren)
7. [Versionierung](#versionierung)
8. [Fehlerberichte und Support](#fehlerberichte-und-support)
9. [Weitere Informationen](#weitere-informationen)

## Motivation

Durch ein Video von dem Youtuber "Loi Liang Yang" wurde ich auf den Exploit aufmerksam und fragte mich inwieweit ein Tool entwickelt werden könnte, welches die infiziertes PDFs per Email versenden zu können. So entwickelte sich das Projekt und letztendlich ist ein flexibles Tool namens "evilPDF" entstanden.

## Installation

### Voraussetzungen

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

### Installationsanleitung

1. Schritt 1
2. Schritt 2
3. Schritt 3

## Nutzung

Grundlegende Informationen zur Nutzung des Projekts.

## Beispiele

```python
# Code-Beispiel
print("Hallo Welt")
