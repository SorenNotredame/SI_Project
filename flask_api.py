import time
from flask import Flask, request, jsonify
from flask_cors import *
import Data_acquisition
from threading import Thread
import peak_predictor

app = Flask(__name__)
CORS(app)

values = {'kwartiervermorgen_gewenst': '3500', 'a_manueel': False, 'b_manueel': True, 'c_manueel': True, 'hoogste_kwartiervermogen': '3500', 'a_actief': True, "b_actief": True, 'c_actief': True}    

def flask_thread():
    app.run(host="0.0.0.0")

def data_thread():
    Data_acquisition.main()

def peak_thread():
    peak = peak_predictor
    while True:
        peak.main()
        values['hoogste_kwartiervermogen'] = f"{peak.max_average_power:.2f}"
        values['a_actief'] = peak.ATurnOff
        values['b_actief'] = peak.BTurnOff
        values['c_actief'] = peak.CTurnOff


flask_th  = Thread(target=flask_thread); flask_th.start()
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

flask_th.join()
data_th.join()
peak_th.join()
