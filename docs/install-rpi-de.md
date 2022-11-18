# Installation ScrabScrap v2

## Basis-Installation des RPI

Für die Installation muss entweder die 64bit oder due 32bit Variante des PI OS Lite gewählt werden.

### 32bit

Die Erzeugung der SD Karte mittels "Raspberry Pi Imager". Hier das Image "PI OS Lite (64bit) - Debian Bullseye" auswählen.

Bei dem Erzeugen der SD Karte ggf. folgende Optionen konfigurieren

- hostname = scrabscrap
- ssh aktivieren = true
- WiFi Zugriff = ID / Passwort
- User / Passwort = (alter default: pi/raspberry)
- Spracheinstellungen

Nachdem der RPI gestartet wurde, per ssh eine Verbindung zum Rechner aufbauen.

```bash
sudo apt-get update
sudo apt-get upgrade
sudp apt-get autoremove
```

Nach dem Update technische Einstellungen auf dem RPI vornehmen

```bash
sudo raspi-config
```

Es müssen aktiviert werden

- Kamera (Legacy Camera aktivieren)
- i2c

#### Git und Python Libraries installieren (32bit)

```bash
sudo apt-get install -y git python3-venv python3-dev
#installation des Tools, um die ic2 Ports zu ermitteln (i2cdetect -y 1)
sudo apt-get install -y i2c-tools
#Installation der Libs für OpenCV
sudo apt-get install -y libgsm1 libatk1.0-0 libavcodec58 libcairo2 libvpx6 libvorbisenc2 
libwayland-egl1 libva-drm2 libwavpack1 libshine3 libdav1d4 libwayland-client0 libxcursor1 
libopus0 libchromaprint1 libxinerama1 libpixman-1-0 libzmq5 libmp3lame0 libxcb-shm0 libsz2 
libgtk-3-0 libharfbuzz0b libilmbase25 libvdpau1 libssh-gcrypt-4 libpangocairo-1.0-0 
libtwolame0 libnorm1 libxi6 libxfixes3 libxcomposite1 libxcb-render0 libwayland-cursor0 
libvorbisfile3 libspeex1 libxrandr2 libxkbcommon0 libtheora0 libaec0 libx264-160 libaom0 
libzvbi0 libopenexr25 libogg0 libpangoft2-1.0-0 librsvg2-2 libxvidcore4 libsrt1.4-gnutls 
libbluray2 libvorbis0a libdrm2 libmpg123-0 libatlas3-base libxdamage1 libavformat58 
libatk-bridge2.0-0 libswscale5 libsnappy1v5 libcodec2-0.9 libsodium23 libudfread0 
libswresample3 libcairo-gobject2 libx265-192 libthai0 libva-x11-2 ocl-icd-libopencl1 
libepoxy0 libpango-1.0-0 libavutil56 libva2 librabbitmq4 libgme0 libatspi2.0-0 
libgraphite2-3 libhdf5-103-1 libgfortran5 libsoxr0 libpgm-5.3-0 libopenmpt0 libxrender1 
libdatrie1 libgdk-pixbuf-2.0-0 libopenjp2-7 libwebpmux3 --fix-missing
```

### 64bit (draft - PICamera muss noch reimplementiert werden)

Die Erzeugung der SD Karte mittels "Raspberry Pi Imager". Hier das Image "PI OS Lite (64bit) - Debian Bullseye" auswählen.

Bei dem Erzeugen der SD Karte ggf. folgende Optionen konfigurieren

- hostname = scrabscrap
- ssh aktivieren = true
- WiFi Zugriff = ID / Passwort
- User / Passwort = (alter default: pi/raspberry)
- Spracheinstellungen

Nachdem der RPI gestartet wurde, per ssh eine Verbindung zum Rechner aufbauen.

```bash
sudo apt update
sudo apt full-upgrade
```

Nach dem Update technische Einstellungen auf dem RPI vornehmen

```bash
sudo raspi-config
```

Es müssen aktiviert werden

- **deaktiviere** legacy Camera
- i2c

#### Git und Python Libraries installieren (64bit)

```bash
sudo apt install -y git python3-venv python3-dev
#installation des Tools, um die ic2 Ports zu ermitteln (i2cdetect -y 1)
sudo apt install -y i2c-tools
#Installation der Libs für OpenCV
sudo apt install -y --fix-missing libjpeg-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libgtk2.0-dev
sudo apt install -y --fix-missing libcanberra-gtk* libgtk-3-dev libgstreamer1.0-dev gstreamer1.0-gtk3 
sudo apt install -y --fix-missing libgstreamer-plugins-base1.0-dev gstreamer1.0-gl libxvidcore-dev libx264-dev libtbb2 
sudo apt install -y --fix-missing libtbb-dev libdc1394-22-dev libv4l-dev v4l-utils libopenblas-dev libatlas-base-dev 
sudo apt install -y --fix-missing libblas-dev liblapack-dev gfortran libhdf5-dev
```

## Clone des ScrabScrap Repositories

Falls von dem RPI auch Commits an das Repository vorgenommen werden sollen, muss
die GitHub Userkennung gesetzt werden.

```bash
git config --global user.name
git config --global user.email
git config --global credential.helper store
git config --global pull.rebase true
git config --global pull.autostash true
```

Danach kann das Repository geladen werden

```bash
cd
git clone https://github.com/scrabscrap/scrabble-scraper-v2.git
```

