import cv2
from ultralytics import YOLO
import time
import math
import random
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import speech_recognition as sr
from rf_logic import calculate_threat_score, classify_signal, anomaly_reason, recommendation, calculate_confidence, identify_platform, generate_transmitter_id, extract_elint_parameters, tactical_ai_response, generate_global_ai_analysis

st.set_page_config(page_title="Defense AI Terminal", layout="wide", initial_sidebar_state="expanded")

# -----------------------------
# Global CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── Main background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #000000 0%, #0a0f2e 40%, #0f172a 75%, #0a1a3a 100%) !important;
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

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #000000 0%, #060d1f 50%, #000a1a 100%) !important;
    border-right: 1px solid rgba(30, 58, 138, 0.5) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSlider p,
[data-testid="stSidebar"] p {
    color: #7DD3FC !important;
}

/* ── Sidebar buttons – active mode (primary) ── */
[data-testid="stSidebar"] button[kind="primary"] {
    background: linear-gradient(90deg, #0d2a6e 0%, #1a4a9c 100%) !important;
    border: 1px solid #38BDF8 !important;
    box-shadow: 0px 0px 14px rgba(56, 189, 248, 0.35) !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] button[kind="primary"] p {
    font-size: 0.92em !important;
    padding: 4px 0 !important;
    color: #FFFFFF !important;
    letter-spacing: 1.2px !important;
}

/* ── Sidebar buttons – inactive (secondary) ── */
[data-testid="stSidebar"] button[kind="secondary"] {
    background: rgba(6, 13, 31, 0.9) !important;
    border: 1px solid rgba(30, 58, 138, 0.45) !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] button[kind="secondary"] p {
    font-size: 0.92em !important;
    letter-spacing: 1px !important;
    padding: 4px 0 !important;
    color: #7DD3FC !important;
}

[data-testid="stSidebar"] button[kind="secondary"]:hover {
    border-color: #38BDF8 !important;
    background: rgba(15, 35, 80, 0.7) !important;
    box-shadow: 0px 0px 8px rgba(56, 189, 248, 0.2) !important;
}

[data-testid="stSidebar"] button[kind="secondary"]:hover p {
    color: #FFFFFF !important;
}

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: rgba(2, 6, 15, 0.85);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 10px;
    padding: 18px;
    border-left: 6px solid #38BDF8;
    box-shadow: 0px 6px 15px rgba(0,0,0,0.5);
}

/* ── Glass panels ── */
.glass-box {
    background: rgba(2, 6, 15, 0.8);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 25px;
    box-shadow: 0px 12px 30px rgba(0,0,0,0.6), inset 0 0 15px rgba(56, 189, 248, 0.05);
}

hr { border-color: rgba(30, 58, 138, 0.5); }

