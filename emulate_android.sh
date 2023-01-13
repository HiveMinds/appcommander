#!/bin/bash
# This script installs android studio and than installs an emulated Android
# phone on it, with GUI.
# Source: https://github.com/Uirado/linux-bash-install/blob/a150a462d2f9d095734f10a7b8c6c39871e5df71/batch-install.sh

yes | sudo apt install openjdk-8-jdk
echo 'export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")' >> ~/.profile
sudo update-java-alternatives --set java-1.8.0-openjdk-amd64
. ~/.profile

sudo apt update
sudo apt upgrade

#installLog "Android SDK"
mkdir -p ~/Android/Sdk
wget -O ~/Android/Sdk/android-sdk.zip "https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip"
unzip -o -qq ~/Android/Sdk/android-sdk.zip -d ~/Android/Sdk
rm ~/Android/Sdk/android-sdk.zip
mv ~/Android/Sdk/tools/emulator ~/Android/Sdk/tools/emulator2


wget -O ~/gradle-4.10.3.zip https://downloads.gradle-dn.com/distributions/gradle-4.10.3-all.zip
unzip -o -qq ~/gradle-4.10.3.zip -d ~/

echo 'export GRADLE_HOME=$HOME/gradle-4.10.3' >> ~/.profile
echo 'export ANDROID_HOME=$HOME/Android/Sdk' >> ~/.profile
echo 'export ANDROID_SDK_ROOT=$ANDROID_HOME' >> ~/.profile
echo 'export PATH=$PATH:$ANDROID_HOME/tools' >> ~/.profile
echo 'export PATH=$PATH:$ANDROID_HOME/tools/bin' >> ~/.profile
echo 'export PATH=$PATH:$GRADLE_HOME/bin' >> ~/.profile

. ~/.profile
mkdir -p ~/.android
touch ~/.android/repositories.cfg
installLog "Android SDK packages"
sdkmanager --install "platform-tools"
sdkmanager --install "build-tools;29.0.2"
sdkmanager --install "extras;google;google_play_services"
sdkmanager --install "system-images;android-28;google_apis_playstore;x86_64"

sdkmanager --install emulator
echo 'export PATH=$PATH:$ANDROID_HOME/emulator' >> ~/.profile
. ~/.profile

# create android VMs android-small and @android-large
avdmanager create avd -n "android-small" -k "system-images;android-28;google_apis_playstore;x86_64"
avdmanager create avd -n Emulator-Api23-Default -c 12M -f -k "system-images;android-28;google_apis_playstore;x86_64"

# Show installed android devs:
emulator -list-avds

# Launch emulated phone:
#emulator -avd android-small -netdelay none -netspeed full
emulator -avd android-small -netdelay none -netspeed full -skin 768x1280
#emulator -avd Emulator-Api23-Default -netdelay none -netspeed full -skin 768x1280
