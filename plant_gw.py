#!/usr/bin/env python
#
# Example using Dynamic Payloads
# 
#  This is an example of how to use payloads of a varying (dynamic) size.
# 

from __future__ import print_function
import time
from datetime import datetime
from RF24 import *
import OPi.GPIO as GPIO
import struct
import paho.mqtt.client as mqtt
irq_gpio_pin = None

########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/RPi/pyRF24/readme.md

# CE Pin, CSN Pin, SPI Speed

# Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 8Mhz
#radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)

#RPi B
# Setup for GPIO 15 CE and CE1 CSN with SPI Speed @ 8Mhz
#radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)

#RPi B+
# Setup for GPIO 22 CE and CE0 CSN for RPi B+ with SPI Speed @ 8Mhz
#radio = RF24(RPI_BPLUS_GPIO_J8_15, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)

# RPi Alternate, with SPIDEV - Note: Edit RF24/arch/BBB/spi.cpp and  set 'this->device = "/dev/spidev0.0";;' or as listed in /dev
radio = RF24(2, 10);


# Setup for connected IRQ pin, GPIO 24 on RPi B+; uncomment to activate
#irq_gpio_pin = RPI_BPLUS_GPIO_J8_18
#irq_gpio_pin = 24

##########################################

#def on_connect(client, userdata, flags, rc):
#    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("hometest/elias/balcon")

# The callback for when a PUBLISH message is received from the server.
#def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))

#def on_message(client, userdata, msg):
#	print(str(msg.payload))


#def setup_mqtt():
#	global client 
#	client = mqtt.Client()
#	client.on_connect = on_connect
#	client.on_message = on_message
#	client.connect("broker.hivemq.com", 1883, 60)

def RadioSetup():
	radio.begin()
	radio.setPALevel(RF24_PA_MAX)
	radio.setDataRate(RF24_2MBPS)
	radio.setChannel(0x4C)
	radio.enableDynamicPayloads()
	radio.setRetries(5,15)
	radio.openReadingPipe(1,0xF0F0F0F0D2)
	#radio.openWritingPipe(0xF0F0F0F0D2)
	radio.printDetails()

	


RadioSetup()
#setup_mqtt()
#radio.stopListening()
# forever loop
radio.startListening()
while 1:
	#client.loop()
	if radio.available():
			plen = radio.getDynamicPayloadSize()
			receive_payload = radio.read(plen)
			hum, temp, soil, light = struct.unpack('BBHH',receive_payload)
			print('Humidity: ' +str(hum) + ' % ' +'Temperature: ' + str(temp) + ' Celsius ' +'Soil moisture: '+ str(soil) + ' ' + 'Light: ' + str(light))
