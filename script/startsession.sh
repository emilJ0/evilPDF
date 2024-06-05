#!/bin/bash
ip=$1 # nimmt übergebenes Argument auf und speichert es in der Variable "ip"
DSTIP="$ip" msfconsole -r msf/sessions.rc # übergibt mithilfe von DSTIP "ip" an das Resource Script und startet dieses
