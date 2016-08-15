import mraa, time, sys
import ibmiotf.device

''' List of stations (We should make a database to put list of stations)'''
stations = {
  "EB1" : 14, 
  "EB2" : 36,
  "HuntLibrary" : 48
}

''' Connection establishment to IBM Bluemix Cloud'''
cloudTopic = "status"

try:
  cloudOptions = {
    "org": "i5nag4",
    "type": "edison",
    "id": "infrastructure-1",
    "auth-method": "token",
    "auth-token": "EcE592net"
  }
  cloudClient = ibmiotf.device.Client(cloudOptions)
except ibmiotf.ConnectionException  as e:
  print("Execption")

''' When at a station, We press the appropriate button, which will send the 
message to IBM Blumix for the device location'''
def onButtonPush(gpio):
  if gpio.read() == 1:
    mystation = ""
    for key, value in stations.iteritems():
      if value == gpio.getPin(False):
        mystation = str(key)
    #print("My station is: " + mystation)
    data = {
      "d" : {
        "Station" : mystation
      }
    }
    cloudClient.publishEvent("status", "json", data)

def main():

  cloudClient.connect()

  pins = [] 

  try:
    for station in stations:
      pins.append(mraa.Gpio(stations[station]))

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