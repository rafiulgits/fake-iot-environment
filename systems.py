from sensors import LM393Sensor, DHT22Sensor
from smart_things import SmartAC, SmartLight
from client import MqttClient


class BaseSystem:

	def __init__(self):
		self.devices = []
		self.setup()


	def setup(self):
		pass


	def get_devices(self) -> list:
		return self.devices



class HomeAutomationSystem(BaseSystem):

	def __init__(self, mqttClient:MqttClient):
		self.mqttClient = mqttClient
		BaseSystem.__init__(self)


	def setup(self):
		self.setup_temperature_sensor()
		self.setup_living_room_ac()
		self.setup_living_room_light()


	def setup_temperature_sensor(self):
		dht22 = DHT22Sensor(self.mqttClient, "home/temperature-humidity", 5)
		self.devices.append(dht22)


	def setup_living_room_ac(self):
		smartAc = SmartAC(self.mqttClient, {'status': 'ON', 'value' : 19}, 7)
		smartAc.set_incomming_command_topic("home/living-room/ac/status/change")
		smartAc.set_status_publishing_topic("home/living-room/ac/status")
		self.devices.append(smartAc)


	def setup_living_room_light(self):
		smartLight = SmartLight(self.mqttClient, {'status' : 'ON'}, 10) 
		smartLight.set_incomming_command_topic("home/living-room/light/status/change")
		smartLight.set_status_publishing_topic("home/living-room/light/status")
		self.devices.append(smartLight)



class SupplyChainManagementSystem(BaseSystem):
	pass