#!/bin/bash
whiptail --msgbox "Please remove all keys" 10 30
whiptail --msgbox "Insert the BLUE key with your transaction and press OK" 10 30
# Wait to See plug on dmesg
whiptail --infobox "Waiting for BLUE key insertion" 10 30
sleep 3
whiptail --infobox "Copying transaction" 10 30
sleep 3
whiptail --msgbox "Insert the RED key" 10 30
whiptail --infobox "Signing transaction" 10 30
sleep 3
whiptail --msgbox "Scan the following code to broadbast signed transaction" 10 30
fbi t.png
