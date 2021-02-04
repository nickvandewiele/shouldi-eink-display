#!/bin/bash
sudo apt install git python3-pandas python3-pip python3-matplotlib

## Install Inky dependencies
curl https://get.pimoroni.com/inky | bash

## Fetch the display repo code
git clone https://github.com/openbook/shouldi-eink-display.git

cd should-eink-display

### pi specific pandas
pip3 install pytz
pip3 install flask
#pip3 install matplotlib

# Add cron schedule
line="*/30 * * * * $(pwd)/display.py"
echo $line
(crontab -u pi -l; echo "$line" ) | crontab -u pi -
