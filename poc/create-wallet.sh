#!/bin/bash
whiptail --msgbox "Please insert the RED key" 10 30 &
sleep 2
kill %1
./touchscreen_1.sh

#Here check for keys inserted via dmesg

whiptail --msgbox "Please insert the BLUE key" 10 30 &
sleep 2
kill %1
./touchscreen_1.sh

#Mount them both
mkdir /media/REDKEY; mkdir /media/BLUEKEY
mount /dev/sda1 /media/REDKEY; mount /dev/sdb1 /media/BLUEKEY

whiptail --infobox "Creating wallet" 10 30

WALLET_TS=`date +"%s"`
WALLET_NAME=redwallet-RED-${WALLET_TS}_wallet
WALLET_PATH=/media/REDKEY/$WALLET_NAME
strace electrum create -o -w $WALLET_PATH

cp $WALLET_PATH /run
electrum deseed -o -w /run/$WALLET_NAME
mv /run/$WALLET_NAME /media/BLUEKEY/redwallet-BLUE-${WALLET_TS}_wallet

umount /media/REDKEY; umount /media/BLUEKEY
 
whiptail --infobox "You can now remove both keys" 10 30
