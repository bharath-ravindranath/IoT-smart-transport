import mraa, time, sys
import ibmiotf.device

''' List of stations (We should make a database to put list of stations)'''
signal = {
  14: "red",
  36: "yellow",
  48: "green"
}


''' Connection establishment to IBM Bluemix Cloud'''
cloudTopic = "trafficSignal"

try:
  cloudOptions = {
    "org": "gezj6x",
    "type": "Signal",
    "id": "EcoPRTSignal",
    "auth-method": "token",
    "auth-token": "2p9azAgJiTxhUbXMCF"
  }
  cloudClient = ibmiotf.device.Client(cloudOptions)
except ibmiotf.ConnectionException  as e:
  print("Execption")

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

  cloudClient.connect()
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
  except valueError as e:
    print(e)

if __name__ == '__main__':
  main()
