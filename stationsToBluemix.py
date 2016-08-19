import mraa, time, sys
import ibmiotf.device

''' List of stations (We should make a database to put list of stations)'''
stations = {
  "EB1" : [14, 0],
  "EB2" : [36, 0],
  "Hunt" : [48, 0]
}


''' Connection establishment to IBM Bluemix Cloud'''
cloudTopic = "trafficSignal"

try:
  cloudOptions = {
    "org": "y8ck3c",
    "type": "vehicle",
    "id": "ABC",
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

  cloudClient.connect()

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