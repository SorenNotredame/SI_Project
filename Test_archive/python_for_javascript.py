from fastapi import FastAPI
from pydantic import BaseModel
import json
from datetime import datetime

app = FastAPI()

DATA_FILE = "data.json"

# Standaardwaarden als het bestand ontbreekt
default_data = {
    "kwartiervermogen": 3500,         # Wordt elke maand gereset
    "hoogste_kwartiervermogen": 3500, # Wordt alleen gelezen
    "manual_override": {           # Knoppen met booleans
        "Type A": False,
        "Type B": False,
        "Type C": False
    },
    "last_reset": str(datetime.utcnow().month) # Houdt maand bij voor reset
}

# Functie om data te laden
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_data

# Functie om data op te slaan
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Zorg ervoor dat er een JSON-bestand is
if not load_data():
    save_data(default_data)

# Pydantic models
class KwartiervermogenModel(BaseModel):
    kwartiervermogen: int

class ManualOverrideModel(BaseModel):
    Type_A: bool
    Type_B: bool
    Type_C: bool

# 🚀 **GET - Haal het hoogste kwartiervermogen op**
@app.get("/hoogste_kwartiervermogen")
async def get_hoogste_kwartiervermogen():
    data = load_data()
    return {"hoogste_kwartiervermogen": data["hoogste_kwartiervermogen"]}

# 🚀 **POST - Reset het kwartiervermogen elke maand**
@app.post("/reset_kwartiervermogen")
async def reset_kwartiervermogen(model: KwartiervermogenModel):
    data = load_data()
    current_month = str(datetime.utcnow().month)

    # Controleer of het een nieuwe maand is
    if data["last_reset"] != current_month:
        data["kwartiervermogen"] = model.kwartiervermogen
        data["last_reset"] = current_month
        save_data(data)
        return {"message": "Kwartiervermogen gereset", "new_kwartiervermogen": data["kwartiervermogen"]}
    
    return {"message": "Reset niet nodig, zelfde maand", "kwartiervermogen": data["kwartiervermogen"]}

# 🚀 **POST - Stel handmatige overrides in (booleans)**
@app.post("/manual_override")
async def set_manual_override(model: ManualOverrideModel):
    data = load_data()

    # Werk de waarden bij
    data["manual_override"]["Type A"] = model.Type_A
    data["manual_override"]["Type B"] = model.Type_B
    data["manual_override"]["Type C"] = model.Type_C

    save_data(data)
    return {"message": "Manual override bijgewerkt", "new_values": data["manual_override"]}

