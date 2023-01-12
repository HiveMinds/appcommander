#!/usr/bin/env bash
# Script to export your self-signed root CA certificate to your phone
# through ADB.

PEM_FILE_NAME=ca.pem
hash=$(openssl x509 -inform PEM -subject_hash_old -in $PEM_FILE_NAME | head -1)
OUT_FILE_NAME="$hash.0"

cp $PEM_FILE_NAME $OUT_FILE_NAME
openssl x509 -inform PEM -text -in $PEM_FILE_NAME -out /dev/null >> $OUT_FILE_NAME

echo "Saved to $OUT_FILE_NAME"

#adb shell mount -o rw,remount,rw /system # Throws error:
#adb: error: failed to copy '4b1055ef.0' to '/system/etc/security/cacerts/4b1055ef.0': remote couldn't create file: Read-only file system
#4b1055ef.0: 0 files pushed, 0 skipped. 0.2 MB/s (2049 bytes in 0.011s)

# adb root
adb shell mount -o rw,remount,rw / # Worked to allow push to /system.

read -p "Mounted"
adb push $OUT_FILE_NAME /system/etc/security/cacerts/
#adb push 4b1055ef.0 /system/etc/security/cacerts/
read -p "Pushed"
# adb shell mount -o ro,remount,ro /system
adb shell mount -o ro,remount,ro /

read -p "ReMounted, now rebooting."
adb reboot
read -p "Reboot"
