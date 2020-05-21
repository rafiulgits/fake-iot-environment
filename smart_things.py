from threading import Thread, Timer
from json import dumps, loads


class SmartThing(Thread):

	def __init__(self, mqttClient, currentStatus, readingInterval):
		Thread.__init__(self)
		self.mqttClient = mqttClient
		self.currentStatus = currentStatus
		self.readingInterval = readingInterval


	def set_incomming_command_topic(self, topic):
		self.incoming_command_topic = topic


	def set_status_publishing_topic(self, topic):
		self.status_publishing_topic = topic


	def start(self):
		self.setup_mqttClient()
		Thread.start(self)


	def setup_mqttClient(self):
		self.mqttClient.subscribe(self.incoming_command_topic)
		self.mqttClient.on_message = self.on_command_execute_request


	def on_command_execute_request(self, client, userdata, message):
		pass


	def run(self):
		self.publish_status(self.currentStatus)
		Timer(self.readingInterval, self.run).start()


	def publish_status(self, payload):
		self.mqttClient.publish(self.status_publishing_topic, dumps(payload).encode('utf8'))



class SmartAC(SmartThing):
	"""
	currentStatus : {
		'status' : 'ON',
		'value' : 23 
	}
	"""
	
	def __init__(self, mqttClient, currentStatus, readingInterval):
		SmartThing.__init__(self, mqttClient, currentStatus, readingInterval)


	def on_command_execute_request(self, client, userdata, message):
		if message.topic != self.incoming_command_topic:
			return
		command = loads(message.payload)
		status = command.get('status')
		value = command.get('value')
		if status is not None and (status == 'ON' or status == 'OFF'):
			self.currentSatus['status'] = status
			
		if value is not None and ( value > 14 or value < 35):
			self.currentStatus['value'] = value

		self.publish_status(self.currentStatus)




class SmartLight(SmartThing):
	"""
	currentStatus : {
		'status' : 'ON'
	}
	"""
	def __init__(self, mqttClient, currentStatus, readingInterval):
		SmartThing.__init__(self, mqttClient, currentStatus, readingInterval)


	def on_command_execute_request(self, client, userdata, message):
		if message.topic != self.incoming_command_topic:
			return
		command = loads(message.payload)
		status = command.get('status')
		if status is not None and (status == 'ON' or status == 'OFF'):
			self.currentStatus['status'] = status
		self.publish_status(self.currentStatus)
