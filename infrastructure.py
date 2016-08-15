import json
import random, time, datetime
import paho.mqtt.client as paho

config = {
	"username" : "iot_user",
	"password" : "EcE592net!",
	"broker"   : "10.139.68.190", #Mqtt broker to connect to
	"publish_topic" : "CSIE/", #control signal from infrastructure element
	"subscribe_topic" : "MDV/#", #Measurement data from Vehical 
	"port"		: 1883,
	"logfile" : "infrastructure.log"
}

number_of_cars = 4
control_signal = ['Green', 'Yellow', 'Red'] #signal sent to the vehicles
logfile = open(config["logfile"], "wa")


def on_connect(client, userdata, flags, rc):
    print("Connected to broker")
    client.subscribe(config["subscribe_topic"])
    #print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    logfile.write(msg.payload + "\n")
    logfile.flush()

def on_disconnect(client, userdata, rc):
	if rc != 0:
		print("Unexpected disconnection.")
		close(logfile)

def main():

	#create a client
	client = paho.Client()

	#define callbacks
	client.on_connect = on_connect
	client.on_message = on_message
	client.on_disconnect = on_disconnect

	#Set the username and password and connect to the broker
	client.username_pw_set(config["username"], config["password"])
	client.connect(config["broker"], config["port"] )

	client.loop_start()

	while True:
		for i in range(number_of_cars):
			ts = time.time()
			st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%s')
			data = {"d" : {"timestamp": st, "signal" : random.choice(control_signal)}}
			data = json.dumps(data)
			(rc, mid) = client.publish(config["publish_topic"] + str(i+1), data)
			print("Published a message")
		time.sleep(5)

if __name__ == '__main__':
	main()