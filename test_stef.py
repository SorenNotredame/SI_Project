import datetime
import time as t
from zigbee2mqtt_class import ZigbeeController

mqtt_broker_address = "localhost"

zigbee_controller = ZigbeeController(mqtt_broker_address)
zigbee_controller.turn_off_device("Light")
print("Waiting 2 seconds,...")
t.sleep(2)
zigbee_controller.turn_on_device("Light")
print("Waiting 10 seconds,...")
t.sleep(10)
zigbee_controller.get_power_consumption("Light")
t.sleep(10)  # Request power consumption
zigbee_controller.subscribe_to_power_consumption("Light")  # Subscribe to power consumption messages
t.sleep(2)  # Wait for the message to be received
#print(f"Power consumption for {device_id}: {zigbee_controller.power_consumption.get("Light")}W")