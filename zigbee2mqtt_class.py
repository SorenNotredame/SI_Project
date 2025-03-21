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
        self.device_states = {}

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload)
            device_id = msg.topic.split('/')[-1]
            power = payload.get('power')
            state = payload.get('state')
            if power is not None:
                self.power_consumption[device_id] = power
                print(f"Power consumption for {device_id}: {power}W")
            if state is not None:
                self.device_states[device_id] = state
                print(f"State for {device_id}: {state}")
        except json.JSONDecodeError:
            print("Failed to decode JSON payload")

    def turn_on_device(self, device_id):
        self.client.publish(f"zigbee2mqtt/{device_id}/set", json.dumps({"state": "ON"}))
        print(f"Device {device_id} turned on")

    def turn_off_device(self, device_id):
        self.client.publish(f"zigbee2mqtt/{device_id}/set", json.dumps({"state": "OFF"}))
        print(f"Device {device_id} turned off")

    #Test function. Do not use!!
    def update_device(self, device_id):
        self.client.publish(f"zigbee2mqtt/bridge/request/device/ota_update/check", json.dumps({"id": f"{device_id}"}))
        t.sleep(10)
        self.client.publish(f"zigbee2mqtt/bridge/request/device/ota_update/update", json.dumps({"id": f"{device_id}"}))
        print(f"Device {device_id} update check")

    def subscribe_to_device(self, device_id):
        self.client.subscribe(f"zigbee2mqtt/{device_id}")
        print(f"Subscribed to power consumption messages for {device_id}")

    def get_device_state(self, device_id):
        return self.device_states.get(device_id, "Unknown")
    
    def get_device_power(self, device_id):
        return self.power_consumption.get(device_id, "Unknown") 

zigbee_controller = ZigbeeController("localhost")

"""
# Example usage:

mqtt_broker_address = "localhost"
device_id = "Type-C"

zigbee_controller = ZigbeeController(mqtt_broker_address)
zigbee_controller.subscribe_to_device(device_id)
print(f"Current power for {device_id}: {zigbee_controller.get_device_power(device_id)}")
print(f"Current state for {device_id}: {zigbee_controller.get_device_state(device_id)}")
t.sleep(1)
zigbee_controller.turn_on_device(device_id)
t.sleep(30)
print(f"Current power for {device_id}: {zigbee_controller.get_device_power(device_id)}")
print(f"Current state for {device_id}: {zigbee_controller.get_device_state(device_id)}")
t.sleep(1)
t.sleep(5)
print(f"Current power for {device_id}: {zigbee_controller.get_device_power(device_id)}")
print(f"Current state for {device_id}: {zigbee_controller.get_device_state(device_id)}")
t.sleep(1)
print(f"Current power for {device_id}: {zigbee_controller.get_device_power(device_id)}")
print(f"Current state for {device_id}: {zigbee_controller.get_device_state(device_id)}")
t.sleep(1)
print(f"Current power for {device_id}: {zigbee_controller.get_device_power(device_id)}")
print(f"Current state for {device_id}: {zigbee_controller.get_device_state(device_id)}")
t.sleep(1)
print(f"Current power for {device_id}: {zigbee_controller.get_device_power(device_id)}")
print(f"Current state for {device_id}: {zigbee_controller.get_device_state(device_id)}")
t.sleep(1)
zigbee_controller.turn_off_device(device_id)

# Turn on the device and get its state
zigbee_controller.turn_on_device(device_id)
t.sleep(2)  # Wait for the message to be received

print(f"Current state for {device_id}: {zigbee_controller.get_device_state(device_id)}")

# Turn off the device and get its state
zigbee_controller.turn_off_device(device_id)
t.sleep(2)  # Wait for the message to be received
print(f"Current state for {device_id}: {zigbee_controller.get_device_state(device_id)}")
"""        
"""
# Example usage:
mqtt_broker_address = "localhost"
device_id = "Freezer"

zigbee_controller = ZigbeeController(mqtt_broker_address)
zigbee_controller.turn_on_device(device_id)
#zigbee_controller.get_power_consumption(device_id)  # Request power consumption
zigbee_controller.subscribe_to_power_consumption(device_id)  # Subscribe to power consumption messages
x = 0
while x < 5:

    # Access the power consumption value
    t.sleep(10)  # Wait for the message to be received
    x += 1
    print(f"Power consumption for {device_id}: {zigbee_controller.power_consumption.get(device_id)}W")
    print(x)
zigbee_controller.turn_off_device(device_id)
"""
