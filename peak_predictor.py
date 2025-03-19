import sys
import time
from datetime import datetime, timedelta
from read_p1 import read_p1_value

MAX_PEAK = 3500  # Max piekwaarde in Watt
SAMPLES_PER_MINUTE = 60  # Aantal samples per minuut
MINUTES = 15  # Aantal minuten voor gemiddelde berekening

# Variables to track the state
samples = []
minute_averages = []
current_cycle_power = 0
CTurnOff = False
ATurnOff = False
BTurnOff = False

def update_device_status():
    global CTurnOff, ATurnOff, BTurnOff, current_cycle_power
    if current_cycle_power >= 0.8 * MAX_PEAK:
        BTurnOff = True
    elif current_cycle_power >= 0.7 * MAX_PEAK:
        ATurnOff = True
    elif current_cycle_power >= 0.6 * MAX_PEAK:
        CTurnOff = True
    else:
        CTurnOff = ATurnOff = BTurnOff = False

def add_sample(value):
    global samples, current_cycle_power
    samples.append(value)
    if len(samples) == SAMPLES_PER_MINUTE:
        minute_average = sum(samples) / len(samples)
        minute_averages.append(minute_average)
        samples.clear()
        current_cycle_power = sum(minute_averages) / len(minute_averages)
        update_device_status()

def get_status():
    return current_cycle_power, CTurnOff, ATurnOff, BTurnOff

def main():
    global samples, minute_averages
    # Calculate the next 15-minute interval
    now = datetime.now()
    next_cycle = (now + timedelta(minutes=15 - now.minute % 15)).replace(second=0, microsecond=0)

    while True:
        try:
            # Check if it's time to start a new cycle
            if datetime.now() >= next_cycle:
                print(f"Starting new cycle at {next_cycle.strftime('%H:%M:%S')}")
                samples = []  # Reset samples for the new cycle
                minute_averages = []  # Reset minute averages for the new cycle
                next_cycle += timedelta(minutes=15)  # Schedule the next cycle

            # Read and process the power value
            value = read_p1_value()
            if value:
                add_sample(value)
                current_cycle_power, CTurnOff, ATurnOff, BTurnOff = get_status()
                print(f"Current Cycle Power: {current_cycle_power} W")
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