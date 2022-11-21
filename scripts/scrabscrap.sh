#!/bin/bash

# damit das Script beim Booten des Rechners ausgeführt wird, muss folgender Eintrag
# als User "pi" vorgenommen werden:
# crontab -e
# @reboot /home/pi/scrabble-scraper-v2/script/scrabscrap.sh &

export DISPLAY=:0

# working directory is $PYTHONDIR/work
SCRIPTPATH=$(dirname "$0")
PYTHONDIR="$(cd "$SCRIPTPATH/../python" && pwd)"
WORKDIR=$PYTHONDIR/work

# create directories
mkdir -p "$WORKDIR/log"
mkdir -p "$WORKDIR/web"
mkdir -p "$WORKDIR/recording"

# copy defaults if not exists
cp -n "$PYTHONDIR/defaults/scrabble.ini" "$WORKDIR/scrabble.ini"
cp -n "$PYTHONDIR/defaults/ftp-secret.ini" "$WORKDIR/ftp-secret.ini"
cp -n "$PYTHONDIR/defaults/log.conf" "$WORKDIR/log.conf"

# start app
export PYTHONPATH=src:
source ~/.venv/cv/bin/activate

cd "$PYTHONDIR"
python -m scrabscrap >> "$WORKDIR/log/game.log"