/* ── Classification badges ── */
.badge-friendly { color: #FFFFFF; background-color: rgba(30, 58, 138, 0.8); border: 1px solid #38BDF8; padding: 5px 12px; border-radius: 4px; display: inline-block; font-weight: 600; letter-spacing: 0.5px; }
.badge-unknown  { color: #0a0f2e; background-color: #FACC15; padding: 5px 12px; border-radius: 4px; display: inline-block; font-weight: 600; }
.badge-hostile  { color: #FFFFFF; background-color: rgba(239, 68, 68, 0.85); border: 1px solid #EF4444; padding: 5px 12px; border-radius: 4px; font-weight: 800; display: inline-block; letter-spacing: 0.5px; }

.label-muted { color: #7DD3FC; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; }

/* ── ELINT terminal log ── */
.elint-log {
    color: #F8FAFC;
    background: rgba(0, 0, 0, 0.5);
    padding: 15px;
    font-size: 0.9em;
    height: 100%;
    border: 1px solid rgba(30, 58, 138, 0.4);
    border-left: 4px solid #38BDF8;
    line-height: 1.7;
    font-family: 'Courier New', monospace;
    border-radius: 4px;
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(30, 58, 138, 0.4);
    border-radius: 8px;
}

h1, h2, h3, h4, h5 {
    color: #F8FAFC !important;
    font-weight: 600;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    border-bottom: 2px solid rgba(30, 58, 138, 0.3) !important;
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(3, 8, 17, 0.8);
    border: 1px solid rgba(30, 58, 138, 0.4);
    border-bottom: none;
    border-radius: 6px 6px 0px 0px;
    padding: 10px 22px;
    color: #7DD3FC;
    font-weight: 600;
    font-size: 0.95em;
    letter-spacing: 0.8px;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(30, 58, 138, 0.35);
    color: #FFFFFF;
    border-top: 2px solid #7DD3FC;
}

.stTabs [aria-selected="true"] {
    background-color: rgba(30, 58, 138, 0.8) !important;
    color: #FFFFFF !important;
    border-top: 3px solid #38BDF8 !important;
}

/* ── Page header banner ── */
.main-header {
    background: linear-gradient(90deg, rgba(13, 42, 110, 0.9) 0%, rgba(3, 8, 17, 0.2) 100%);
    padding: 16px 28px;
    border-radius: 8px;
    border-left: 6px solid #38BDF8;
    margin-bottom: 28px;
}

.main-header h1 {
    margin: 0;
    font-size: 2em;
    letter-spacing: 3px;
    font-weight: 800;
}

/* ── Alert/error box ── */
[data-testid="stAlert"] {
    background-color: rgba(239, 68, 68, 0.15);
    border-left: 4px solid #EF4444;
    color: #FFFFFF;
}

/* ── Module panel headers ── */
.module-header {
    font-size: 0.95em;
    font-weight: 800;
    color: #F8FAFC;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 20px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    display: flex;
    align-items: center;
    gap: 10px;
}

.module-tag {
    font-size: 0.75em;
    background: rgba(30, 58, 138, 0.6);
    color: #38BDF8;
    padding: 4px 10px;
    border-radius: 4px;
    border: 1px solid rgba(56, 189, 248, 0.35);
    letter-spacing: 1.5px;
    font-weight: 700;
}

/* ── Sidebar section label ── */
.sidebar-section-label {
    text-align: left;
    color: rgba(56, 189, 248, 0.6);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 18px 0 10px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(30, 58, 138, 0.4);
}

/* ── Legend row ── */
.legend-row {
    display: flex;
    justify-content: center;
    gap: 20px;
    font-size: 0.82em;
    margin-top: 8px;
    color: #FFFFFF;
    border: 1px solid rgba(56, 189, 248, 0.15);
    padding: 9px 16px;
    border-radius: 6px;
    background: rgba(0, 0, 0, 0.45);
    letter-spacing: 0.5px;
}

.legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    vertical-align: middle;
}

.legend-sq {
    width: 10px;
    height: 10px;
    display: inline-block;
    margin-right: 6px;
    vertical-align: middle;
}

/* ── Floating AI popover ── */
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
    background-color: #060d1f !important;
    border: 2px solid #38BDF8 !important;
    font-size: 18px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4) !important;
    transition: transform 0.2s ease-in-out !important;
}
div[data-testid="stPopover"] > button:hover {
    background-color: #0d2a6e !important;
    transform: scale(1.1) !important;
    box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6) !important;
}
div[data-testid="stPopover"] > button p {
    margin: 0 !important;
    padding: 0 !important;
    font-size: 1.1em !important;
    color: #38BDF8 !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# AUTHENTICATION GATE
# ══════════════════════════════════════════════════════════════
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "auth_error" not in st.session_state:
    st.session_state.auth_error = ""
if "auth_attempts" not in st.session_state:
    st.session_state.auth_attempts = 0

if not st.session_state.authenticated:
    # ── Full-page login styles (red-black fusion) ──────────────
    st.markdown("""
    <style>
    /* Hide sidebar and strip padding on login screen */
    [data-testid="stSidebar"]          { display: none !important; }
    [data-testid="stHeader"]           { display: none !important; }
    [data-testid="stToolbar"]          { display: none !important; }
    [data-testid="stDecoration"]       { display: none !important; }

    /* RED-BLACK fusion background — login page only */
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 50% 0%,   #3b0000 0%,  #1a0000 35%, #000000 70%)
            !important;
        background-color: #000000 !important;
    }
    [data-testid="stAppViewBlockContainer"] {
        background-image: none !important;  /* remove grid from main app */
        padding-top: 0 !important;
    }

    /* Kill default top padding */
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }

    /* Style the MIDDLE column as the card */
    div[data-testid="column"]:nth-child(2) > div:first-child {
        background: rgba(8, 2, 2, 0.92) !important;
        border: 1px solid rgba(239, 68, 68, 0.30) !important;
        border-top: 3px solid #EF4444 !important;
        border-radius: 14px !important;
        padding: 36px 36px 30px !important;
        box-shadow:
            0 0  60px rgba(220, 38, 38, 0.18),
            0 20px 60px rgba(0, 0, 0, 0.90),
            inset 0 0 30px rgba(139, 0, 0, 0.06) !important;
        backdrop-filter: blur(20px) !important;
    }

    /* Input fields */
    div[data-testid="column"]:nth-child(2) input {
        background: rgba(20, 2, 2, 0.8) !important;
        border: 1px solid rgba(239, 68, 68, 0.30) !important;
        color: #F8FAFC !important;
        border-radius: 6px !important;
    }
    div[data-testid="column"]:nth-child(2) input:focus {
        border-color: #EF4444 !important;
        box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.20) !important;
    }
    div[data-testid="column"]:nth-child(2) input::placeholder {
        color: #4B2525 !important;
    }

    /* Authenticate button */
    div[data-testid="column"]:nth-child(2) button[kind="primary"] {
        background: linear-gradient(90deg, #7f1d1d 0%, #991b1b 50%, #7f1d1d 100%) !important;
        border: 1px solid #EF4444 !important;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.35) !important;
        font-weight: 800 !important;
        letter-spacing: 2px !important;
        font-size: 0.85em !important;
        border-radius: 6px !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="column"]:nth-child(2) button[kind="primary"]:hover {
        background: linear-gradient(90deg, #991b1b 0%, #b91c1c 50%, #991b1b 100%) !important;
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.55) !important;
        transform: translateY(-1px) !important;
    }
    div[data-testid="column"]:nth-child(2) button[kind="primary"] p {
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Lock icon + header ──────────────────────────────────────
    st.markdown("""
    <div style='text-align:center; padding: 30px 0 20px 0;'>
        <div style='font-size:3.2em; margin-bottom:14px; filter: drop-shadow(0 0 18px rgba(239,68,68,0.6));'>🔒</div>
        <div style='
            display:inline-block;
            font-size:0.7em; font-weight:700; letter-spacing:5px; color:#EF4444;
            text-transform:uppercase; padding:5px 20px;
            border:1px solid rgba(239,68,68,0.45); border-radius:3px;
            background:rgba(239,68,68,0.08); margin-bottom:16px;'>
            ⚠ &nbsp; CLASSIFIED SYSTEM — AUTHORIZED ACCESS ONLY
        </div>
        <div style='
            font-size:2.4em; font-weight:900; letter-spacing:7px;
            color:#F8FAFC; margin: 0 0 6px 0;
            text-shadow: 0 0 50px rgba(220,38,38,0.5), 0 0 20px rgba(239,68,68,0.3);'>
            DEFENSE AI TERMINAL
        </div>
        <div style='
            font-size:0.78em; color:#6B2121; letter-spacing:3px;
            text-transform:uppercase; margin-bottom:10px;'>
            Integrated SIGINT &amp; Optical Surveillance Platform &nbsp;·&nbsp; REL FVEY
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Centered login form using columns ───────────────────────
    _l, col_c, _r = st.columns([1, 1.2, 1])
    with col_c:
        # Officer Name field
        st.markdown("""
        <div style='font-size:0.72em; font-weight:700; letter-spacing:2.5px;
                    text-transform:uppercase; color:#EF4444; margin-bottom:6px;'>
            👤 &nbsp; Officer Name
        </div>""", unsafe_allow_html=True)
        name_input = st.text_input("name", label_visibility="collapsed",
                                   placeholder="Enter your full name", key="login_name")

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        st.markdown("""<hr style='border:none; border-top:1px solid rgba(139,0,0,0.4); margin:16px 0;'>""",
                    unsafe_allow_html=True)

        # Officer ID field
        st.markdown("""
        <div style='font-size:0.72em; font-weight:700; letter-spacing:2.5px;
                    text-transform:uppercase; color:#EF4444; margin-bottom:6px;'>
            🔐 &nbsp; Officer ID
        </div>""", unsafe_allow_html=True)
        id_input = st.text_input("officer_id", label_visibility="collapsed",
                                 placeholder="Enter your Officer ID",
                                 type="password", key="login_id")

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

        # Authenticate button
        if st.button("  AUTHENTICATE & ENTER SYSTEM  ", use_container_width=True, type="primary"):
            if (name_input.strip().upper() == "ARITRAA DAS" and
                    id_input.strip() == "aritraadas2006"):
                st.session_state.authenticated = True
                st.session_state.auth_error = ""
                st.rerun()
            else:
                st.session_state.auth_attempts += 1
                st.session_state.auth_error = (
                    f"⚠  ACCESS DENIED — Invalid credentials "
                    f"(Attempt {st.session_state.auth_attempts})"
                )
                st.rerun()

        # Error message
        if st.session_state.auth_error:
            st.markdown(
                f"<div style='margin-top:12px; padding:10px 14px; "
                f"background:rgba(139,0,0,0.18); border-left:3px solid #EF4444; "
                f"border-radius:5px; color:#FCA5A5; font-size:0.83em; "
                f"letter-spacing:0.5px;'>{st.session_state.auth_error}</div>",
                unsafe_allow_html=True
            )

        # Footer inside card
        st.markdown("""
        <hr style='border:none; border-top:1px solid rgba(139,0,0,0.35); margin:22px 0 14px 0;'>
        <div style='font-size:0.68em; color:#4B1111; text-align:center;
                    letter-spacing:2px; text-transform:uppercase;'>
            SIGINT PLATFORM v2.0 &nbsp;·&nbsp; RESTRICTED &nbsp;·&nbsp; DO NOT SHARE
        </div>
        <div style='font-family:monospace; color:rgba(139,0,0,0.18); font-size:0.6em;
                    text-align:center; margin-top:6px; letter-spacing:1px;'>
            ████ ██████ ████ ██ ████████ ████ ███ ██████
        </div>
        """, unsafe_allow_html=True)

    st.stop()   # ◄── blocks ALL application code for unauthenticated users

# -----------------------------
# Session state
# -----------------------------
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "RF SIGNAL ANALYZER"
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
        if "frequency_mhz" in df.columns:
            return df
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

df = load_data()

# -----------------------------
# QUICK ACCESS AI TERMINAL (FLOATING)
# -----------------------------
with st.popover("🔍"):
    st.markdown("""
    <div style='border-bottom: 1px solid rgba(56, 189, 248, 0.2); padding-bottom: 10px; margin-bottom: 12px;'>
        <span style='color: #38BDF8; font-weight: 800; letter-spacing: 2px; font-size: 1.0em;'>TACTICAL AI ASSISTANT</span><br>
        <span style='font-size: 0.82em; color: #94A3B8; letter-spacing: 0.5px;'>Submit text or voice commands to interrogate live signal and optical data.</span>
    </div>
    """, unsafe_allow_html=True)

    chat_container = st.container(height=300)
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_container.markdown(
                f"<div style='margin-bottom:10px;'><span style='color:#94A3B8; font-size:0.8em; letter-spacing:1px;'>YOU</span><br>"
                f"<span style='color:#F8FAFC; font-weight:600;'>{msg['content']}</span></div>",
                unsafe_allow_html=True
            )
        else:
            chat_container.markdown(
                f"<div style='margin-bottom:10px; padding:8px 10px; background:rgba(56,189,248,0.06); border-left:3px solid #38BDF8; border-radius:4px;'>"
                f"<span style='color:#38BDF8; font-size:0.8em; letter-spacing:1px;'>TACTICAL AI</span><br>"
                f"<span style='color:#BAE6FD;'>{msg['content']}</span></div>",
                unsafe_allow_html=True
            )

    with st.form(key="ai_chat_form", clear_on_submit=True):
        user_input = st.text_input("Query intel...", placeholder="e.g. sitrep, threats, camera status", label_visibility="collapsed")
        submitted = st.form_submit_button("SEND ▶", use_container_width=True)
        if submitted and user_input.strip():
            query = user_input.strip()
            hist_df = pd.DataFrame(st.session_state.history) if st.session_state.history else None
            current_tracks = hist_df.drop_duplicates(subset=['Transmitter ID'], keep='last').copy() if hist_df is not None else None
            st.session_state.chat_history.append({"role": "user", "content": query})
            resp = tactical_ai_response(query, current_tracks, st.session_state.cv_events)
            st.session_state.chat_history.append({"role": "assistant", "content": resp})
            st.rerun()

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    audio_val = st.audio_input("🎙 Voice command")
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
                    st.session_state.chat_history.append({"role": "user", "content": f"[VOICE] {text}"})
                    resp = tactical_ai_response(text, current_tracks, st.session_state.cv_events)
                    st.session_state.chat_history.append({"role": "assistant", "content": resp})
                    st.rerun()
            except sr.UnknownValueError:
                st.warning("Audio unintelligible. Please speak clearer.")
            except Exception as e:
                st.error(f"Audio Decode Error: {e}")


# -----------------------------
# Sidebar Configuration
# -----------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-section-label'>SYSTEM MODES</div>", unsafe_allow_html=True)

    if st.button(
        "RF SIGNAL ANALYZER",
        use_container_width=True,
        type="primary" if st.session_state.app_mode == "RF SIGNAL ANALYZER" else "secondary"
    ):
        st.session_state.app_mode = "RF SIGNAL ANALYZER"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    if st.button(
        "OPTICAL SURVEILLANCE",
        use_container_width=True,
        type="primary" if st.session_state.app_mode == "OPTICAL SURVEILLANCE" else "secondary"
    ):
        st.session_state.app_mode = "OPTICAL SURVEILLANCE"
        st.rerun()

    st.markdown("<div class='sidebar-section-label' style='margin-top:28px;'>COMMAND INTERFACE</div>", unsafe_allow_html=True)

    speed = st.slider("SWEEP INTERVAL (Seconds)", 0.2, 3.0, 1.0, 0.1)

    if st.session_state.app_mode == "RF SIGNAL ANALYZER":
        if st.button("BEGIN RF SURVEILLANCE", use_container_width=True, type="primary"):
            st.session_state.rf_running = True
        if st.button("PAUSE RF TRACKING", use_container_width=True):
            st.session_state.rf_running = False

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button("PURGE RF DATA", use_container_width=True):
            st.session_state.rf_running = False
            st.session_state.index = 0
            st.session_state.history = []
            st.session_state.scores = []
            st.session_state.waterfall_grid = np.zeros((30, 100))
            st.rerun()
    else:
        if st.button("INITIALIZE CAMERA FEED", use_container_width=True, type="primary"):
            st.session_state.cv_running = True
        if st.button("PAUSE CAMERA FEED", use_container_width=True):
            st.session_state.cv_running = False

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button("PURGE OPTICAL LOGS", use_container_width=True):
            st.session_state.cv_running = False
            st.session_state.cv_events = []
            st.session_state.cv_loiter_start = None
            st.rerun()


# -----------------------------
# Processing Logic
# -----------------------------
signal = None
active_tracks = None

if st.session_state.rf_running:
    if len(df) == 0:
        st.session_state.rf_running = False
        if st.session_state.app_mode == "RF SIGNAL ANALYZER":
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
    row["velocity_ms"] = float(row.get("velocity_ms", 0))
    row["altitude_m"] = float(row.get("altitude_m", 0))

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


# ─────────────────────────────────────────────
# MODE: RF SIGNAL ANALYZER
# ─────────────────────────────────────────────
if st.session_state.app_mode == "RF SIGNAL ANALYZER":
    st.markdown("""
    <div class="main-header">
        <h1>RF SIGNAL ANALYZER</h1>
    </div>
    """, unsafe_allow_html=True)

    signal = st.session_state.history[-1] if st.session_state.history else None

    if signal is None:
        st.info("System Paused. Press BEGIN RF SURVEILLANCE in the sidebar to initiate scanning.")
    else:
        hist_df = pd.DataFrame(st.session_state.history)
        active_tracks = hist_df.drop_duplicates(subset=['Transmitter ID'], keep='last').copy()

        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.metric("Latest Threat Score", f"{signal['Threat Score']}%")
        with m2:
            st.metric("Total Active Tracks", len(active_tracks))
        with m3:
            st.metric("Hostile Targets", len(active_tracks[active_tracks["Classification"] == "Hostile"]))
        with m4:
            st.metric("Peak Velocity", f"{signal['velocity_ms']} m/s")
        with m5:
            st.metric("Tactical Altitude", f"{int(signal['altitude_m'])} m")

        # --- BATTLESPACE AI OVERVIEW ---
        global_ai_text = generate_global_ai_analysis(active_tracks)
        st.markdown(
            f"<div style='background:rgba(239,68,68,0.08); border-left:3px solid #EF4444; padding:14px 18px;"
            f" margin-top:18px; margin-bottom:18px; border-radius:6px;"
            f" box-shadow:0 0 12px rgba(239,68,68,0.12);'>"
            f"<div style='color:#EF4444; font-weight:800; font-size:0.78em; letter-spacing:2.5px; margin-bottom:6px;'>BATTLESPACE AI OVERVIEW</div>"
            f"<div style='color:#FCA5A5; font-size:0.93em; line-height:1.6; font-weight:500;'>{global_ai_text}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2, tab3, tab4 = st.tabs([
            "BATTLESPACE RADAR",
            "ELECTRONIC INTELLIGENCE",
            "THREAT HISTORICS",
            "C2 NETWORK TOPOLOGY"
        ])

        # ── Tab 1: Radar ──────────────────────────
        with tab1:
            col_radar, col_orbat = st.columns([1, 1.2])
            with col_radar:
                st.markdown(
                    "<div class='module-header'>"
                    "<span class='module-tag'>RADAR</span>"
                    "TACTICAL SITREP"
                    "</div>",
                    unsafe_allow_html=True
                )
                sectors = np.arange(0, 360, 45)
                sector_colors = []
                for s in sectors:
                    in_sector = active_tracks[(active_tracks["bearing_deg"] >= s) & (active_tracks["bearing_deg"] < s + 45)]
                    max_threat = in_sector["Threat Score"].max() if not in_sector.empty else 0
                    if max_threat >= 70:
                        sector_colors.append("rgba(239, 68, 68, 0.25)")
                    elif max_threat >= 40:
                        sector_colors.append("rgba(250, 204, 21, 0.20)")
                    else:
                        sector_colors.append("rgba(30, 58, 138, 0.12)")

                fig = go.Figure(go.Barpolar(
                    r=[300]*8, theta=sectors + 22.5, width=[44.5]*8,
                    marker_color=sector_colors, marker_line_color="#1E3A8A",
                    marker_line_width=1, opacity=0.8, hoverinfo="none"
                ))

                if not active_tracks.empty:
                    symbols = active_tracks["Classification"].map({
                        "Hostile": "diamond-open", "Unknown": "square-open", "Friendly": "circle-open"
                    }).tolist()
                    fig.add_trace(go.Scatterpolar(
                        r=active_tracks["distance_km"], theta=active_tracks["bearing_deg"],
                        mode="markers+text",
                        marker=dict(color=active_tracks["color"], size=14, symbol=symbols,
                                    line=dict(color=active_tracks["color"], width=2)),
                        text=active_tracks["Transmitter ID"].str[-4:],
                        textposition="top right",
                        textfont=dict(color="#7DD3FC", size=10),
                        hovertext=active_tracks["Platform ID"] + "<br>Range: " + active_tracks["distance_km"].astype(str) + " km",
                        hoverinfo="text"
                    ))

                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 300], gridcolor="rgba(30,58,138,0.4)",
                                        gridwidth=1, tickfont=dict(color="#38BDF8", size=9), dtick=50, angle=90),
                        angularaxis=dict(direction="clockwise", rotation=90, gridcolor="rgba(30,58,138,0.4)",
                                         gridwidth=1, tickfont=dict(color="#94A3B8", size=11, family="Inter"),
                                         tickmode="array", tickvals=np.arange(0, 360, 45),
                                         ticktext=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
                        bgcolor="#01040A"
                    ),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=30, b=30, l=30, r=30), height=400, showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("""
                <div class='legend-row'>
                    <div><span class='legend-sq' style='background:rgba(239,68,68,0.7);'></span> HIGH THREAT (Score 70+)</div>
                    <div><span class='legend-sq' style='background:rgba(250,204,21,0.7);'></span> ELEVATED RISK (40-69)</div>
                    <div><span class='legend-sq' style='background:rgba(30,58,138,0.6);'></span> CLEAR / ROUTINE (&lt;40)</div>
                </div>
                """, unsafe_allow_html=True)

            with col_orbat:
                st.markdown(
                    "<div class='module-header'>"
                    "<span class='module-tag'>EOB</span>"
                    "ACTIVE THREAT DATABASE"
                    "</div>",
                    unsafe_allow_html=True
                )
                display_tracks = active_tracks[[
                    "Transmitter ID", "Classification", "Confidence",
                    "Platform ID", "frequency_mhz", "velocity_ms", "altitude_m", "Threat Score"
                ]].copy()
                display_tracks["Confidence"] = display_tracks["Confidence"].apply(lambda x: f"{x:.1f}%")
                display_tracks = display_tracks.sort_values(by="Threat Score", ascending=False)
                st.dataframe(display_tracks, use_container_width=True, hide_index=True, height=420)
        # ── Tab 2: ELINT ──────────────────────────
        with tab2:
            st.markdown(
                "<div class='module-header'>"
                "<span class='module-tag'>SDR</span>"
                "LIVE WATERFALL SPECTROGRAM"
                "</div>",
                unsafe_allow_html=True
            )
            tactical_colors = [
                [0.0, 'rgb(0,0,0)'],
                [0.1, 'rgb(0,20,50)'],
                [0.4, 'rgb(0,80,200)'],
                [0.7, 'rgb(0,200,255)'],
                [0.9, 'rgb(255,255,255)'],
                [1.0, 'rgb(255,255,100)']
            ]
            fig_wf = go.Figure(data=go.Heatmap(
                z=st.session_state.waterfall_grid,
                colorscale=tactical_colors,
                zmin=-120, zmax=-40,
                showscale=False
            ))
            fig_wf.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(showticklabels=False, showgrid=False),
                yaxis=dict(showticklabels=False, autorange='reversed', showgrid=False),
                height=360
            )
            st.plotly_chart(fig_wf, use_container_width=True)
            st.markdown("""
            <div class='legend-row'>
                <div><span class='legend-sq' style='background:rgb(255,255,100); width:12px; height:4px; border-radius:2px;'></span> PEAK EMISSION</div>
                <div><span class='legend-sq' style='background:rgb(0,200,255); width:12px; height:4px; border-radius:2px;'></span> ACTIVE RF SIGNAL</div>
                <div><span class='legend-sq' style='background:rgb(0,20,50); width:12px; height:4px; border-radius:2px; border:1px solid #1E3A8A;'></span> NOISE FLOOR</div>
            </div>
            """, unsafe_allow_html=True)

            col_details, col_elint = st.columns([1.5, 1])
            with col_details:
                c = signal["Classification"]
                badge_class = f"badge-{c.lower()}"
                st.markdown(
                    "<div class='glass-box'>"
                    "<div class='module-header'>"
                    "<span class='module-tag'>REPORT</span>"
                    "INTERCEPT ANALYSIS"
                    "</div>"
                    f'<div style="margin-bottom:18px;"><span class="{badge_class}">STATUS: {c} &nbsp;|&nbsp; {signal["Confidence"]:.1f}% MATCH</span></div>'
                    f"<div style='margin-bottom:8px;'><b>Identified Platform:</b><br><span style='color:#FFFFFF; font-size:1.05em;'>{signal['Platform ID']}</span></div>"
                    "<div style='height:10px;'></div>"
                    f"<div><b>Target Action Recommendation:</b><br><span style='color:#38BDF8;'>{signal['Recommendation']}</span></div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            with col_elint:
                elint_text = "<br>".join([
                    f"Frequency : {signal['frequency_mhz']} MHz",
                    f"Bandwidth : {signal['bandwidth_khz']} kHz",
                    f"Doppler   : {signal['doppler_shift_hz']} Hz",
                    f"Power Rx  : {signal['power_dbm']} dBm",
                    f"Velocity  : {signal['velocity_ms']} m/s",
                    f"Altitude  : {int(signal['altitude_m'])} m",
                    ""
                ] + [line for line in signal['ELINT Details'].split(' | ')])
                st.markdown(
                    "<div class='glass-box'>"
                    "<div class='module-header'>"
                    "<span class='module-tag'>ELINT</span>"
                    "SYSTEM LOGS"
                    "</div>"
                    f"<div class='elint-log'>{elint_text}</div>"
                    "</div>",
                    unsafe_allow_html=True
                )

        # ── Tab 3: Historics ──────────────────────
        with tab3:
            st.markdown(
                "<div class='module-header'>"
                "<span class='module-tag'>TIMELINE</span>"
                "HISTORICAL THREAT TRACKING"
                "</div>",
                unsafe_allow_html=True
            )
            trend_df = pd.DataFrame({
                "Time": range(len(st.session_state.scores)),
                "Threat Score": st.session_state.scores
            })
            line_fig = px.area(
                trend_df, x="Time", y="Threat Score",
                template="plotly_dark",
                color_discrete_sequence=["#38BDF8"]
            )
            line_fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(30,58,138,0.3)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(30,58,138,0.3)', range=[0, 100]),
                height=540
            )
            st.plotly_chart(line_fig, use_container_width=True)
        # ── Tab 4: C2 Topology ───────────────────
        with tab4:
            st.markdown(
                "<div class='module-header'>"
                "<span class='module-tag'>C2 NET</span>"
                "NETWORK TOPOLOGY MAP"
                "</div>",
                unsafe_allow_html=True
            )
            if not active_tracks.empty and len(active_tracks) > 1:
                nodes = active_tracks.copy()
                nodes['x'] = nodes['distance_km'] * np.cos(np.radians(nodes['bearing_deg']))
                nodes['y'] = nodes['distance_km'] * np.sin(np.radians(nodes['bearing_deg']))

                edge_x, edge_y = [], []
                node_connections = {i: 0 for i in range(len(nodes))}
                node_ids = list(nodes.index)

                for i in range(len(node_ids)):
                    for j in range(i + 1, len(node_ids)):
                        idx1, idx2 = node_ids[i], node_ids[j]
                        f1 = nodes.loc[idx1, 'frequency_mhz']
                        f2 = nodes.loc[idx2, 'frequency_mhz']
                        dx = nodes.loc[idx1, 'x'] - nodes.loc[idx2, 'x']
                        dy = nodes.loc[idx1, 'y'] - nodes.loc[idx2, 'y']
                        dist = np.sqrt(dx**2 + dy**2)
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
                        node_texts.append("[ COMMAND NODE ]")
                    else:
                        node_texts.append(nodes.loc[idx, 'Platform ID'])

                fig_net = go.Figure()

                if len(edge_x) > 0:
                    fig_net.add_trace(go.Scatter(
                        x=edge_x, y=edge_y,
                        line=dict(width=1.5, color='rgba(56, 189, 248, 0.35)'),
                        mode='lines', hoverinfo='none', showlegend=False
                    ))

                symbols_net = nodes["Classification"].map({
                    "Hostile": "diamond", "Unknown": "square", "Friendly": "circle"
                }).tolist()

                fig_net.add_trace(go.Scatter(
                    x=nodes['x'], y=nodes['y'],
                    mode='markers+text',
                    marker=dict(size=node_sizes, color=nodes["color"],
                                symbol=symbols_net, line=dict(width=2, color="#FFFFFF")),
                    text=node_texts,
                    textposition="top center",
                    textfont=dict(color="#F8FAFC", size=11, family="Inter"),
                    hovertext=nodes['Transmitter ID'] + "<br>Freq: " + nodes['frequency_mhz'].astype(str) + " MHz<br>Links: " + pd.Series(node_connections).astype(str).values,
                    hoverinfo='text',
                    showlegend=False
                ))

                fig_net.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=10, b=0),
                    xaxis=dict(showgrid=True, gridcolor='rgba(30,58,138,0.2)',
                               zeroline=True, zerolinecolor='rgba(56,189,248,0.4)',
                               showticklabels=False, title=''),
                    yaxis=dict(showgrid=True, gridcolor='rgba(30,58,138,0.2)',
                               zeroline=True, zerolinecolor='rgba(56,189,248,0.4)',
                               showticklabels=False, title=''),
                    height=580, showlegend=False
                )
                st.plotly_chart(fig_net, use_container_width=True)
                st.markdown("""
                <div class='legend-row'>
                    <div><span class='legend-dot' style='background:#EF4444;'></span> HOSTILE NODE</div>
                    <div><span class='legend-dot' style='background:#1E3A8A;'></span> FRIENDLY NODE</div>
                    <div><span class='legend-dot' style='background:#FACC15;'></span> UNKNOWN NODE</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Insufficient tracks or tactical proximity to map C2 Topology Network.")


# ─────────────────────────────────────────────
# MODE: OPTICAL SURVEILLANCE
# ─────────────────────────────────────────────
elif st.session_state.app_mode == "OPTICAL SURVEILLANCE":
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
                        alert_msg = f"[{time.strftime('%X')}] LOITERING ALERT: SUSPECT IN FRAME > 10s"
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
                    cv2.putText(annotated_frame, "HIGH ALERT: LOITERING!", (30, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)

                weapon_detected = any(obj for obj in detected_crit_objects if "KNIFE" in obj or "GUN" in obj or "WEAPON" in obj)
                if weapon_detected:
                    cv2.putText(annotated_frame, "HIGH ALERT: WEAPON DETECTED!", (30, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)

                st.session_state.cv_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

    # Critical loitering warning banner
    is_loitering = any("LOITERING ALERT" in event for event in st.session_state.cv_events[:5])
    if is_loitering:
        st.error("CRITICAL WARNING: Active Suspect Loitering Detected (>10 seconds in frame)")
        # ── Loitering KLAXON: maximum-harshness Web Audio API alarm ──
        components.html("""
        <script>
        (function() {
            var COOLDOWN = 4500;
            var last = parseInt(sessionStorage.getItem('loiterAlarm') || '0');
            var now  = Date.now();
            if (now - last < COOLDOWN) return;
            sessionStorage.setItem('loiterAlarm', now.toString());

            try {
                var ctx = new (window.AudioContext || window.webkitAudioContext)();
                var T   = ctx.currentTime;

                // ── Hard-clip distortion curve ────────────────────────────
                function mkDist(amt) {
                    var c = new Float32Array(1024);
                    for (var i = 0; i < 1024; i++) {
                        var x = (i * 2) / 1024 - 1;
                        c[i] = ((Math.PI + amt) * x) / (Math.PI + amt * Math.abs(x));
                    }
                    return c;
                }

                // ── Two distortion stages in series ───────────────────────
                var dist1 = ctx.createWaveShaper();
                dist1.curve = mkDist(900); dist1.oversample = '4x';
                var dist2 = ctx.createWaveShaper();
                dist2.curve = mkDist(600); dist2.oversample = '4x';
                dist1.connect(dist2);

                // ── Master gain ───────────────────────────────────────────
                var master = ctx.createGain();
                master.gain.setValueAtTime(0.0, T);
                dist2.connect(master);
                master.connect(ctx.destination);

                // ── Ring modulator (carrier × modulator = metallic screech)
                var ringMod  = ctx.createOscillator();  // modulator
                var ringGain = ctx.createGain();
                ringMod.type = 'sawtooth';
                ringMod.frequency.value = 97;            // inharmonic prime
                ringGain.gain.value = 1.0;
                ringMod.connect(ringGain);
                ringGain.connect(master.gain);           // AM the master
                ringMod.start(T); ringMod.stop(T + 3.5);

                // ── 16 Hz LFO rapid stutter ───────────────────────────────
                var lfo = ctx.createOscillator();
                var lfoG = ctx.createGain();
                lfo.type = 'square';
                lfo.frequency.value = 16;
                lfoG.gain.value = 0.65;
                lfo.connect(lfoG);
                lfoG.connect(master.gain);
                lfo.start(T); lfo.stop(T + 3.5);

                // ── Oscillator layer factory ──────────────────────────────
                function osc(type, det, startT, stopT, vol) {
                    var o = ctx.createOscillator();
                    var g = ctx.createGain();
                    o.type = type; o.detune.value = det;
                    g.gain.setValueAtTime(vol, T);
                    o.connect(g); g.connect(dist1);
                    o.start(T + startT); o.stop(T + stopT);
                    return o;
                }

                // ── Sub-bass rumble layer (adds physical shock) ───────────
                function bass(startT, stopT) {
                    var b = ctx.createOscillator();
                    var g = ctx.createGain();
                    b.type = 'sawtooth'; b.frequency.value = 55;
                    g.gain.setValueAtTime(0.9, T);
                    b.connect(g); g.connect(dist1);
                    b.start(T + startT); b.stop(T + stopT);
                }

                // ── Screech sweep (200 Hz → 3200 Hz → 250 Hz) ────────────
                function screech(startT, dur) {
                    // 5 detuned layers: 3 sawtooth + square + triangle
                    var detunes  = [0, +18, -18, +35, -35];
                    var types    = ['sawtooth','sawtooth','sawtooth','square','triangle'];
                    var vols     = [0.70, 0.55, 0.55, 0.65, 0.40];
                    detunes.forEach(function(det, idx) {
                        var o = osc(types[idx], det, startT, startT + dur, vols[idx]);
                        o.frequency.setValueAtTime(200,  T + startT);
                        o.frequency.exponentialRampToValueAtTime(3200,
                            T + startT + dur * 0.42);
                        o.frequency.exponentialRampToValueAtTime(250,
                            T + startT + dur);
                    });
                    bass(startT, startT + dur);
                }

                // ── Klaxon bark: rapid descending thud ───────────────────
                function bark(startT) {
                    var o = osc('square', 0, startT, startT + 0.07, 0.95);
                    o.frequency.setValueAtTime(1200, T + startT);
                    o.frequency.exponentialRampToValueAtTime(120, T + startT + 0.07);
                    // parallel sawtooth for extra grit
                    var o2 = osc('sawtooth', +25, startT, startT + 0.07, 0.75);
                    o2.frequency.setValueAtTime(1400, T + startT);
                    o2.frequency.exponentialRampToValueAtTime(100, T + startT + 0.07);
                }

                // ── SEQUENCE (3 seconds total) ────────────────────────────
                // Burst 1 screech sweep
                screech(0.00, 0.80);
                // Rapid bark cluster 1 (every 55ms)
                for (var i = 0; i < 5; i++) bark(0.85 + i * 0.055);
                // Burst 2 screech sweep
                screech(1.20, 0.80);
                // Rapid bark cluster 2
                for (var j = 0; j < 5; j++) bark(2.05 + j * 0.055);
                // Kill shot – final single long screech descend
                screech(2.40, 0.50);

                // ── Master envelope ───────────────────────────────────────
                master.gain.setValueAtTime(0.85, T + 0.01);
                master.gain.setValueAtTime(0.85, T + 2.88);
                master.gain.linearRampToValueAtTime(0.0, T + 3.10);

            } catch(e) {}
        })();
        </script>
        """, height=0)

    st.markdown(
        "<div class='glass-box'>"
        "<div class='module-header'>"
        "<span class='module-tag'>CAM</span>"
        "LIVE CV SECTOR OVERLOOK"
        "</div>",
        unsafe_allow_html=True
    )

    col_video, col_logs = st.columns([1.5, 1])
    with col_video:
        if st.session_state.cv_frame is not None:
            st.image(st.session_state.cv_frame, use_container_width=True)
        else:
            st.info("Awaiting Camera Initialization. Press INITIALIZE CAMERA FEED in the sidebar.")
    with col_logs:
        st.markdown(
            "<div style='color:#38BDF8; font-size:0.78em; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;'>OPTICAL EVENT LOG</div>",
            unsafe_allow_html=True
        )
        if not st.session_state.cv_events:
            st.markdown("<div class='elint-log'>No tactical optical alerts detected.</div>", unsafe_allow_html=True)
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
