from settings import *
from paho.mqtt import client as mqtt
from sensors import DHT22Sensor


class MqttClient:
	def __init__(self):
		self.client = mqtt.Client(client_id=MQTT_CLIENT_ID, transport='tcp')
		self.setup()


	def setup(self):
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.on_subscribe = self.on_subscribe
		self.client.on_disconnect = self.on_disconnect
		self.client.username_pw_set(MQTT_CLIENT_USERNAME, MQTT_CLIENT_PASSWORD)


	def on_connect(self, client, userdata, flags, result_code):
		print("connected")
		

	def on_subscribe(self, client, userdata, mid, granted_qos):
		print(mid)
		print(userdata)
		print(granted_qos)


	def on_message(self, client, userdata, message):
		print(message)
		print(userdata)


	def on_disconnect(self, client, userdata, rc):
		print("diconnect")


	def start(self):
		self.client.connect(MQTT_BROKER_HOST,MQTT_BROKER_PORT, 3)
		dht22_sensor = DHT22Sensor(self.client, "home/temperature-humidity", 10)
		dht22_sensor.start()
		self.client.loop_start()
		dht22_sensor.join()
