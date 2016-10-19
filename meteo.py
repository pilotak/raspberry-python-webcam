#!/usr/bin/python3
import smbus
import math
import time
import datetime
from ftplib import FTP
import picamera
import os
import subprocess
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import Image

## CONFIG
localPath = "/home/pi/raspberry-python-webcam/"
imageFile = "image.jpg"
font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf",25)

compass_address = 0x1e
x_offset = -82
y_offset = -15

ftpHost = ""
ftpUser = ""
ftpPassword = ""
remotePath = "/camera/"
remoteFile = "output.jpg"
##

bus = smbus.SMBus(1)

def read_byte(adr):
    return bus.read_byte_data(compass_address, adr)

def read_word(adr):
    high = bus.read_byte_data(compass_address, adr)
    low = bus.read_byte_data(compass_address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(compass_address, adr, value)

write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
write_byte(2, 0b00000000) # Continuous sampling

scale = 0.92

x_out = (read_word_2c(3) - x_offset) * scale
y_out = (read_word_2c(7) - y_offset) * scale
z_out = (read_word_2c(5)) * scale


bearing  = math.atan2(y_out, x_out) 
if (bearing < 0):
    bearing += 2 * math.pi

degrees = round(math.degrees(bearing))

camera = picamera.PiCamera()
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'horizon'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 180
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)
camera.capture(localPath + imageFile)

img = Image.open(localPath + imageFile)
basewidth = 640
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)

draw = ImageDraw.Draw(img)
draw.text((430, 450), datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),(255,255,255),font=font)
#draw.text((10, 55), "Test",(255,255,255),font=font)

compass = Image.open(localPath+"compass.png")
img.paste(compass, (555, 10), compass)

needle = Image.open(localPath+"needle.png")
needle = needle.rotate(degrees,PIL.Image.BICUBIC)
needle = needle.transpose(Image.FLIP_LEFT_RIGHT)
#needle = needle.rotate(180)
img.paste(needle, (556, 10), needle)

draw = ImageDraw.Draw(img)
img.save(localPath+imageFile, "jpeg", quality=100)

del draw, img, compass, needle
time.sleep(2)

session = FTP(ftpHost, ftpUser, ftpPassword)
session.cwd(remotePath)
file = open(localPath+imageFile,'rb')
session.storbinary('STOR '+remoteFile, file)
file.close()
session.quit()
