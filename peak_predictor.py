from read_p1 import read_p1_value

MAX_PEAK = 3500  # Max piekwaarde in Watt
SAMPLES_PER_MINUTE = 60  # Aantal samples per minuut
MINUTES = 15  # Aantal minuten voor gemiddelde berekening

# Variables to track the state
samples = []
average_power = 0
CTurnOff = False
ATurnOff = False
BTurnOff = False

def update_device_status():
    global CTurnOff, ATurnOff, BTurnOff, average_power
    if average_power >= 0.8 * MAX_PEAK:
        BTurnOff = True
    elif average_power >= 0.7 * MAX_PEAK:
        ATurnOff = True
    elif average_power >= 0.6 * MAX_PEAK:
        CTurnOff = True
    else:
        CTurnOff = ATurnOff = BTurnOff = False

def add_sample(value):
    global samples, average_power
    samples.append(value)
    if len(samples) > SAMPLES_PER_MINUTE * MINUTES:
        samples.pop(0)
    average_power = sum(samples) / len(samples)
    update_device_status()

def get_status():
    return average_power, CTurnOff, ATurnOff, BTurnOff

def main():
    while True:
        try:
            value = read_p1_value()
            if value:
                add_sample(value)
                average_power, CTurnOff, ATurnOff, BTurnOff = get_status()
                print(f"Average Power: {average_power} W")
                print(f"CTurnOff: {CTurnOff}, ATurnOff: {ATurnOff}, BTurnOff: {BTurnOff}")
        except KeyboardInterrupt:
            print("Stopping...")
            break
        except Exception as e:
            print(f"Something went wrong: {e}")

if __name__ == '__main__':
    main()