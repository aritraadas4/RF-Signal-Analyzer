import hashlib
import random

def calculate_threat_score(signal):
    score = 0

    power = float(signal.get("power_dbm", -120))
    snr = float(signal.get("snr_db", 0))
    frequency = float(signal.get("frequency_mhz", 0))
    bandwidth = float(signal.get("bandwidth_khz", 0))
    modulation = str(signal.get("modulation", "")).strip()
    distance = float(signal.get("distance_km", 100))
    doppler = abs(float(signal.get("doppler_shift_hz", 0)))

    if doppler > 1000:
        score += 25
    elif doppler > 500:
        score += 15

    if bandwidth >= 5000:
        score += 15

    if modulation in ["PULSED", "FMCW", "SPREAD-SPECTRUM"]:
        score += 20
    elif modulation in ["QAM16", "OFDM", "UNKNOWN"]:
        score += 10

    if power > -70 and distance > 50:
        score += 10

    if power < -100 and snr < 5 and doppler > 500:
        score += 15

    if 8500 <= frequency <= 10500:
        score += 15

    return min(int(score), 100)


def classify_signal(score):
    if score < 40:
        return "Friendly"
    elif score < 70:
        return "Unknown"
    return "Hostile"


def anomaly_reason(signal):
    reasons = []

    power = float(signal.get("power_dbm", -120))
    snr = float(signal.get("snr_db", 0))
    frequency = float(signal.get("frequency_mhz", 0))
    bandwidth = float(signal.get("bandwidth_khz", 0))
    modulation = str(signal.get("modulation", "")).strip()
    distance = float(signal.get("distance_km", 100))
    doppler = abs(float(signal.get("doppler_shift_hz", 0)))

    if doppler > 1000:
        reasons.append(f"Supersonic doppler shift detected ({doppler} Hz)")
        
    if bandwidth >= 15000:
        reasons.append("Ultra-wideband transmission")

    if modulation in ["PULSED", "FMCW"]:
        reasons.append("Radar signature detected")
    elif modulation == "SPREAD-SPECTRUM":
        reasons.append("Evasive spread-spectrum hopping")

    if 8500 <= frequency <= 10500:
        reasons.append("X-Band Fire Control illumination")

    if snr < 2.0 and doppler > 500:
        reasons.append("Low-observable (stealth) kinematics")

    if not reasons:
        return "Stable communication pattern"

    return ", ".join(reasons)

def generate_ai_anomaly_explanation(anomaly_string):
    if anomaly_string == "Stable communication pattern":
        return "The emitter is transmitting over a stable carrier wave with no immediate signs of hostile modulation, jumping, or aggressive kinematics. Recommend standard logging."
        
    explanation = "The AI has detected severe deviations from standard telemetry: "
    if "Supersonic doppler shift" in anomaly_string:
        explanation += "The target exhibits extreme radial velocity consistent with a supersonic projectile or high-speed interceptor closing in. "
    if "Ultra-wideband transmission" in anomaly_string:
        explanation += "Massive bandwidth saturation implies either high-density data streaming (C2 datalink) or broadband electronic jamming attempts. "
    if "Radar signature detected" in anomaly_string:
        explanation += "Pulsed or FMCW modulation confirms this is an active radar array mechanically or electronically scanning the airspace. "
    if "spread-spectrum hopping" in anomaly_string:
        explanation += "The signal is rapidly hopping across frequencies, a cryptographic technique used by military networks to evade interception and target-locking. "
    if "X-Band Fire Control" in anomaly_string:
        explanation += "Transmission falls strictly within the X-Band frequency, strongly indicating a surface-to-air missile targeting system actively tracking. "
    if "stealth" in anomaly_string:
        explanation += "Low Signal-to-Noise ratio juxtaposed with high object kinematics suggests a Low-Observable (Stealth) craft attempting to mask its signature. "
        
    return explanation.strip()

