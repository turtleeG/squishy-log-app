import serial
import json
import time
from datetime import datetime

participant_id = input("Enter participant ID (e.g., P03): ").strip()
if not participant_id:
    participant_id = "UNKNOWN"

# connecting to serial (stress ball)
PORT = "/dev/cu.usbmodem1101"  #2nd port on my mac
BAUD = 115200

print("Connecting to device...")
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # let Arduino reset

print("Connected. Reading data...")

data = []  # we store everything here
session_start_time = time.time()

try:
    while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()

        if not line:
            continue

        parts = line.split(",")
        if len(parts) == 3:
            now = time.time()
            msg = {
                "source": parts[0],  # FSR or ANX
                "event": parts[1],   # PRESS, PEAK, RELEASE

                # Arduino time (ms since device boot)
                # "arduino_ms": int(parts[2]),

                # Human-readable time
                "time": datetime.now().strftime("%H:%M:%S"),

                # Seconds since session started
                "relative_time_sec": int(now - session_start_time)
            }
            print(msg)
            data.append(msg)

        else:
            print("Bad line:", line)

except KeyboardInterrupt:
    print("\nStopping and saving...")

ser.close()

# Save data to session.json
date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"{participant_id}_{date_str}.json"

with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {filename}")
