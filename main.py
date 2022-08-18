from client import MqttClient
from systems import BaseSystem, HomeAutomationSystem

class FakeSystems:

	def __init__(self):
		self.systems = []


	def add_system(self, system):
		self.systems.append(system)


	def get_all_systems_devices(self):
		devices = []
		for system in self.systems:
			devices = devices + system.get_devices()
		return devices


def main():
	client = MqttClient()
	fakeSystems = FakeSystems()
	fakeSystems.add_system(HomeAutomationSystem(client))
	devices = fakeSystems.get_all_systems_devices()
	client.start_with_devices(devices)

if __name__ == '__main__':
	main()
