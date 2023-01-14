#!/usr/bin/env bash
# Script to export your self-signed root CA certificate to your phone
# through ADB. No reboot required. No root required.
install_self_signed_root_ca_on_android() {
    certificateName="$1"

    #certificateName=ca.crt
    ca_dir_in_phone="/data/local/tmp/try3"
    ca_path_in_phone="$ca_dir_in_phone/$certificateName"

    adb shell mkdir -m 700 "$ca_dir_in_phone"
    adb push "$certificateName" "$ca_path_in_phone"

    adb shell am start -n com.android.certinstaller/.CertInstallerMain -a android.intent.action.VIEW -t application/x-x509-ca-cert -d file://"$ca_path_in_phone"
}
