import cv2
from ultralytics import YOLO
import time
import math
import random
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import speech_recognition as sr
from rf_logic import calculate_threat_score, classify_signal, anomaly_reason, recommendation, calculate_confidence, identify_platform, generate_transmitter_id, extract_elint_parameters, tactical_ai_response, generate_global_ai_analysis

st.set_page_config(page_title="Defense AI Terminal", layout="wide", initial_sidebar_state="expanded")

# -----------------------------
# Clean Blue, Black, White CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #000000 0%, #1e1b4b 40%, #0f172a 75%, #1d4ed8 100%) !important;
    background-color: #000000 !important;
    color: white !important;
}

.stMarkdown, .stMarkdown p, .stMetric label, .stMetric div {
    color: white !important;
}

[data-testid="stAppViewBlockContainer"] {
    background-image: linear-gradient(rgba(30, 58, 138, 0.05) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(30, 58, 138, 0.05) 1px, transparent 1px);
    background-size: 30px 30px;
}

.glass-box {
    background: rgba(2, 6, 15, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(30, 58, 138, 0.4);
    border-radius: 8px;
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0px 8px 16px rgba(0,0,0,0.4);
}

div[data-testid="metric-container"] {
    background: rgba(2, 6, 15, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(30, 58, 138, 0.4);
    border-radius: 8px;
    padding: 15px;
    border-left: 5px solid #38BDF8;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

hr { border-color: rgba(30, 58, 138, 0.5); }

.badge-friendly { color: #FFFFFF; background-color: rgba(30, 58, 138, 0.8); border: 1px solid #38BDF8; padding: 5px 10px; border-radius: 4px; display: inline-block; }
.badge-unknown { color: #000000; background-color: #FACC15; padding: 5px 10px; border-radius: 4px; display: inline-block; }
.badge-hostile { color: #FFFFFF; background-color: rgba(239, 68, 68, 0.8); border: 1px solid #EF4444; padding: 5px 10px; border-radius: 4px; font-weight: 800; display: inline-block; }

.label-muted { color: #7DD3FC; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; }

.elint-log {
    color: #F8FAFC;
    background: rgba(0, 0, 0, 0.5);
    padding: 15px;
    font-size: 0.9em;
    height: 100%;
    border: 1px solid rgba(30, 58, 138, 0.4);
    border-left: 4px solid #38BDF8;
    line-height: 1.6;
    font-family: 'Courier New', monospace;
    border-radius: 4px;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(30, 58, 138, 0.4);
    border-radius: 8px;
}

h1, h2, h3, h4, h5 {
    color: #F8FAFC !important;
    font-weight: 600;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
    border-bottom: 2px solid rgba(30, 58, 138, 0.3) !important;
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(3, 8, 17, 0.8);
    border: 1px solid rgba(30, 58, 138, 0.4);
    border-bottom: none;
    border-radius: 6px 6px 0px 0px;
    padding: 12px 24px;
    color: #7DD3FC;
    font-weight: 600;
    font-size: 1.05em;
    transition: all 0.3s ease;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.5);
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(30, 58, 138, 0.4);
    color: #FFFFFF;
    border-top: 2px solid #7DD3FC;
}

.stTabs [aria-selected="true"] {
    background-color: rgba(30, 58, 138, 0.85) !important;
    color: #FFFFFF !important;
    border-top: 3px solid #38BDF8 !important;
    border-bottom: 2px solid #38BDF8 !important;
}

.main-header {
    background: linear-gradient(90deg, rgba(30,58,138,0.8) 0%, rgba(3,8,17,0.1) 100%);
    padding: 15px 25px;
    border-radius: 8px;
    border-left: 6px solid #38BDF8;
    margin-bottom: 30px;
}
.main-header h1 {
    margin: 0;
    font-size: 2.2em;
    letter-spacing: 2px;
}

/* Custom CSS for Loitering Highlight Error box */
[data-testid="stAlert"] {
    background-color: rgba(239, 68, 68, 0.2);
    border-left: 4px solid #EF4444;
    color: #FFFFFF;
}

/* Transform Sidebar buttons into massive glowing tactical switches */
[data-testid="stSidebar"] button[kind="primary"] {
    background: linear-gradient(90deg, #1E3A8A 0%, #38BDF8 100%) !important;
    border: 2px solid #FFFFFF !important;
    box-shadow: 0px 0px 20px rgba(56, 189, 248, 0.6) !important;
    font-weight: 900 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    transform: scale(1.02);
}

[data-testid="stSidebar"] button[kind="primary"] p {
    font-size: 1.05em !important;
    text-shadow: 0px 3px 6px rgba(0,0,0,0.8) !important;
    padding: 6px 0 !important;
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] button[kind="secondary"] {
    background: rgba(3, 8, 17, 0.8) !important;
    border: 1px solid rgba(30, 58, 138, 0.5) !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] button[kind="secondary"] p {
    font-size: 1.0em !important;
    letter-spacing: 0.5px !important;
    padding: 4px 0 !important;
    color: #7DD3FC !important;
}

[data-testid="stSidebar"] button[kind="secondary"]:hover {
    border-color: #38BDF8 !important;
    box-shadow: 0px 0px 10px rgba(56, 189, 248, 0.3) !important;
}
[data-testid="stSidebar"] button[kind="secondary"]:hover p {
    color: #FFFFFF !important;
}

.module-header {
    font-size: 1.05em;
    font-weight: 800;
    color: #F8FAFC;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    display: flex;
    align-items: center;
    gap: 12px;
}

.module-icon {
    font-size: 1.3em;
    background: rgba(30, 58, 138, 0.4);
    padding: 8px;
    border-radius: 8px;
    border: 1px solid rgba(56, 189, 248, 0.4);
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
}

.sidebar-title {
    text-align: center;
    color: #7DD3FC;
    font-size: 0.85em;
    font-weight: 800;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session state
# -----------------------------
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "🌐 RF SIGNAL ANALYZER"
if "rf_running" not in st.session_state:
    st.session_state.rf_running = False
if "cv_running" not in st.session_state:
    st.session_state.cv_running = False
if "index" not in st.session_state:
    st.session_state.index = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "history" not in st.session_state:
    st.session_state.history = []
if "scores" not in st.session_state:
    st.session_state.scores = []
if "waterfall_grid" not in st.session_state:
    st.session_state.waterfall_grid = np.zeros((30, 100))

# OPTICAL SURVEILLANCE CV STATE
if "cv_cap" not in st.session_state:
    st.session_state.cv_cap = None
if "cv_model" not in st.session_state:
    st.session_state.cv_model = None

if "cv_loiter_start" not in st.session_state:
    st.session_state.cv_loiter_start = None
if "cv_events" not in st.session_state:
    st.session_state.cv_events = []
if "cv_frame" not in st.session_state:
    st.session_state.cv_frame = None

def load_data():
    try:
        df = pd.read_csv("live_signals.csv")
        if "power_dbm" in df.columns:
            return df
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

df = load_data()

# -----------------------------
# QUICK ACCESS AI TERMINAL (FLOATING)
# -----------------------------
st.markdown("""
<style>
div[data-testid="stPopover"] {
    position: fixed !important;
    bottom: 20px !important;
    right: 20px !important;
    z-index: 999999 !important;
    width: 45px !important;
    height: 45px !important;
}
div[data-testid="stPopover"] > button {
    border-radius: 50% !important;
    width: 45px !important;
    height: 45px !important;
    padding: 0 !important;
    background-color: #0F172A !important;
    border: 2px solid #38BDF8 !important;
    font-size: 20px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4) !important;
    transition: transform 0.3s ease-in-out !important;
}
div[data-testid="stPopover"] > button:hover {
    background-color: #0d2745 !important;
    transform: scale(1.1) !important;
    box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6) !important;
}
div[data-testid="stPopover"] > button p {
    margin: 0 !important;
    padding: 0 !important;
    font-size: 1.2em !important;
}
</style>
""", unsafe_allow_html=True)

if "ai_text_input" not in st.session_state:
    st.session_state.ai_text_input = ""

def process_text_query():
    if st.session_state.ai_text_input:
        query = st.session_state.ai_text_input
        hist_df = pd.DataFrame(st.session_state.history) if st.session_state.history else None
        current_tracks = hist_df.drop_duplicates(subset=['Transmitter ID'], keep='last').copy() if hist_df is not None else None
        
        st.session_state.chat_history.append({"role": "user", "content": query})
        resp = tactical_ai_response(query, current_tracks, st.session_state.cv_events)
        st.session_state.chat_history.append({"role": "assistant", "content": resp})
        st.session_state.ai_text_input = ""

with st.popover("🔍"):
        st.markdown("<div style='text-align: center; border-bottom: 1px solid rgba(56, 189, 248, 0.2); padding-bottom: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
        st.markdown("<span style='color: #38BDF8; font-weight: 800; letter-spacing: 1px; font-size: 1.1em;'>🤖 TACTICAL AI ASSISTANT</span><br><span style='font-size: 0.85em; color: #94A3B8;'>Execute text or voice commands to analyze live signal data and camera feeds.</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        chat_container = st.container(height=300)
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_container.markdown(f"**You:** {msg['content']}")
            else:
                chat_container.markdown(f"<span style='color:#38BDF8;'><b>AI:</b> {msg['content']}</span>", unsafe_allow_html=True)
                
        st.text_input("Query intel...", key="ai_text_input", on_change=process_text_query)
        audio_val = st.audio_input("Voice command")
        if audio_val is not None:
            audio_hash = hash(audio_val.getvalue())
            if "last_audio" not in st.session_state or st.session_state.last_audio != audio_hash:
                st.session_state.last_audio = audio_hash
                r = sr.Recognizer()
                try:
                    audio_val.seek(0)
                    with sr.AudioFile(audio_val) as source:
                        audio_data = r.record(source)
                        text = r.recognize_google(audio_data)
                        
                        hist_df = pd.DataFrame(st.session_state.history) if st.session_state.history else None
                        current_tracks = hist_df.drop_duplicates(subset=['Transmitter ID'], keep='last').copy() if hist_df is not None else None
                        
                        st.session_state.chat_history.append({"role": "user", "content": f"🎙️ {text}"})
                        resp = tactical_ai_response(text, current_tracks, st.session_state.cv_events)
                        st.session_state.chat_history.append({"role": "assistant", "content": resp})
                        st.rerun()
                except sr.UnknownValueError:
                    st.error("Audio unintelligible. Please speak clearer.")
                except Exception as e:
                    st.error(f"Audio Decode Error: {e}")



# -----------------------------
# Sidebar Configuration
# -----------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>⚡ SYSTEM MODES</div>", unsafe_allow_html=True)
    
    if st.button("🌐  RF SIGNAL ANALYZER", use_container_width=True, type="primary" if st.session_state.app_mode == "🌐 RF SIGNAL ANALYZER" else "secondary"):
        st.session_state.app_mode = "🌐 RF SIGNAL ANALYZER"
        st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
    if st.button("👁️ OPTICAL SURVEILLANCE", use_container_width=True, type="primary" if st.session_state.app_mode == "👁️ OPTICAL SURVEILLANCE" else "secondary"):
        st.session_state.app_mode = "👁️ OPTICAL SURVEILLANCE"
        st.rerun()
    
    st.markdown("<br><div class='sidebar-title'>⚙️ COMMAND INTERFACE</div>", unsafe_allow_html=True)
    
    speed = st.slider("SURVEILLANCE SWEEP SPEED (Seconds)", 0.2, 3.0, 1.0, 0.1)
    
    if st.session_state.app_mode == "🌐 RF SIGNAL ANALYZER":
        if st.button("▶ BEGIN RF SURVEILLANCE", use_container_width=True, type="primary"):
            st.session_state.rf_running = True
        if st.button("⏸ PAUSE RF TRACKING", use_container_width=True):
            st.session_state.rf_running = False
            
        st.markdown("<br><br>", unsafe_allow_html=True)
            
        if st.button("🚫 PURGE RF DATA", use_container_width=True):
            st.session_state.rf_running = False
            st.session_state.index = 0
            st.session_state.history = []
            st.session_state.scores = []
            st.session_state.waterfall_grid = np.zeros((30, 100))
            st.rerun()
    else:
        if st.button("▶ INITIALIZE CAMERA FEED", use_container_width=True, type="primary"):
            st.session_state.cv_running = True
        if st.button("⏸ PAUSE CAMERA FEED", use_container_width=True):
            st.session_state.cv_running = False
            
        st.markdown("<br><br>", unsafe_allow_html=True)
            
        if st.button("🚫 PURGE OPTICAL LOGS", use_container_width=True):
            st.session_state.cv_running = False
            st.session_state.cv_events = []
            st.session_state.cv_loiter_start = None
            st.rerun()


# -----------------------------
# Processing Logic (Always runs in background if active)
# -----------------------------
signal = None
active_tracks = None

if st.session_state.rf_running:
    if len(df) == 0:
        st.session_state.rf_running = False
        if st.session_state.app_mode == "🌐 RF SIGNAL ANALYZER":
            st.error("NO SIGNAL DATA RECOGNIZED. Ensure the emitter proxy is online.")
    else:
        if st.session_state.index >= len(df):
            st.session_state.index = max(0, len(df) - 1)
            
        row = df.iloc[st.session_state.index].to_dict()

    score = calculate_threat_score(row)
    label = classify_signal(score)
    
    confidence = calculate_confidence(row)
    platform = identify_platform(row)
    tx_id = generate_transmitter_id(row)
    elint_params = extract_elint_parameters(row)

    row["Threat Score"] = score
    row["Classification"] = label
    row["Anomaly Reason"] = anomaly_reason(row)
    row["Recommendation"] = recommendation(label, score)
    row["Confidence"] = confidence
    row["Platform ID"] = platform
    row["Transmitter ID"] = tx_id
    row["ELINT Details"] = elint_params

    color_map = {"Friendly": "#1E3A8A", "Unknown": "#FACC15", "Hostile": "#EF4444"}
    row["color"] = color_map.get(label, "#FFFFFF")

    st.session_state.history.append(row)
    if len(st.session_state.history) > 100:
        st.session_state.history.pop(0)
        
    st.session_state.scores.append(score)
    if len(st.session_state.scores) > 100:
        st.session_state.scores.pop(0)

    freq_val = row.get("frequency_mhz", 0)
    bin_idx = int(min(max(freq_val / 150, 0), 99))
    st.session_state.waterfall_grid = np.roll(st.session_state.waterfall_grid, shift=1, axis=0)
    st.session_state.waterfall_grid[0] = np.random.uniform(-110, -100, 100)
    power = row.get("power_dbm", -90)
    spread = int(row.get("bandwidth_khz", 25) / 500) + 1
    for i in range(max(0, bin_idx - spread), min(100, bin_idx + spread + 1)):
         st.session_state.waterfall_grid[0][i] = power + random.uniform(-2, 2)



    st.session_state.index += 1


# -----------------------------
# MODE: RF SIGNAL ANALYZER
# -----------------------------
if st.session_state.app_mode == "🌐 RF SIGNAL ANALYZER":
    st.markdown("""
    <div class="main-header">
        <h1>RF SIGNAL ANALYZER</h1>
    </div>
    """, unsafe_allow_html=True)
    
    signal = st.session_state.history[-1] if st.session_state.history else None
    
    if signal is None:
        st.info("System Paused. Click **BEGIN SURVEILLANCE** to scan environments.")
    else:
        hist_df = pd.DataFrame(st.session_state.history)
        active_tracks = hist_df.drop_duplicates(subset=['Transmitter ID'], keep='last').copy()

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Latest Threat Score", f"{signal['Threat Score']}%")
        with m2:
            st.metric("Total Active Tracks", len(active_tracks))
        with m3:
            st.metric("Hostile Targets Detected", len(active_tracks[active_tracks["Classification"] == "Hostile"]))
        with m4:
            st.metric("Max Range Evaluated", f"{active_tracks['distance_km'].max():.1f} km" if len(active_tracks) > 0 else "0 km")

        # --- GLOBAL AI OVERVIEW ---
        global_ai_text = generate_global_ai_analysis(active_tracks)
        st.markdown("<div style='background:rgba(239, 68, 68, 0.1); border-left: 3px solid #EF4444; padding: 15px; margin-top:15px; margin-bottom:15px; border-radius: 4px; box-shadow: 0 0 15px rgba(239,68,68,0.15);'>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#EF4444; font-weight:800; font-size:0.9em; letter-spacing:1.5px;'>🤖 BATTLESPACE AI OVERVIEW</span><br><span style='color:#FCA5A5; font-size: 0.95em; line-height: 1.5; font-weight:500;'>{global_ai_text}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2, tab3, tab4 = st.tabs([
            "➤  BATTLESPACE RADAR", 
            "➤  ELECTRONIC INTELLIGENCE", 
            "➤  THREAT HISTORICS",
            "➤  C2 NETWORK TOPOLOGY"
        ])
        
        with tab1:
            col_radar, col_orbat = st.columns([1, 1.2])
            with col_radar:
                st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
                st.markdown("<div class='module-header'><span class='module-icon'>📡</span> TACTICAL SITREP RADAR</div>", unsafe_allow_html=True)
                sectors = np.arange(0, 360, 45)
                sector_colors = []
                for s in sectors:
                    in_sector = active_tracks[(active_tracks["bearing_deg"] >= s) & (active_tracks["bearing_deg"] < s + 45)]
                    max_threat = in_sector["Threat Score"].max() if not in_sector.empty else 0
                    if max_threat >= 70:
                        sector_colors.append("rgba(239, 68, 68, 0.25)")
                    elif max_threat >= 40:
                        sector_colors.append("rgba(250, 204, 21, 0.25)")
                    else:
                        sector_colors.append("rgba(30, 58, 138, 0.15)")
                        
                fig = go.Figure(go.Barpolar(r=[300]*8, theta=sectors + 22.5, width=[44.5]*8, marker_color=sector_colors, marker_line_color="#1E3A8A", marker_line_width=1, opacity=0.8, hoverinfo="none"))
                
                if not active_tracks.empty:
                    symbols = active_tracks["Classification"].map({"Hostile": "diamond-open", "Unknown": "square-open", "Friendly": "circle-open"}).tolist()
                    fig.add_trace(go.Scatterpolar(
                        r=active_tracks["distance_km"], theta=active_tracks["bearing_deg"], mode="markers+text",
                        marker=dict(color=active_tracks["color"], size=14, symbol=symbols, line=dict(color=active_tracks["color"], width=2)),
                        text=active_tracks["Transmitter ID"].str[-4:], textposition="top right", textfont=dict(color="#7DD3FC", size=10),
                        hovertext=active_tracks["Platform ID"] + "<br>Range: " + active_tracks["distance_km"].astype(str) + " km", hoverinfo="text"
                    ))

                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 300], gridcolor="#1E3A8A", gridwidth=1.5, tickfont=dict(color="#38BDF8", size=9), dtick=50, angle=90),
                        angularaxis=dict(direction="clockwise", rotation=90, gridcolor="#1E3A8A", gridwidth=1.5, tickfont=dict(color="#94A3B8", size=11, family="Inter", weight="bold"), tickmode="array", tickvals=np.arange(0, 360, 45), ticktext=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
                        bgcolor="#01040A"
                    ),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=20, l=20, r=20), height=380, showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("""
                <div style='display:flex; justify-content:center; gap:15px; font-size:0.85em; margin-top:5px; color:#FFFFFF; border:1px solid rgba(255,255,255,0.1); padding:8px; border-radius:6px; background:rgba(0,0,0,0.5);'>
                    <div><span style='color:rgba(239, 68, 68, 0.8); font-size:1.2em;'>🟥</span> HIGH THREAT ALARM (Score 70+)</div>
                    <div><span style='color:rgba(250, 204, 21, 0.8); font-size:1.2em;'>🟨</span> ELEVATED RISK (Score 40-69)</div>
                    <div><span style='color:rgba(30, 58, 138, 0.8); font-size:1.2em;'>🟦</span> CLEAR / ROUTINE (Score &lt;40)</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_orbat:
                st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
                st.markdown("<div class='module-header'><span class='module-icon'>📋</span> ACTIVE THREAT DATABASE</div>", unsafe_allow_html=True)
                display_tracks = active_tracks[["Transmitter ID", "Classification", "Confidence", "Platform ID", "frequency_mhz", "distance_km", "Threat Score"]].copy()
                display_tracks["Confidence"] = display_tracks["Confidence"].apply(lambda x: f"{x:.1f}%")
                display_tracks = display_tracks.sort_values(by="Threat Score", ascending=False)
                st.dataframe(display_tracks, use_container_width=True, hide_index=True, height=380)
                st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='module-header'><span class='module-icon'>🌊</span> LIVE WATERFALL SPECTROGRAM</div>", unsafe_allow_html=True)
            fig_wf = go.Figure(data=go.Heatmap(z=st.session_state.waterfall_grid, colorscale='Blues', zmin=-120, zmax=-40, showscale=False))
            fig_wf.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(showticklabels=False, showgrid=False), yaxis=dict(showticklabels=False, autorange='reversed', showgrid=False), height=350)
            st.plotly_chart(fig_wf, use_container_width=True)
            st.markdown("""
            <div style='display:flex; justify-content:center; gap:20px; font-size:0.85em; margin-top:5px; color:#FFFFFF; border:1px solid rgba(255,255,255,0.1); padding:8px; border-radius:6px; background:rgba(0,0,0,0.5);'>
                <div><span style='color:#EFF6FF; font-size:1.2em;'>⬜</span> PEAK EMISSION SPIKE</div>
                <div><span style='color:#60A5FA; font-size:1.2em;'>🟦</span> ACTIVE RF SIGNAL</div>
                <div><span style='color:#01040A; text-shadow: 0 0 2px white; font-size:1.2em;'>⬛</span> BACKGROUND NOISE FLOOR</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            col_details, col_elint = st.columns([1.5, 1])
            with col_details:
                st.markdown("<div class='module-header'><span class='module-icon'>📑</span> INTERCEPT REPORT</div>", unsafe_allow_html=True)
                c = signal["Classification"]
                badge_class = f"badge-{c.lower()}"
                st.markdown(f'<div style="margin-bottom: 20px;"><span class="{badge_class}">Status: {c} / {signal["Confidence"]:.1f}% Match</span></div>', unsafe_allow_html=True)
                st.markdown(f"**Identified Platform:**<br><span style='color:#FFFFFF; font-size:1.1em;'>{signal['Platform ID']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Target Action Recommendation:**<br><span style='color:#38BDF8;'>{signal['Recommendation']}</span>", unsafe_allow_html=True)
            with col_elint:
                st.markdown("<div class='module-header'><span class='module-icon'>💻</span> ELINT SYSTEM LOGS</div>", unsafe_allow_html=True)
                elint_text = "<br>".join([f"Frequency : {signal['frequency_mhz']} MHz", f"Bandwidth : {signal['bandwidth_khz']} kHz", f"Doppler   : {signal['doppler_shift_hz']} Hz", f"Power Rx  : {signal['power_dbm']} dBm", ""] + [line for line in signal['ELINT Details'].split(' | ')])
                st.markdown(f"<div class='elint-log'>{elint_text}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with tab3:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='module-header'><span class='module-icon'>📉</span> HISTORICAL EVENT TRACKING</div>", unsafe_allow_html=True)
            trend_df = pd.DataFrame({"Time": range(len(st.session_state.scores)), "Threat Score": st.session_state.scores})
            line_fig = px.area(trend_df, x="Time", y="Threat Score", template="plotly_dark", color_discrete_sequence=["#38BDF8"])
            line_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(showgrid=True, gridcolor='rgba(30,58,138,0.3)'), yaxis=dict(showgrid=True, gridcolor='rgba(30,58,138,0.3)', range=[0, 100]), height=600)
            st.plotly_chart(line_fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with tab4:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='module-header'><span class='module-icon'>🕸️</span> C2 NETWORK TOPOLOGY MAP</div>", unsafe_allow_html=True)
            
            if not active_tracks.empty and len(active_tracks) > 1:
                # Convert polar coordinates to Cartesian for layout mapping
                nodes = active_tracks.copy()
                nodes['x'] = nodes['distance_km'] * np.cos(np.radians(nodes['bearing_deg']))
                nodes['y'] = nodes['distance_km'] * np.sin(np.radians(nodes['bearing_deg']))
                
                edge_x = []
                edge_y = []
                
                node_connections = {i: 0 for i in range(len(nodes))}
                node_ids = list(nodes.index)
                
                for i in range(len(node_ids)):
                    for j in range(i+1, len(node_ids)):
                        idx1 = node_ids[i]
                        idx2 = node_ids[j]
                        
                        f1 = nodes.loc[idx1, 'frequency_mhz']
                        f2 = nodes.loc[idx2, 'frequency_mhz']
                        
                        dx = nodes.loc[idx1, 'x'] - nodes.loc[idx2, 'x']
                        dy = nodes.loc[idx1, 'y'] - nodes.loc[idx2, 'y']
                        dist = np.sqrt(dx**2 + dy**2)
                        
                        # Link if freq delta < 50MHz and distance < 100km
                        if abs(f1 - f2) < 50 and dist < 100:
                            edge_x.extend([nodes.loc[idx1, 'x'], nodes.loc[idx2, 'x'], None])
                            edge_y.extend([nodes.loc[idx1, 'y'], nodes.loc[idx2, 'y'], None])
                            node_connections[i] += 1
                            node_connections[j] += 1
                
                node_sizes = [15 + (node_connections[i] * 5) for i in range(len(nodes))]
                
                max_conn = max(node_connections.values()) if node_connections else 0
                command_node_idx = None
                if max_conn > 0:
                    command_node_idx = node_ids[max(node_connections, key=node_connections.get)]
                
                node_texts = []
                for idx_num, idx in enumerate(node_ids):
                    lbl = nodes.loc[idx, 'Classification']
                    if idx == command_node_idx and lbl == "Hostile":
                        node_texts.append("🔴 COMMAND TARGET 🔴")
                    else:
                        node_texts.append(nodes.loc[idx, 'Platform ID'])
                        
                fig_net = go.Figure()
                
                if len(edge_x) > 0:
                    fig_net.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=1.5, color='rgba(56, 189, 248, 0.4)'), mode='lines', hoverinfo='none', showlegend=False))
                    
                symbols_net = nodes["Classification"].map({"Hostile": "diamond", "Unknown": "square", "Friendly": "circle"}).tolist()
                
                fig_net.add_trace(go.Scatter(
                    x=nodes['x'], y=nodes['y'], 
                    mode='markers+text',
                    marker=dict(size=node_sizes, color=nodes["color"], symbol=symbols_net, line=dict(width=2, color="#FFFFFF")),
                    text=node_texts,
                    textposition="top center",
                    textfont=dict(color="#F8FAFC", size=11, family="Inter", weight="bold"),
                    hovertext=nodes['Transmitter ID'] + "<br>Freq: " + nodes['frequency_mhz'].astype(str) + " MHz<br>Links: " + pd.Series(node_connections).astype(str).values,
                    hoverinfo='text',
                    showlegend=False
                ))
                
                fig_net.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=10, b=0),
                    xaxis=dict(showgrid=True, gridcolor='rgba(30,58,138,0.2)', zeroline=True, zerolinecolor='rgba(56, 189, 248, 0.5)', showticklabels=False, title=''),
                    yaxis=dict(showgrid=True, gridcolor='rgba(30,58,138,0.2)', zeroline=True, zerolinecolor='rgba(56, 189, 248, 0.5)', showticklabels=False, title=''),
                    height=600, showlegend=False
                )
                
                st.plotly_chart(fig_net, use_container_width=True)
                st.markdown("""
                <div style='display:flex; justify-content:center; gap:20px; font-size:0.85em; margin-top:5px; color:#FFFFFF; border:1px solid rgba(255,255,255,0.1); padding:8px; border-radius:6px; background:rgba(0,0,0,0.5);'>
                    <div><span style='color:#EF4444; font-size:1.2em;'>🔴</span> HOSTILE NODE TARGET</div>
                    <div><span style='color:#38BDF8; font-size:1.2em;'>🔵</span> FRIENDLY / ALLIED NODE</div>
                    <div><span style='color:#FACC15; font-size:1.2em;'>🟡</span> UNKNOWN / NEUTRAL NODE</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Insufficient tracks or tactical proximity to map C2 Topology Network.")
            
            st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# MODE: OPTICAL SURVEILLANCE
# -----------------------------
elif st.session_state.app_mode == "👁️ OPTICAL SURVEILLANCE":
    st.markdown("""
    <div class="main-header">
        <h1>OPTICAL SURVEILLANCE STATION</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.cv_running:
        if st.session_state.cv_model is None:
            st.session_state.cv_model = YOLO("yolov8m.pt")
        if st.session_state.cv_cap is None:
            st.session_state.cv_cap = cv2.VideoCapture(0)

        if st.session_state.cv_model is not None and st.session_state.cv_cap.isOpened():
            ret, frame = st.session_state.cv_cap.read()
            if ret:
                results = st.session_state.cv_model(frame)
                person_detected = False
                detected_crit_objects = []
                
                for r in results:
                    for box in r.boxes:
                        cls = int(box.cls[0])
                        label_cv = st.session_state.cv_model.names[cls]
                        conf_cv = float(box.conf[0])
                        
                        if label_cv in ["person", "knife", "gun", "weapon"]:
                            detected_crit_objects.append(f"{label_cv.upper()} ({conf_cv:.2f})")
                            if label_cv == "person":
                                person_detected = True
                                
                if person_detected:
                    if st.session_state.cv_loiter_start is None:
                        st.session_state.cv_loiter_start = time.time()
                    elif (time.time() - st.session_state.cv_loiter_start) > 10:
                        alert_msg = f"[{time.strftime('%X')}] 🚨 LOITERING ALERT: SUSPECT IN FRAME > 10s"
                        if not st.session_state.cv_events or st.session_state.cv_events[0] != alert_msg:
                            st.session_state.cv_events.insert(0, alert_msg)
                else:
                    st.session_state.cv_loiter_start = None
                    
                if detected_crit_objects:
                    st.session_state.cv_events.insert(0, f"[{time.strftime('%X')}] DETECTED: {', '.join(detected_crit_objects)}")
                
                if len(st.session_state.cv_events) > 20:
                    st.session_state.cv_events = st.session_state.cv_events[:20]
                    
                annotated_frame = results[0].plot()
                
                if st.session_state.cv_loiter_start is not None and (time.time() - st.session_state.cv_loiter_start) > 10:
                    cv2.putText(annotated_frame, "HIGH ALERT: LOITERING!", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)

                weapon_detected = any(obj for obj in detected_crit_objects if "KNIFE" in obj or "GUN" in obj or "WEAPON" in obj)
                if weapon_detected:
                    cv2.putText(annotated_frame, "HIGH ALERT: WEAPON DETECTED!", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)

                st.session_state.cv_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

    # Render loitering highlight massively if detected recently
    is_loitering = False
    for event in st.session_state.cv_events[:5]:
        if "LOITERING ALERT" in event:
            is_loitering = True
            
    if is_loitering:
        st.error("🚨 CRITICAL WARNING: Active Suspect Loitering Detected (>10 seconds in frame)")

    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("<div class='module-header'><span class='module-icon'>📹</span> LIVE CV SECTOR OVERLOOK</div>", unsafe_allow_html=True)
    
    col_video, col_logs = st.columns([1.5, 1])
    with col_video:
        if st.session_state.cv_frame is not None:
            st.image(st.session_state.cv_frame, use_container_width=True)
        else:
            st.info("Awaiting Camera Initialization... Press BEGIN SURVEILLANCE to fetch frames.")
    with col_logs:
        st.markdown("<b>Optical Event Log</b>", unsafe_allow_html=True)
        if not st.session_state.cv_events:
            st.markdown("<div class='elint-log'>No tactical optical alerts.</div>", unsafe_allow_html=True)
        else:
            log_text = "<br>".join(st.session_state.cv_events)
            st.markdown(f"<div class='elint-log'>{log_text}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)



# -----------------------------
# Auto refresh 
# -----------------------------
if st.session_state.rf_running or st.session_state.cv_running:
    time.sleep(speed)
    st.rerun()
