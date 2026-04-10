import csv
import os
import random
import time
from datetime import datetime

FILE_NAME = "live_signals.csv"

# Base Location (Groom Lake / Area 51, Nevada)
BASE_LAT = 37.2350
BASE_LON = -115.8111

def generate_friendly():
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "frequency_mhz": round(random.uniform(225.0, 400.0), 3),
        "bandwidth_khz": random.choice([12.5, 25.0, 250.0]),
        "power_dbm": round(random.uniform(-85.0, -50.0), 1),
        "snr_db": round(random.uniform(15.0, 35.0), 1),
        "modulation": random.choice(["AM", "FM", "FSK", "PSK"]),
        "latitude": BASE_LAT + random.uniform(-0.1, 0.1),
        "longitude": BASE_LON + random.uniform(-0.1, 0.1),
        "distance_km": round(random.uniform(2.0, 15.0), 1),
        "bearing_deg": round(random.uniform(0, 360), 1),
        "doppler_shift_hz": round(random.uniform(-15.0, 15.0), 1)
    }

def generate_unknown():
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "frequency_mhz": round(random.choice([random.uniform(30.0, 88.0), random.uniform(900.0, 1200.0)]), 3),
        "bandwidth_khz": random.choice([25.0, 100.0, 1000.0]),
        "power_dbm": round(random.uniform(-105.0, -75.0), 1),
        "snr_db": round(random.uniform(3.0, 12.0), 1),
        "modulation": random.choice(["QAM16", "OFDM", "UNKNOWN"]),
        "latitude": BASE_LAT + random.uniform(-0.6, 0.6),
        "longitude": BASE_LON + random.uniform(-0.6, 0.6),
        "distance_km": round(random.uniform(20.0, 80.0), 1),
        "bearing_deg": round(random.uniform(0, 360), 1),
        "doppler_shift_hz": round(random.uniform(-250.0, 250.0), 1)
    }

def generate_hostile():
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "frequency_mhz": round(random.choice([random.uniform(8500.0, 10500.0), random.uniform(1200.0, 1400.0)]), 3),
        "bandwidth_khz": random.choice([5000.0, 15000.0, 20000.0]),
        "power_dbm": round(random.uniform(-115.0, -95.0), 1),
        "snr_db": round(random.uniform(-2.0, 5.0), 1),
        "modulation": random.choice(["PULSED", "FMCW", "SPREAD-SPECTRUM"]),
        "latitude": BASE_LAT + random.uniform(-1.5, 1.5),
        "longitude": BASE_LON + random.uniform(-1.5, 1.5),
        "distance_km": round(random.uniform(80.0, 250.0), 1),
        "bearing_deg": round(random.uniform(0, 360), 1),
        "doppler_shift_hz": round(random.uniform(1000.0, 2500.0) * random.choice([1, -1]), 1)
    }

def choose_signal():
    r = random.random()
    if r < 0.60:
        return generate_friendly()
    elif r < 0.85:
        return generate_unknown()
    return generate_hostile()

def ensure_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as f:
            write_headers(f)
    else:
        # Check if the right headers exist, if not overwrite
        with open(FILE_NAME, "r") as f:
            line = f.readline()
        if "frequency_mhz" not in line:
            with open(FILE_NAME, "w", newline="") as f:
                write_headers(f)

def write_headers(f):
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "timestamp", "frequency_mhz", "bandwidth_khz", "power_dbm",
            "snr_db", "modulation", "latitude", "longitude",
            "distance_km", "bearing_deg", "doppler_shift_hz"
        ]
    )
    writer.writeheader()

def append_signal(signal):
    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=signal.keys())
        writer.writerow(signal)

def main():
    ensure_file()
    print("Live SDR Feed Simulator - Initializing Data Hooks...")
    time.sleep(1)
    print("Locked onto orbital and ground vectors. Awaiting intercepts.")
    while True:
        signal = choose_signal()
        append_signal(signal)
        print(f"[{signal['timestamp']}] DETECTED: {signal['frequency_mhz']} MHz | Pw: {signal['power_dbm']} dBm | Mod: {signal['modulation']}")
        time.sleep(random.uniform(0.2, 1.5))

if __name__ == "__main__":
    main()