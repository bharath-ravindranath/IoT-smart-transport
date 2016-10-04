import json, random, time, datetime
import ast
import paho.mqtt.client as paho
import ibmiotf.device

infraOptions = {
  "username" : "iot_user",
  "password" : "EcE592net!",
  "broker"   : "192.168.1.241", #Mqtt broker to connect to
  "sub_topic" : "#", #control signal from infrastructure element
  "port"    : 1883,
}

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


def on_connect(client, userdata, flags, rc):
    #print("Connected to broker")
    client.subscribe(infraOptions["sub_topic"])

def on_message(client, userdata, msg):
    data = ast.literal_eval(str(msg.payload))
    data['d']['topic'] = str(msg.topic)
    cloudClient.publishEvent("status", "json", data)


def main():
  client = paho.Client()

  #define callbacks
  client.on_connect = on_connect
  client.on_message = on_message

  #Set the username and password and connect to the broker
  client.username_pw_set(infraOptions["username"], infraOptions["password"])
  client.connect(infraOptions["broker"], infraOptions["port"] )

  cloudClient.connect()
  client.loop_forever()


if __name__ == '__main__':
  main()