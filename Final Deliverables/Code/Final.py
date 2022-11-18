import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import os
from twilio.rest import Client
account_sid = 'ACdf538f343de5d91d1c1d2c5d79469482'
auth_token = 'f8615a53b24f4b2cb2ce3627409592b8'


#Provide your IBM Watson Device Credentials
organization = "hycgw4"
deviceType = "Industry"
deviceId = "Safety"
authMethod = "token"
authToken = "6cj)4?!*u8kwo*84a6"

# Initialize GPIO


def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data['command'])
    status=cmd.data['command']
    if status=="Sprinkler On":
        print ("Sprinkler is on")
    elif status=="Sprinkler Off": 
        print ("Sprinkler is off")
    elif status=="Exhaust On":
        print ("Exhaust is on")
    else : 
        print ("Exhaust is off")    
   
    #print(cmd)
    
        


try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a data
deviceCli.connect()

while True:
        #Get Sensor Data from DHT11
        
        Temperature=random.randint(60,100)
        Humidity=random.randint(0,50)
        data = { 'Temperature' : Temperature, 'Humidity': Humidity }
        #print data
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % Temperature, "Humidity = %s %%" % Humidity, "to IBM Watson")    
        

        success = deviceCli.publishEvent("IoTSensor", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(10)
        if Temperature==100:
           print("Sprinkler is ON")
           client = Client(account_sid, auth_token)

           message = client.messages \
           .create(
           from_ =  '+19789615397',
           body='Emergency!!',
           to = '+917502272799')
           print(message.sid)
           
        else :
            print(" ")
        
        
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
