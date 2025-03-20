from flask import Flask, request, jsonify
from flask_cors import *

app = Flask(__name__)
CORS(app)

values = {'kwartiervermorgen_gewenst': '3500', 'a': False, 'b': True, 'c': True}

@app.route('/get_values', methods=['GET'])
def get_values():
    return jsonify(values)

# Define an endpoint to receive data
@app.route('/data', methods=['POST'])
def get_data():
    global values
    data = request.get_json()
    print(data)
    values = {'kwartiervermorgen_gewenst': data["kwartiervermorgen_gewenst"], 
              'a': data["a"], 
              'b': data["b"], 
              'c': data["c"]}
    return "done"
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)