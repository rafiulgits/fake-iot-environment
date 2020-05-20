from client import MqttClient

def main():
	client = MqttClient()
	client.start()
	client.client;


if __name__ == '__main__':
	main()
