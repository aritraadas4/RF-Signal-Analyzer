import hashlib
import random

def calculate_threat_score(signal):
    """
    Weighted Threat Scoring Model:
    - Kinematics (Velocity/Doppler): 30%
    - Signal Strength/Proximity: 25%
    - Modulation/Spectral Signature: 25%
    - Frequency Band (X-Band/Fire Control): 20%
    """
    score = 0.0

    power = float(signal.get("power_dbm", -120))
    snr = float(signal.get("snr_db", 0))
    frequency = float(signal.get("frequency_mhz", 0))
    bandwidth = float(signal.get("bandwidth_khz", 0))
    modulation = str(signal.get("modulation", "")).strip()
    distance = float(signal.get("distance_km", 100))
    doppler = abs(float(signal.get("doppler_shift_hz", 0)))
    velocity = float(signal.get("velocity_ms", 0))
    altitude = float(signal.get("altitude_m", 0))

    # 1. KINEMATICS (Max 30 pts)
    # High velocity (>300m/s / Mach 1) and high doppler are aggressive
    kin_score = min((velocity / 800) * 20, 20) + min((doppler / 2000) * 10, 10)
    score += kin_score

    # 2. PROXIMITY & POWER (Max 25 pts)
    # Strong power at range is a massive emitter (Radar)
    prox_score = 0
    if distance < 50: prox_score += 10
    if power > -70: prox_score += 15
    score += min(prox_score, 25)

    # 3. SPECTRAL SIGNATURE (Max 25 pts)
    sig_score = 0
    if modulation in ["PULSED", "FMCW"]: sig_score += 20 # Radar
    elif modulation == "SPREAD-SPECTRUM": sig_score += 15 # Military C2
    elif bandwidth > 10000: sig_score += 10 # Wideband / Jamming
    score += sig_score

    # 4. FREQUENCY BAND (Max 20 pts)
    band_score = 0
    if 8500 <= frequency <= 10500: band_score += 20 # X-Band Fire Control
    elif 1200 <= frequency <= 1400: band_score += 10 # L-Band Search
    score += band_score

    return min(int(score), 100)


def classify_signal(score):
    if score < 35:
        return "Friendly"
    elif score < 65:
        return "Unknown"
    return "Hostile"


def anomaly_reason(signal):
    reasons = []

    power = float(signal.get("power_dbm", -120))
    frequency = float(signal.get("frequency_mhz", 0))
    bandwidth = float(signal.get("bandwidth_khz", 0))
    modulation = str(signal.get("modulation", "")).strip()
    velocity = float(signal.get("velocity_ms", 0))
    doppler = abs(float(signal.get("doppler_shift_hz", 0)))

    if velocity > 343: # Speed of sound
        reasons.append(f"Supersonic kinematic trace ({round(velocity/343, 1)} Mach)")
    elif velocity > 150:
        reasons.append("High-speed airborne vector")
        
    if bandwidth >= 15000:
        reasons.append("Ultra-wideband saturation")

    if modulation in ["PULSED", "FMCW"]:
        reasons.append("Active Combat Radar pulses")
    elif modulation == "SPREAD-SPECTRUM":
        reasons.append("Frequency-hopping evasion detected")

    if 8500 <= frequency <= 10500:
        reasons.append("X-Band illumination (Precision Lock)")

    if not reasons:
        return "Stable communication pattern"

    return ", ".join(reasons)

def generate_ai_anomaly_explanation(anomaly_string):
    if anomaly_string == "Stable communication pattern":
        return "The emitter is transmitting over a stable carrier wave with no immediate signs of hostile modulation, jumping, or aggressive kinematics. Recommend standard logging."
        
    explanation = "Tactical AI Analysis: "
    if "Supersonic" in anomaly_string:
        explanation += "Target is exceeding the sound barrier; likely a missile or interceptor aircraft. "
    if "Airborne" in anomaly_string:
        explanation += "Kinematics suggest a fast-moving aerial platform. "
    if "Ultra-wideband" in anomaly_string:
        explanation += "Signal bandwidth indicates high-density data or broadband jamming. "
    if "Radar pulses" in anomaly_string:
        explanation += "Emitter is actively scanning for targets using pulsed energy. "
    if "Frequency-hopping" in anomaly_string:
        explanation += "Signal is using FHSS to evade electronic counter-measures. "
    if "X-Band" in anomaly_string:
        explanation += "Precision fire-control radar detected! Target is likely preparing for engagement. "
        
    return explanation.strip()