def generate_global_ai_analysis(active_tracks):
    if active_tracks is None or active_tracks.empty:
        return "The local aerospace environment is currently clear. No anomalous emissions detected."
        
    hots = active_tracks[active_tracks["Classification"] == "Hostile"]
    
    analysis = f"Currently tracking {len(active_tracks)} live signals with {len(hots)} confirmed as hostile. "
    
    if not hots.empty:
        highest = hots.sort_values(by="Threat Score", ascending=False).iloc[0]
        analysis += f"Primary threat lock is engaged on a {highest['Platform ID']} ({highest['Threat Score']}% Threat Rating) at bearing {highest['bearing_deg']}°, range {highest['distance_km']}km. "
    else:
        analysis += "All tracked signals are currently benign or unidentified. No immediate intercept protocols recommended. "
        
    all_anomalies = []
    for _, track in active_tracks.iterrows():
        a_str = anomaly_reason(track)
        if a_str != "Stable communication pattern":
            all_anomalies.extend(a_str.split(", "))
            
    unique_anomalies = list(set(all_anomalies))
    if unique_anomalies:
        analysis += f"Notable electronic warfare signatures detected across the battlespace: {', '.join(unique_anomalies[:3])}."
        
    return analysis




def recommendation(label, score):
    if label == "Friendly":
        return "Maintain current scan routine"
    elif label == "Unknown":
        if score >= 60:
            return "Task ELINT drone for visual/spectral ID"
        return "Log telemetry and monitor decay"
    else:
        if score >= 85:
            return "AUTHORIZE KINETIC INTERCEPT / ELECTRONIC JAMMING"
        return "Raise DEFCON, lock SAM tracking"

def calculate_confidence(signal):
    snr = float(signal.get("snr_db", 0))
    distance = float(signal.get("distance_km", 100))
    
    base_conf = 50.0
    base_conf += min(snr * 1.5, 45.0)
    
    if distance > 100:
        base_conf -= (distance - 100) * 0.1
        
    return min(max(base_conf, 15.0), 99.9)

def identify_platform(signal):
    freq = float(signal.get("frequency_mhz", 0))
    mod = str(signal.get("modulation", "")).strip()
    bw = float(signal.get("bandwidth_khz", 0))
    
    if 225 <= freq <= 400:
        return "Airborne C2 / AWACS Link"
    elif 8500 <= freq <= 10500:
        if bw > 10000:
            return "S-400 Fire Control Radar"
        else:
            return "Su-35 Flanker-E"
    elif 30 <= freq <= 88:
        return "Ground Infantry VHF Radio"
    elif 900 <= freq <= 1400:
        return "Early Warning Radar (Long Range)"
        
    if mod in ["UNKNOWN", "QAM16"]:
        return "Unidentified Commercial Drone"
        
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
        highest = active_tracks.iloc[0]
        if highest["Classification"] == "Hostile":
            return f"CRITICAL: The highest threat is a {highest['Platform ID']} at {highest['distance_km']}km bearing {highest['bearing_deg']}°. Threat score is {highest['Threat Score']}%. I recommend engaging."
        else:
            return f"The highest scored track is a {highest['Classification']} '{highest['Platform ID']}' with score {highest['Threat Score']}%. No hostiles currently pose a severe threat."
            
    # 2. Camera Analytics
    elif any(word in prompt for word in ["camera", "weapon", "gun", "knife", "person", "see"]):
        if not cv_events:
            return "The optical surveillance feed is currently clear. No tactical alerts."
        weapons = [e for e in cv_events if "WEAPON" in e or "GUN" in e or "KNIFE" in e]
        if weapons:
            return "VITAL INCIDENT: Lethal weapons have been visually confirmed by the optical system recently! Check the CV Logs immediately."
        loiter = [e for e in cv_events if "LOITERING" in e]
        if loiter:
            return "A suspect is currently loitering in the optical target zone. No weapons visually identified yet."
        return f"Recent optical event: {cv_events[0]}"
        
    # 3. Overall Sitrep
    elif any(word in prompt for word in ["sitrep", "status", "summary", "report"]):
        if active_tracks is None or active_tracks.empty:
            return "SITREP: No active signals on the Electronic Order of Battle."
        hots = len(active_tracks[active_tracks["Classification"] == "Hostile"])
        return f"TACTICAL SITREP: Tracking {len(active_tracks)} live signals. {hots} are classified as Hostile. Radar sweep and CV surveillance are nominal."

    # 4. Intelligence Glossary
    elif "elint" in prompt:
        return "ELINT (Electronic Intelligence) involves gathering data from non-communications electromagnetic radiations, primarily radars, surface-to-air missiles, and aircraft."
    elif "frequency hopping" in prompt or "spread spectrum" in prompt:
        return "Frequency Hopping Spread Spectrum (FHSS) is an evasive transmission method where the carrier frequency rapidly changes according to a pseudorandom sequence to avoid interception and jamming."
        
    # 5. Default Fallback
    return "Command received. Query processed, but no specific tactical correlation found in current radar data. Please specify 'threats', 'sitrep', or 'camera status'."

