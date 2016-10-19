Simple Python3 script that takes a picture from CSI camera, reads HMC5883L I2C compass heading and overlay the picture. It than sends it over FTP to the server in specified interval. Useful as a meteo cam and because I have it on rotary mast with antennas, compass comes on scene.

Also enable I2C bus and camera in raspi-config

# How to install
```sh
git clone git://github.com/pilotak/raspberry-python-webcam.git
cd ./raspberry-python-webcam
sudo apt-get install libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms1-dev libjpeg-dev python3-picamera
sudo pip-3.2 install pillow -I
chmod +x ./meteo.py
chmod +x ./cron.sh
```

## Calibration
[Please follow this link](http://blog.bitify.co.uk/2013/11/connecting-and-calibrating-hmc5883l.html)

Make some config in meteo.py and you set up!

### To run it forever
```sh
crontab -e
# append to the end of file
* * * * * /home/pi/raspberry-python-webcam/cron.sh > /home/pi/raspberry-python-webcam/.log 2>&1
```
