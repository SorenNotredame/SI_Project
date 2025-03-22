import time
from flask import Flask, request, jsonify
from flask_cors import *
import Data_acquisition
from threading import Thread
import peak_predictor
from zigbee2mqtt_class import ZigbeeController

app = Flask(__name__)
CORS(app)
#_manueel == True is dat deze schakelaar aanstaat
#_actief == True is dat de schakeling aan staat dus apparaat is niet actief indien True
values = {'kwartiervermorgen_gewenst': '3500', 'a_manueel': False, 'b_manueel': False, 'c_manueel': False, 'hoogste_kwartiervermogen': '0', 'a_turned_off': False, "b_turned_off": False, 'c_turned_off': False}    

def flask_thread():
    app.run(host="0.0.0.0")
    

def data_thread():
    Data_acquisition.main()

def peak_thread():
    peak = peak_predictor
    while True:
        peak.MAX_PEAK = int(values["kwartiervermorgen_gewenst"])
        peak.main()
        values['hoogste_kwartiervermogen'] = f"{peak.max_average_power:.2f}"
        
        if 'zigbee_controller' not in globals():
            mqtt_broker_address = "localhost"
            zigbee_controller = ZigbeeController(mqtt_broker_address)
            device_id_a = "Type-A"
            zigbee_controller.subscribe_to_device(device_id_a)
            device_id_b = "Type-B"
            zigbee_controller.subscribe_to_device(device_id_b)
            device_id_c = "Type-C"
            zigbee_controller.subscribe_to_device(device_id_c)
        values['a_turned_off'] = peak.ATurnOff
        
        if not values['a_manueel']:
            
            # Check if the device should be turned OFF
            if peak.ATurnOff:
                #!!!!!!dit staat gecomment omdat get_device_state geen waarde geeft als dit werk mag dit worden uncomment en geindent
                """ if zigbee_controller.get_device_state(device_id_a) == "ON": """
                zigbee_controller.turn_off_device(device_id_a)
                print(f"{device_id_a} turned OFF due to peak.ATurnOff")

            # Check if the device should be turned back ON
            else:  # peak.ATurnOff is False
                #!!!!!!!dit staat gecomment omdat get_device_state geen waarde geeft als dit werk mag dit worden uncomment en geindent
                """ if zigbee_controller.get_device_state(device_id_a) == "OFF": """
                zigbee_controller.turn_on_device(device_id_a)
                print(f"{device_id_a} turned ON as peak.ATurnOff is now False")
        #!!!!!!!dit staat gecomment omdat get_device_state geen waarde geeft als dit werk mag dit worden uncomment en geindent
        """ else: 
            if zigbee_controller.get_device_state(device_id_a) == "OFF":
                    zigbee_controller.turn_on_device(device_id_a) """

        values['b_turned_off'] = peak.BTurnOff

        """ if not values['b_manueel']:
            # Check if the device should be turned OFF
            if peak.BTurnOff:
                if zigbee_controller.get_device_state(device_id_b) == "ON":
                    zigbee_controller.turn_off_device(device_id_b)
                    print(f"{device_id_b} turned OFF due to peak.BTurnOff")

            # Check if the device should be turned back ON
            else:  # peak.BTurnOff is False
                if zigbee_controller.get_device_state(device_id_b) == "OFF":
                    zigbee_controller.turn_on_device(device_id_b)
                    print(f"{device_id_b} turned ON as peak.BTurnOff is now False") 
                    
        else: 
            if zigbee_controller.get_device_state(device_id_b) == "OFF":
                zigbee_controller.turn_on_device(device_id_b)"""

        values['c_turned_off'] = peak.CTurnOff

        """ if not values['c_manueel']:
            # Check if the device should be turned OFF
            if peak.CTurnOff:
                if zigbee_controller.get_device_state(device_id_c) == "ON":
                    zigbee_controller.turn_off_device(device_id_c)
                    print(f"{device_id_c} turned OFF due to peak.CTurnOff")

            # Check if the device should be turned back ON
            else:  # peak.CTurnOff is False
                if zigbee_controller.get_device_state(device_id_c) == "OFF":
                    zigbee_controller.turn_on_device(device_id_c)
                    print(f"{device_id_c} turned ON as peak.CTurnOff is now False") 
        else: 
            if zigbee_controller.get_device_state(device_id_c) == "OFF":
                zigbee_controller.turn_on_device(device_id_c)"""

flask_th = Thread(target=flask_thread); flask_th.start()
data_th = Thread(target=data_thread); data_th.start()
peak_th = Thread(target=peak_thread); peak_th.start()

@app.route('/get_values', methods=['GET'])
def get_values():
    return jsonify(values)

# Define an endpoint to receive data
@app.route('/data', methods=['POST'])
def get_data():
    global values
    data = request.get_json()
    print(data)
    values['kwartiervermorgen_gewenst'] = data["kwartiervermorgen_gewenst"]
    values['a_manueel'] = data["a"] 
    values['b_manueel'] = data["b"] 
    values['c_manueel'] = data["c"]
    return "done"

""" flask_th.join()
data_th.join()
peak_th.join()
 """