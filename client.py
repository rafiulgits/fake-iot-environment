from settings import *
from paho.mqtt import client as mqtt


class MqttClient:
	def __init__(self):
		self.client = mqtt.Client(client_id=MQTT_CLIENT_ID, transport='tcp')
		self.setup()


	def setup(self):
		self.client.on_connect = self.on_connect
		self.client.on_message = self._on_message
		self.client.on_subscribe = self.on_subscribe
		self.client.on_disconnect = self.on_disconnect
		self.message_handlers = {}
		self.client.username_pw_set(MQTT_CLIENT_USERNAME, MQTT_CLIENT_PASSWORD)


	def on_connect(self, client, userdata, flags, result_code):
		print("connected")


	def on_subscribe(self, client, userdata, mid, granted_qos):
		pass


	def _on_message(self, client, userdata, message):
		print("message")
		handler = self.message_handlers.get(message.topic)
		if handler is not None:
			handler(client, message)
		else:
			print("no handler for incomming message")


	def on_disconnect(self, client, userdata, rc):
		print("diconnect")


	def publish(self, topic, payload):
		self.client.publish(topic, payload)


	def subscribe(self, topic):
		self.client.subscribe(topic)


	def add_message_handler(self, topic:str, handler:callable):
		self.message_handlers[topic] = handler


	def start(self):
		self.client.connect(MQTT_BROKER_HOST,MQTT_BROKER_PORT)
		try:
			self.client.loop_forever()
		except KeyboardInterrupt:
			pass


	def start_with_devices(self, devices:list):
		self.client.connect(MQTT_BROKER_HOST,MQTT_BROKER_PORT)
		for device_thread in devices:
			device_thread.daemon = True
			device_thread.start()
		try:
			self.client.loop_forever()
		except KeyboardInterrupt:
			pass
		for device_thread in devices:
			device_thread.join()