def generate_global_ai_analysis(active_tracks):
    if active_tracks is None or active_tracks.empty:
        return "The local aerospace environment is currently clear. No anomalous emissions detected."
        
    hots = active_tracks[active_tracks["Classification"] == "Hostile"]
    
    analysis = f"Currently tracking {len(active_tracks)} live signals with {len(hots)} confirmed as hostile. "
    
    if not hots.empty:
        highest = hots.sort_values(by="Threat Score", ascending=False).iloc[0]
        mach = round(highest.get('velocity_ms', 0) / 343, 1)
        analysis += f"PRIMARY THREAT: {highest['Platform ID']} ({highest['Threat Score']}%) at {highest['distance_km']}km. Tracking at {mach} Mach. "
    else:
        analysis += "No immediate hostile intercept protocols recommended. "
        
    all_anomalies = []
    for _, track in active_tracks.iterrows():
        a_str = anomaly_reason(track)
        if a_str != "Stable communication pattern":
            all_anomalies.extend(a_str.split(", "))
            
    unique_anomalies = list(set(all_anomalies))
    if unique_anomalies:
        analysis += f"Signatures: {', '.join(unique_anomalies[:3])}."
        
    return analysis




def recommendation(label, score):
    if label == "Friendly":
        return "Maintain routine surveillance"
    elif label == "Unknown":
        if score >= 55:
            return "Deploy ISR drone for visual verification"
        return "Monitor telemetry for pattern change"
    else:
        if score >= 80:
            return "AUTHORIZE KINETIC ENGAGEMENT / C-RAM ACTIVE"
        return "Lock Fire Control, Alert CAP (Combat Air Patrol)"

def calculate_confidence(signal):
    snr = float(signal.get("snr_db", 0))
    distance = float(signal.get("distance_km", 100))
    
    # Confidence increases with SNR and proximity
    base_conf = 40.0
    base_conf += min(snr * 2.0, 50.0)
    
    if distance > 150:
        base_conf -= (distance - 150) * 0.1
        
    return min(max(base_conf, 10.0), 99.9)

def identify_platform(signal):
    freq = float(signal.get("frequency_mhz", 0))
    mod = str(signal.get("modulation", "")).strip()
    bw = float(signal.get("bandwidth_khz", 0))
    vel = float(signal.get("velocity_ms", 0))
    
    if 225 <= freq <= 400:
        return "Military Airborne Link (C2)"
    elif 8500 <= freq <= 10500:
        if vel > 400:
            return "Su-57 Felon (Stealth Fighter)"
        elif bw > 15000:
            return "S-400 Triumf (Engagement Radar)"
        else:
            return "Su-35 Flanker-E"
    elif 30 <= freq <= 88:
        return "Tactical VHF Ground Network"
    elif 900 <= freq <= 1400:
        if vel > 200:
            return "MQ-9 Reaper (Armed UAV)"
        return "Long-Range Early Warning Radar"
        
    if vel > 600:
        return "Hypersonic ASM (Anti-Ship Missile)"
        
    if mod in ["UNKNOWN", "QAM16"]:
        return "Commercial UAS / Civil Drone"
        
    return "Unknown Emitter Profile"

def generate_transmitter_id(signal):
    freq = str(round(float(signal.get("frequency_mhz", 0)), 1))
    mod = str(signal.get("modulation", ""))
    
    raw = f"{freq}-{mod}".encode('utf-8')
    h = hashlib.sha1(raw).hexdigest().upper()
    return f"TX-{h[:6]}"

