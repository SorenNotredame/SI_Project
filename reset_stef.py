import time
from zigbee2mqtt_class import ZigbeeController


mqtt_broker_address = "localhost"
device_list = ["Type-A", "Type-B","Type-C"]

zigbee_controller = ZigbeeController(mqtt_broker_address)
device_id_a = "Type-A"
device_id_b = "Type-B"
device_id_c = "Type-C"
for device in device_list:
    zigbee_controller.subscribe_to_device(device)
zigbee_controller.turn_off_device(device_id_a)
zigbee_controller.turn_on_device(device_id_b)
zigbee_controller.turn_off_device(device_id_c)
timer = True

time.sleep(5)

for device in device_list:
    zigbee_controller.get_device_state(device)
    zigbee_controller.get_device_power(device)


