import csv
import os
import random
import time
import math
import numpy as np
from datetime import datetime

FILE_NAME = "live_signals.csv"

# Base Location (Groom Lake / Area 51, Nevada)
BASE_LAT = 37.2350
BASE_LON = -115.8111
SPEED_OF_LIGHT = 299792458 # m/s

class Emitter:
    def __init__(self, category):
        self.id = f"TX-{random.randint(1000, 9999)}"
        self.category = category # "Friendly", "Unknown", "Hostile"
        self.lat = BASE_LAT + random.uniform(-0.5, 0.5)
        self.lon = BASE_LON + random.uniform(-0.5, 0.5)
        self.alt = random.uniform(100, 10000) # Meters
        self.velocity = random.uniform(50, 800) # m/s (approx Mach 0.15 to 2.3)
        self.heading = random.uniform(0, 360) # Degrees
        
        if category == "Friendly":
            self.freq = round(random.uniform(225.0, 400.0), 3)
            self.bw = random.choice([12.5, 25.0, 250.0])
            self.mod = random.choice(["AM", "FM", "FSK", "PSK"])
            self.tx_power = 40 # dBm (10 Watts)
        elif category == "Unknown":
            self.freq = round(random.choice([random.uniform(30.0, 88.0), random.uniform(900.0, 1200.0)]), 3)
            self.bw = random.choice([25.0, 100.0, 1000.0])
            self.mod = random.choice(["QAM16", "OFDM", "UNKNOWN"])
            self.tx_power = 45 # dBm
        else: # Hostile
            self.freq = round(random.choice([random.uniform(8500.0, 10500.0), random.uniform(1200.0, 1400.0)]), 3)
            self.bw = random.choice([5000.0, 15000.0, 20000.0])
            self.mod = random.choice(["PULSED", "FMCW", "SPREAD-SPECTRUM"])
            self.tx_power = 60 # dBm (High power radar)

    def update_position(self, dt):
        # Very simplified flat-earth movement for simulation
        # 1 deg lat approx 111km, 1 deg lon approx 111km * cos(lat)
        dist_m = self.velocity * dt
        heading_rad = math.radians(self.heading)
        
        d_lat = (dist_m * math.cos(heading_rad)) / 111000
        d_lon = (dist_m * math.sin(heading_rad)) / (111000 * math.cos(math.radians(self.lat)))
        
        self.lat += d_lat
        self.lon += d_lon
        
        # Jitter heading slightly
        self.heading += random.uniform(-2, 2)

    def calculate_rf_props(self):
        # Calculate distance to base
        dist_km = self.haversine(BASE_LAT, BASE_LON, self.lat, self.lon)
        bearing = self.calculate_bearing(BASE_LAT, BASE_LON, self.lat, self.lon)
        
        # Free Space Path Loss: FSPL(dB) = 20log10(d) + 20log10(f) + 32.44
        # (d in km, f in MHz)
        fspl = 20 * math.log10(max(dist_km, 0.1)) + 20 * math.log10(self.freq) + 32.44
        rx_power = self.tx_power - fspl + random.uniform(-2, 2) # Adding fading/multipath jitter
        
        # Realistic SNR based on noise floor (~ -120 dBm for 1MHz BW)
        noise_floor = -120 + 10 * math.log10(self.bw / 1000)
        snr = rx_power - noise_floor
        
        # Doppler Shift: fd = (v * cos(theta) / c) * ft
        # Simplification: Assume radial velocity is just a projection of the main velocity
        # (For simulation, we'll randomize the aspect angle theta)
        theta = random.uniform(0, math.pi)
        doppler = (self.velocity * math.cos(theta) / SPEED_OF_LIGHT) * (self.freq * 1e6)
        
        return {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "frequency_mhz": self.freq,
            "bandwidth_khz": self.bw,
            "power_dbm": round(rx_power, 1),
            "snr_db": round(snr, 1),
            "modulation": self.mod,
            "latitude": round(self.lat, 6),
            "longitude": round(self.lon, 6),
            "distance_km": round(dist_km, 1),
            "bearing_deg": round(bearing, 1),
            "doppler_shift_hz": round(doppler, 1),
            "velocity_ms": round(self.velocity, 1),
            "altitude_m": round(self.alt, 0)
        }

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371.0 # Radius of earth in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def calculate_bearing(self, lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlon = lon2 - lon1
        y = math.sin(dlon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
        return (math.degrees(math.atan2(y, x)) + 360) % 360

def main():
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME) # Start fresh for the new physics model
    
    emitters = []
    # Initialize some starting emitters
    for _ in range(3): emitters.append(Emitter("Friendly"))
    for _ in range(2): emitters.append(Emitter("Unknown"))
    for _ in range(2): emitters.append(Emitter("Hostile"))
    
    print("Locked onto orbital and ground vectors. Physics Engine: ACTIVE.")
    
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "frequency_mhz", "bandwidth_khz", "power_dbm",
            "snr_db", "modulation", "latitude", "longitude",
            "distance_km", "bearing_deg", "doppler_shift_hz", "velocity_ms", "altitude_m"
        ])
        writer.writeheader()

    last_time = time.time()
    try:
        while True:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Choose a random emitter to "pulse" or transmit
            e = random.choice(emitters)
            e.update_position(dt)
            data = e.calculate_rf_props()
            
            with open(FILE_NAME, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                writer.writerow(data)
            
            print(f"[{data['timestamp']}] PHYSICS-EMISSION: {data['frequency_mhz']} MHz | Dist: {data['distance_km']} km | Pw: {data['power_dbm']} dBm")
            
            # Chance to spawn new or despawn emitters
            if random.random() < 0.05 and len(emitters) < 15:
                emitters.append(Emitter(random.choice(["Friendly", "Unknown", "Hostile"])))
            
            time.sleep(random.uniform(0.1, 0.4))
    except KeyboardInterrupt:
        print("\nSurveillance Terminated.")

if __name__ == "__main__":
    main()