def extract_elint_parameters(signal):
    # Generates realistic Electronic Intelligence stats based on signal props
    mod = str(signal.get("modulation", ""))
    freq = float(signal.get("frequency_mhz", 0))
    
    params = []
    
    if mod in ["PULSED", "FMCW", "SPREAD-SPECTRUM"] or freq > 8000:
        pri = random.randint(500, 2000)
        pw = round(random.uniform(0.5, 5.0), 1)
        params.append(f"PRI: {pri} us")
        params.append(f"PW: {pw} us")
        if mod == "FMCW":
            params.append(f"Sweep Rate: {random.randint(10, 100)} kHz/ms")
        else:
            params.append(f"Scan Rate: {round(random.uniform(1.0, 4.0), 1)}s")
    else:
        params.append(f"Modulation: {mod}")
        params.append("Continuous Wave (CW)")
        
    return " | ".join(params)

def tactical_ai_response(prompt: str, active_tracks, cv_events):
    prompt = prompt.lower()
    
    # 1. Threat Analytics
    if any(word in prompt for word in ["danger", "threat", "highest", "biggest", "target"]):
        if active_tracks is None or active_tracks.empty:
            return "Radar array is currently idle. No immediate threats detected."
        highest = active_tracks.sort_values(by="Threat Score", ascending=False).iloc[0]
        mach = round(highest.get('velocity_ms', 0) / 343, 1)
        alt = int(highest.get('altitude_m', 0))
        
        if highest["Classification"] == "Hostile":
            return f"CRITICAL: The highest threat is a {highest['Platform ID']} at {highest['distance_km']}km bearing {highest['bearing_deg']}°. Target is tracking at {mach} Mach, Altitude {alt}m. Score is {highest['Threat Score']}%. Recommend immediate lock."
        else:
            return f"The highest scored track is a {highest['Classification']} '{highest['Platform ID']}' with score {highest['Threat Score']}%. Moving at {mach} Mach. No hostiles currently pose a severe threat."
            
    # 2. Camera Analytics
    elif any(word in prompt for word in ["camera", "weapon", "gun", "knife", "person", "see"]):
        if not cv_events:
            return "The optical surveillance feed is currently clear. No tactical alerts."
        weapons = [e for e in cv_events if "WEAPON" in e or "GUN" in e or "KNIFE" in e]
        if weapons:
            return "VITAL INCIDENT: Lethal weapons have been visually confirmed by the optical system! Status: HIGH ALERT."
        loiter = [e for e in cv_events if "LOITERING" in e]
        if loiter:
            return "A suspect is currently loitering in the optical target zone (>10s). Surveillance lock established."
        return f"Recent optical event: {cv_events[0]}"
        
    # 3. Overall Sitrep
    elif any(word in prompt for word in ["sitrep", "status", "summary", "report"]):
        if active_tracks is None or active_tracks.empty:
            return "SITREP: Electronic Order of Battle is clear. No active emissions."
        hots = len(active_tracks[active_tracks["Classification"] == "Hostile"])
        avg_dist = round(active_tracks["distance_km"].mean(), 1)
        return f"TACTICAL SITREP: Tracking {len(active_tracks)} live signals (Avg Range: {avg_dist}km). {hots} are classified as Hostile. Radar sweep and CV surveillance are nominal."

    # 4. Intelligence Glossary
    elif "elint" in prompt:
        return "ELINT (Electronic Intelligence) involves gathering data from non-communications electromagnetic radiations, primarily radars, surface-to-air missiles, and aircraft."
    elif "frequency hopping" in prompt or "spread spectrum" in prompt:
        return "Frequency Hopping Spread Spectrum (FHSS) is an evasive transmission method where the carrier frequency rapidly changes according to a pseudorandom sequence to avoid interception and jamming."
        
    # 5. Default Fallback
    return "Command received. Query processed, but no specific tactical correlation found in current radar data. Please specify 'threats', 'sitrep', or 'camera status'."

