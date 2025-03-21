import sys
import time
from datetime import datetime, timedelta
from Data_acquisition import get_latest_consumption_poll, get_current_energy

MAX_PEAK = 1500  # Max piekwaarde in Watt

# Variables to track the state
samples = []
kwartiervermogen_21_7_0 =[]
kwartiervermogen_1_8_0 = []
CTurnOff = False
ATurnOff = False
BTurnOff = False
start_energy = 0
end_energy = 0
average_power = 0

max_average_power = 0

# Calculate the next 15-minute interval
now = datetime.now()
next_cycle = (now + timedelta(minutes=15 - now.minute % 15)).replace(second=0, microsecond=0)
end_of_cycle =  next_cycle - timedelta(seconds=1)

def get_max_average_power():
    """Return the maximum average power recorded."""
    global max_average_power
    return max_average_power

def predict_quarter_peak():
    """Voorspel de piekwaarde voor het kwartier."""
    if not samples:
        return 0 

    elapsed_time = len(samples)  # Aantal verstreken seconden
    remaining_time = 5 * 60 - elapsed_time  # Resterende tijd in seconden

    # Gemiddeld verbruik van de verstreken tijd
    average_elapsed = sum(samples) / len(samples)

    # Actueel verbruik (laatste sample)
    current_consumption = samples[-1]

    # Voorspelling voor het resterende deel van het kwartier
    predicted_remaining = current_consumption * remaining_time

    # Totale voorspelling voor het kwartier
    total_prediction = (average_elapsed * elapsed_time + predicted_remaining) / (5 * 60)
    return total_prediction

def update_device_status_with_prediction(average_power):
    """Update de status van apparaten met de voorspelling."""
    global CTurnOff, ATurnOff, BTurnOff

    # Voorspel de piekwaarde voor het kwartier
    predicted_peak = predict_quarter_peak()

    # Als de voorspelling de piekwaarde niet overschrijdt, mag niets uitvallen
    if predicted_peak < MAX_PEAK:
        CTurnOff = ATurnOff = BTurnOff = False
        return

    # Anders, gebruik de bestaande logica
    if average_power >= 0.8 * MAX_PEAK:
        BTurnOff = True
    elif average_power >= 0.7 * MAX_PEAK:
        ATurnOff = True
    elif average_power >= 0.6 * MAX_PEAK:
        CTurnOff = True
    else:
        CTurnOff = ATurnOff = BTurnOff = False

def calculate_average_power():
    """Bereken het gemiddelde vermogen van de verzamelde samples."""
    if samples:
        return sum(samples) / len(samples)
    return 0

def main():
    global samples, max_average_power, next_cycle, end_of_cycle, kwartiervermogen_1_8_0, kwartiervermogen_21_7_0, start_energy, end_energy,average_power


    try:
        # Check if it's time to start a new cycle
        if datetime.now() >= next_cycle:
            start_energy = get_current_energy()
            print(start_energy)
            print(f"Starting new cycle at {next_cycle.strftime('%H:%M:%S')}")
            samples = []  # Reset samples for the new cycle
            next_cycle = (next_cycle + timedelta(minutes=5)).replace(second=0, microsecond=0)
            end_of_cycle =  next_cycle - timedelta(seconds=1)
        if datetime.now() >= end_of_cycle:
            kwartiervermogen_21_7_0.append(average_power)
            end_energy = get_current_energy()
            kwartiervermogen_1_8_0 = (end_energy - start_energy)*12
            #offset = kwartiervermogen_1_8_0 - kwartiervermogen_21_7_0
            with open("energy_comparison.txt", "a") as file:
                file.write(f"Energy from Meter (kWh): {kwartiervermogen_1_8_0:.4f}\n")
                file.write(f"Energy from Watt Samples (kWh): {kwartiervermogen_21_7_0}\n")

        # Lees en verwerk de vermogenswaarde
        value = get_latest_consumption_poll()
        if value is not None:
            value_in_watts = value
            samples.append(value_in_watts)  # Voeg de waarde in Watt toe aan de lijst
            average_power = calculate_average_power()  # Bereken het gemiddelde vermogen
            if average_power > max_average_power:
                max_average_power = average_power
            update_device_status_with_prediction(average_power)  # Werk de status van de apparaten bij
            # Print het gemiddelde vermogen
            print(f"Current Average Power: {average_power:.2f} W")
            print(f"CTurnOff: {CTurnOff}, ATurnOff: {ATurnOff}, BTurnOff: {BTurnOff}")

            # Bereken en print de geschatte kwartierpiek
            predicted_peak = predict_quarter_peak()
            print(f"Predicted Quarter Peak: {predicted_peak:.2f} W")

        # Sleep for 1 second to simulate sampling every second
        time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")
        sys.exit()  # Forcefully exit the script
    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == '__main__':
    main()