import paho.mqtt.client as paho
import time
import datetime
import json
import sys

speed_car= 20
client = paho.Client()
config= {
"username": "iot_user",
"password" : "EcE592net!",
"broker" : "10.139.68.190",
"publish-topic" : "MDV" ,
"subscribe-topic" : "CSIE",
"port": 1883
}

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
    client.subscribe(config["subscribe-topic"] + "/" + str(vehicle_id) ,1)	
	
def on_subscribe(client,userdata, mid, granted_qos):
    print("Subscribed: "+str(granted_qos))

def on_message(client, userdata, msg):
    global vehicle_id,speed_car	
    s=json.loads(msg.payload)
    ts = time.time();
    st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')	
    print("Signal received:"+str(s["d"]["signal"]) + " at " + str(s["d"]["timestamp"]))
    if s["d"]["signal"] == "Red":
	speed_car = speed_car-5
    else:
	speed_car=20
    #msg = json.JSONEncoder().encode({"d":{"id":i,"timestamp":st,"signal":s["d"]["signal"],"speed":speed_car}})
    msg = json.dumps({"d":{"id":vehicle_id,"timestamp":st,"signal":s["d"]["signal"],"speed":speed_car}})
    client.publish(config["publish-topic"] + "/" + str(vehicle_id), payload=msg, qos=1, retain=False)	

def on_publish(client, userdata, mid):
    print("Message published")

def main():
    vehicle_id = int(sys.argv[1])
    global vehicle_id
    client.on_subscribe = on_subscribe
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.username_pw_set(config["username"],config["password"])
    client.connect(config["broker"],config["port"])

    client.loop_forever()

if __name__ == '__main__':
    main()