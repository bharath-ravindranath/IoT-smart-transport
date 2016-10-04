import sys
import ibmiotf.api
import ibmiotf
import ibmiotf.device
import logging
import json
import mraa, time
from uuid import getnode as get_mac

''' List of stations (We should make a database to put list of stations)'''
signal = {
  14: "red",
  36: "yellow",
  48: "green"
}


''' Connection establishment to IBM Bluemix Cloud'''
cloudTopic = "trafficSignal"

''' When at a station, We press the appropriate button, which will send the 
message to IBM Blumix for the device location'''
''' When at a station, We press the appropriate button, which will send the 
message to IBM Blumix for the device location'''
def onButtonPush(gpio):
  if gpio.read() == 1:
    status = signal[gpio.getPin(False)]
    data = {
      "d" : {
        "name" : mystation,
        "status": status
      }
    }
    print(data)

    cloudClient.publishEvent(cloudTopic, "json", data)

def main():
  try:
    with open('credentials.json') as data_file:    
      apiOptions  = json.load(data_file)
    
    logger = logging.getLogger("TestApi")
    apiClient   = ibmiotf.api.ApiClient(apiOptions, logger)

    deviceTypeId = "Signal"

    deviceId = str(get_mac())
    authToken = "EcE592net"
    
    print("\nRegistering a new device") 
    print("Registered Device = ")
    apiClient.registerDevice(deviceTypeId, deviceId, authToken)
    print(json.dumps(apiClient.getDevice(deviceTypeId, deviceId), indent=4, sort_keys=True)) 
    # print("\nRetrieving an existing device")  
    # print("Retrieved Device = ", apiClient.getDevice(deviceTypeId, deviceId))

    # var = raw_input("Press Enter to stop")
    
    # print("\nDeleting an existing device")
    # deleted = apiClient.deleteDevice(deviceTypeId, deviceId)
    # print("Device deleted = ", deleted)

  except ibmiotf.APIException as e:
    print(e.httpCode)
    print(str(e))
    sys.exit()

  try:
    cloudOptions = {
      "org": apiOptions["org"],
      "type": deviceTypeId,
      "id": deviceId,
      "auth-method": "token",
      "auth-token": authToken
    } 
    #cloudOptions = json.load(data_file)
    cloudClient = ibmiotf.device.Client(cloudOptions)
  except ibmiotf.ConnectionException  as e:
    print("Execption")

  global mystation
  mystation = str(sys.argv[1])
  pins = [] 

  try:
    
    for x in signal:
      pins.append(mraa.Gpio(x))

    for x in pins:
      x.dir(mraa.DIR_IN)
      x.isr(mraa.EDGE_RISING, onButtonPush, x)
    var = raw_input("Press Enter to stop")
    
    for x in pins:
      x.isrExit()
    deleted = apiClient.deleteDevice(deviceTypeId, deviceId)
  except valueError as e:
    print(e)


if __name__ == '__main__':
    main()
