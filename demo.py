import sys
import ibmiotf.api
import ibmiotf
import logging
import json

''' List of stations (We should make a database to put list of stations)'''
stations = {
  "EB1" : [14, 0],
  "EB2" : [36, 0],
  "Hunt" : [48, 0]
}


''' Connection establishment to IBM Bluemix Cloud'''
cloudTopic = "trafficSignal"

''' When at a station, We press the appropriate button, which will send the 
message to IBM Blumix for the device location'''
def onButtonPush(gpio):
  if gpio.read() == 1:
    mystation = ""
    status = ""
    for key, value in stations.iteritems():
      if value[0] == gpio.getPin(False):
        mystation = str(key)
    stations[mystation][1] += 1
    if stations[mystation][1] % 2 == 0:
      status = "red"
    else:
      status = "green"
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

    deviceId = "testDevice"
    authToken = "EcE592net"
    
    print("\nRegistering a new device") 
    print("Registered Device = ", apiClient.registerDevice(deviceTypeId, deviceId, authToken))
    
    # print("\nRetrieving an existing device")  
    # print("Retrieved Device = ", apiClient.getDevice(deviceTypeId, deviceId))

    # var = raw_input("Press Enter to stop")
    
    # print("\nDeleting an existing device")
    # deleted = apiClient.deleteDevice(deviceTypeId, deviceId)
    # print("Device deleted = ", deleted)

  except ibmiotf.IoTFCReSTException as e:
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

  pins = [] 

  try:
    for station in stations:
      pins.append(mraa.Gpio(stations[station][0]))

    for x in pins:
      x.dir(mraa.DIR_IN)
      x.isr(mraa.EDGE_RISING, onButtonPush, x)
    var = raw_input("Press Enter to stop")
    
    for x in pins:
      x.isrExit()
  except valueError as e:
    print(e)


if __name__ == '__main__':
    main()