import json
import paho.mqtt.client as mqtt
import time as t


class ZigbeeController:
    def __init__(self, mqtt_broker, mqtt_port=1883):
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.client.loop_start()
        self.power_consumption = {}

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload)
            device_id = msg.topic.split('/')[-1]
            power = payload.get('power')
            if power is not None:
                self.power_consumption[device_id] = power
                print(f"Power consumption for {device_id}: {power}W")
        except json.JSONDecodeError:
            print("Failed to decode JSON payload")

    def turn_on_device(self, device_id):
        self.client.publish(f"zigbee2mqtt/{device_id}/set", json.dumps({"state": "ON"}))
        print(f"Device {device_id} turned on")

    def turn_off_device(self, device_id):
        self.client.publish(f"zigbee2mqtt/{device_id}/set", json.dumps({"state": "OFF"}))
        print(f"Device {device_id} turned off")

    def get_power_consumption(self, device_id):
        self.client.publish(f"zigbee2mqtt/{device_id}/get", json.dumps({"power": ""}))
        print(f"Requested power consumption for {device_id}")

    def subscribe_to_power_consumption(self, device_id):
        self.client.subscribe(f"zigbee2mqtt/{device_id}")
        print(f"Subscribed to power consumption messages for {device_id}")

# Example usage:
mqtt_broker_address = "localhost"
device_id = "Light"

zigbee_controller = ZigbeeController(mqtt_broker_address)
zigbee_controller.turn_on_device(device_id)
zigbee_controller.get_power_consumption(device_id)  # Request power consumption
zigbee_controller.subscribe_to_power_consumption(device_id)  # Subscribe to power consumption messages
while True:

    # Access the power consumption value
    t.sleep(10)  # Wait for the message to be received
    print(f"Power consumption for {device_id}: {zigbee_controller.power_consumption.get(device_id)}W")