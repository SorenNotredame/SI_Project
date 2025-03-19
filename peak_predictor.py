import sys
import time
from datetime import datetime, timedelta
from Data_acquisition import read_p1_value

MAX_PEAK = 3500  # Max piekwaarde in Watt

# Variables to track the state
samples = []
CTurnOff = False
ATurnOff = False
BTurnOff = False

def update_device_status(average_power):
    global CTurnOff, ATurnOff, BTurnOff
    if average_power >= 0.8 * MAX_PEAK:
        BTurnOff = True
    elif average_power >= 0.7 * MAX_PEAK:
        ATurnOff = True
    elif average_power >= 0.6 * MAX_PEAK:
        CTurnOff = True
    else:
        CTurnOff = ATurnOff = BTurnOff = False

def calculate_average_power():
    if samples:
        return sum(samples) / len(samples)
    return 0

def main():
    global samples
    # Calculate the next 15-minute interval
    now = datetime.now()
    next_cycle = (now + timedelta(minutes=15 - now.minute % 15)).replace(second=0, microsecond=0)

    while True:
        try:
            # Check if it's time to start a new cycle
            if datetime.now() >= next_cycle:
                print(f"Starting new cycle at {next_cycle.strftime('%H:%M:%S')}")
                samples = []  # Reset samples for the new cycle
                next_cycle = (next_cycle + timedelta(minutes=15)).replace(second=0, microsecond=0)

            # Lees en verwerk de vermogenswaarde
            value = read_p1_value()
            if value:
                samples.append(value)  # Voeg de waarde toe aan de lijst
                average_power = calculate_average_power()  # Bereken het gemiddelde vermogen
                update_device_status(average_power)  # Werk de status van de apparaten bij
                print(f"Current Average Power: {average_power:.2f} W")
                print(f"CTurnOff: {CTurnOff}, ATurnOff: {ATurnOff}, BTurnOff: {BTurnOff}")

            # Sleep for 1 second to simulate sampling every second
            time.sleep(1)

        except KeyboardInterrupt:
            print("Stopping...")
            sys.exit()  # Forcefully exit the script
        except Exception as e:
            print(f"Something went wrong: {e}")

if __name__ == '__main__':
    main()