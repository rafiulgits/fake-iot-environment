from settings import *
from paho.mqtt import client as mqtt
from sensors import DHT22Sensor, LM393Sensor
from smart_things import SmartLight


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
		pass


	def on_message(self, client, userdata, message):
		print(message.payload)


	def on_disconnect(self, client, userdata, rc):
		print("diconnect")



	def start(self):
		self.client.connect(MQTT_BROKER_HOST,MQTT_BROKER_PORT)
		self.client.subscribe("home/#")
		self.init_sensors()
		self.start_sensors()

		#
		#
		# TODO: common on_message listener for all subscriptions
		#
		#

		# smart light
		smartLight = SmartLight(self.client, {'status' : 'ON'}, 10)
		smartLight.set_incomming_command_topic("home/light/status/change")
		smartLight.set_status_publishing_topic("home/light/status")
		smartLight.daemon = True
		smartLight.start()

		try:
			self.client.loop_forever()
		except KeyboardInterrupt:
			pass
		self.join_sensors()
		smartLight.join()


	def init_sensors(self):
		self.sensors = [
			DHT22Sensor(self.client, "home/temperature-humidity", 8),
			LM393Sensor(self.client, "vehicle/car/velocity", 10, 10)
		]


	def start_sensors(self):
		for sensor in self.sensors:
			sensor.daemon = True
			sensor.start()


	def join_sensors(self):
		for sensor in self.sensors:
			sensor.join()
