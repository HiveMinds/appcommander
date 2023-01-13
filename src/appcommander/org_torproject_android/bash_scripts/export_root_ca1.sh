#!/usr/bin/env bash
# Script to export your self-signed root CA certificate to your phone
# through ADB. Root required. No reboot required.

certificatePath=ca.pem

set -e # Fail on error
# Create a separate temp directory, to hold the current certificates
# Without this, when we add the mount we can't read the current certs anymore.

#adb shell mkdir -m 700 /data/local/tmp/htk-ca-copy
read -p "made dir"

# Copy out the existing certificates
adb shell cp /system/etc/security/cacerts/* /data/local/tmp/htk-ca-copy/
read -p "copied file"

# Create the in-memory mount on top of the system certs folder
adb shell mount -t tmpfs tmpfs /system/etc/security/cacerts
read -p "Mounted virtual folder."

# Copy the existing certs back into the tmpfs mount, so we keep trusting them
adb shell mv /data/local/tmp/htk-ca-copy/* /system/etc/security/cacerts/
read -p "Copied existing certificates back."

# Copy our new cert in, so we trust that too
adb shell mv ${certificatePath} /system/etc/security/cacerts/
read -p "Copied new certificates in."

# Update the perms & selinux context labels, so everything is as readable as before
adb shell chown root:root /system/etc/security/cacerts/*
read -p "Restored permissions I."
adb shell chmod 644 /system/etc/security/cacerts/*
read -p "Restored permissions II."
adb shell chcon u:object_r:system_file:s0 /system/etc/security/cacerts/*
read -p "Restored permissions III."

# Delete the temp cert directory & this script itself
adb shell rm -r /data/local/tmp/htk-ca-copy
read -p "Removed temp cert dir."
#rm ${injectionScriptPath}
echo "System cert successfully injected"