## Python Konfiguration erzeugen

```bash
cd ~/scrabble-scraper-v2/python
python3 -m venv .venv --prompt cv
#update pip
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install --force-reinstall -r requirements.txt --only-binary=:all:
```

## Testen der Installation

### OpenCV

Die Installation von OpenCV kann wie folgt geprüft werden

```bash
#venv cv aktivieren
source ~/scrabble-scraper-v2/python/.venv/bin/activate
python
>> import cv2
>> cv2.__version__
'4.5.5'
>> quit()
```

### i2c Bus

Prüfen des Zugriffes auf den i2c Bus

```bash
sudo i2cdetect -y 1
```

## Weitere Konfigurationen

Eine Datei `~/.bash_aliases` anlegen:

```bash
alias ll='ls -al'
alias ..='cd ..'
alias ...='cd ../..'
alias cd..='cd ..'
alias workon='f(){ source ~/scrabble-scraper-v2/python/.venv/bin/activate; }; f'
```

## Autostart von ScrabScrap konfigurieren

Um ScrabScrap automatisch zu starten, muss man auf dem RPI angemeldet sein und dann über `crontab -e`
die Konfiguration der crontab-Einträge des Benutzers vornehmen:

```bash
@reboot /home/pi/scrabble-scraper-v2/scripts/scrabscrap.sh &
```

## boot/config.txt einstellen

- i2c mit Baudrate 400000
- spi=off
- i2c bus 3 auf GPIO5 und GPIO6
- Power LED ausschalten
- Bluetooth ausschalten
- Audio aus

```text
# Uncomment some or all of these to enable the optional hardware interfaces
dtparam=i2c_arm=on,i2c_baudrate=400000
#dtparam=i2s=on
dtparam=spi=off

# use gpio5 (pin 29) as sda and gpio6 (pin 31) as scl
# see https://www.instructables.com/Raspberry-PI-Multiple-I2c-Devices/
dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=5,i2c_gpio_scl=6

#Power-LED ausschalten
dtparam=pwr_led_trigger=none
dtparam=pwr_led_activelow=off
# Disable Bluetooth
dtoverlay=disable-bt

#Camera LED off
# disable_camera_led=1

# Uncomment this to enable infrared communication.
#dtoverlay=gpio-ir,gpio_pin=17
#dtoverlay=gpio-ir-tx,gpio_pin=18

# Additional overlays and parameters are documented /boot/overlays/README

# Enable audio (loads snd_bcm2835)
dtparam=audio=off
```

## Automatischer HotSpot

siehe [GitHub Projekt https://github.com/gitbls/autoAP](https://github.com/gitbls/autoAP)

```bash
sudo curl -L https://github.com/gitbls/autoAP/raw/master/autoAP.sh -o /usr/local/bin/autoAP.sh
sudo curl -L https://github.com/gitbls/autoAP/raw/master/install-autoAP -o /usr/local/bin/install-autoAP
sudo curl -L https://github.com/gitbls/autoAP/raw/master/rpi-networkconfig -o /usr/local/bin/rpi-networkconfig
sudo chmod 755 /usr/local/bin/autoAP.sh /usr/local/bin/install-autoAP /usr/local/bin/rpi-networkconfig
sudo /usr/local/bin/install-autoAP
```

Als AP folgende Werte eingeben

- ssid = ScrabScrap
- psk = scrabscrap
- ip = 10.0.0.1

Zusätzlich muss noch ein lokales WLAN angegeben werden (i.d.R. das WLAN mit dem gerade eine Verbindung besteht).

Am Ende ggf. mit `sudo /usr/local/bin/rpi-networkconfig` auf `systemd-networkd` einstellen.

Befehle für den Zugriff auf die Netzwerkkonfiguration

```bash
iwgetid
wpa_cli list_networks -i wlan0
wpa_cli remove_network <number> -i wlan0
wpa_cli save_config
wpa_cli scan -i wlan0
wpa_cli scan_results -i wlan0
wpa_passphrase {ssid} {key}
```

## Sonstiges

### Installation RTC

Siehe: [Adding a Real Time Clock (RTC) to the Raspberry Pi](https://pimylifeup.com/raspberry-pi-rtc/)

```bash
sudo nano /boot/config.txt
```

Add (currently used: DS3231 RTC)

```text
dtoverlay=i2c-rtc,ds3231
```

```bash
sudo reboot
sudo apt -y remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove
sudo nano /lib/udev/hwclock-set
```

Comment out

```text
#if [ -e /run/systemd/system ] ; then
#    exit 0
#fi
```

Read the time directly from the RTC module

```bash
sudo hwclock -v -r
```

### Optimierungen

#### Bluetooth ausschalten

```bash
sudo nano /boot/config.txt
```

```text
# Disable Bluetooth
dtoverlay=disable-bt
```

```bash
sudo systemctl disable hciuart.service
sudo systemctl disable bluealsa.service
sudo systemctl disable bluetooth.service
```

Zum Aktivieren der Änderung einen Reboot durchführen.

#### Avahi ausschalten

```bash
sudo service avahi-daemon stop
sudo systemctl disable avahi-daemon
```

### System Logging ausschalten

```bash
service rsyslog stop
systemctl disable rsyslog
```

### Journalctl Schreiben auf Disk ausschalten

`sudo nano /etc/systemd/journald.conf`

```text
[Journal]
Storage=volatile
RuntimeMaxUse=32M
```
