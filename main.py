import Data_acquisition
import flask_api
from zigbee2mqtt_class import ZigbeeController
import time as t
import threading

def flask_thread():
    flask_api.app.run(host="0.0.0.0", debug=True)
    t.sleep(10)

def data_acq_thread():
    Data_acquisition.main()


flask_th = threading.Thread(target=flask_thread)
data_acq_th = threading.Thread(target=data_acq_thread)

flask_th.start()
""" data_acq_th.start()

mqtt_broker_address = "localhost"
device_id = "Type-C"


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