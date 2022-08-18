from threading import Thread, Timer
from random import randint, random
from json import dumps


class BaseSensor(Thread):

	def __init__(self, readingInterval):
		Thread.__init__(self)
		self.readingInterval = readingInterval


	def run(self):
		self.loop()
		Timer(self.readingInterval, self.run).start()


	def loop(self):
		pass


	def read(self, obj):
		return dumps(obj).encode('utf8')



class DHT22Sensor(BaseSensor):
	"""
	DHT22 sensor read temperature and humidity. Tmperature read in Celsius
	and humidity in percentage
	"""

	def __init__(self, mqttClient, topic, readingInterval):
		BaseSensor.__init__(self, readingInterval)
		self.mqttClient = mqttClient
		self.topic = topic


	def loop(self):
		self.mqttClient.publish(self.topic, self.read())


	def read_temperature(self):
		return randint(26, 35)
	

	def read_humidity(self):
		return randint(80, 90)


	def read(self):
		return BaseSensor.read(self, {
				'temperature' : self.read_temperature(),
				'humidity' : self.read_humidity()
			})




class LM393Sensor(BaseSensor):
	"""
	LM393 sensor read the RPS-rotation per second. This value will convert into
	RPM - rotation per minutes and KMH - kilo meter per hour
	"""
	
	def __init__(self, mqttClient, topic, readingInterval, wheelDiameter):
		BaseSensor.__init__(self, readingInterval)
		self.mqttClient = mqttClient
		self.topic = topic
		self.wheelDiameter = wheelDiameter



	def loop(self):
		self.mqttClient.publish(self.topic, self.read())



	def read(self):
		rpm = self.read_rpm()
		return BaseSensor.read(self, {
				'rpm' : rpm,
				'kmh' : rpm * self.wheelDiameter * 0.001885
			})


	def read_rpm(self):
		return randint(65, 70)*60