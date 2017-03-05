Simple Python3 script that takes a picture from CSI camera, reads HMC5883L I2C compass heading and overlay the picture. It than sends it over FTP to the server in specified interval. Useful as a meteo cam and because I have it on rotary mast with antennas, compass comes on scene.

Also enable I2C bus and camera in raspi-config

# How to install
```sh
git clone git://github.com/pilotak/raspberry-python-webcam.git
cd ./raspberry-python-webcam
sudo apt-get install python3-smbus python3-picamera dos2unix
sudo apt-get install libfreetype6-dev libtiff4-dev libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
sudo pip3 install pillow -I

dos2unix ./meteo.py && chmod +x ./meteo.py
```

## Calibration
[Please follow this link](http://blog.bitify.co.uk/2013/11/connecting-and-calibrating-hmc5883l.html)

Make some config in meteo.py and you set up!

### To run it forever
```sh
crontab -e
# append to the end of file
* * * * * python3 /home/pi/raspberry-python-webcam/meteo.py > /home/pi/raspberry-python-webcam/.log
```
