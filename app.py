import streamlit as st
import requests
import base64
import json
import os
import time
import urllib.parse
from io import BytesIO
from PIL import Image
from datetime import datetime
from pathlib import Path

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Lumina — Turn Words Into Light",
    page_icon="💫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# LOGO — Lumina Radiant Sun (Teal/Violet/Magenta)
# =========================

LOGO_SVG = """
<svg viewBox="0 0 720 240" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="sunGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f0fdff"/>
      <stop offset="25%" stop-color="#22d3ee"/>
      <stop offset="60%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#e879f9"/>
    </radialGradient>
    <linearGradient id="rayGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#22d3ee"/>
      <stop offset="100%" stop-color="#e879f9"/>
    </linearGradient>
    <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22D3EE"/>
      <stop offset="50%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#E879F9"/>
    </linearGradient>
    <filter id="sunGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="720" height="240" fill="#060a13" rx="24"/>

  <g transform="translate(120, 120)">
    <circle cx="0" cy="0" r="95" fill="#22d3ee" opacity="0.12"/>

    <g stroke="url(#rayGrad)" stroke-width="4" stroke-linecap="round" opacity="0.85">
      <line x1="0" y1="-82" x2="0" y2="-60"/>
      <line x1="0" y1="82"  x2="0" y2="60"/>
      <line x1="-82" y1="0" x2="-60" y2="0"/>
      <line x1="82"  y1="0" x2="60" y2="0"/>
      <line x1="-58" y1="-58" x2="-42" y2="-42"/>
      <line x1="58"  y1="-58" x2="42" y2="-42"/>
      <line x1="-58" y1="58"  x2="-42" y2="42"/>
      <line x1="58"  y1="58"  x2="42" y2="42"/>
      <line x1="-30" y1="-76" x2="-22" y2="-56"/>
      <line x1="30"  y1="-76" x2="22"  y2="-56"/>
      <line x1="-76" y1="-30" x2="-56" y2="-22"/>
      <line x1="-76" y1="30"  x2="-56" y2="22"/>
      <line x1="76"  y1="-30" x2="56"  y2="-22"/>
      <line x1="76"  y1="30"  x2="56"  y2="22"/>
      <line x1="-30" y1="76"  x2="-22" y2="56"/>
      <line x1="30"  y1="76"  x2="22"  y2="56"/>
    </g>

    <circle cx="0" cy="0" r="52" fill="url(#sunGrad)" filter="url(#sunGlow)"/>
    <circle cx="0" cy="0" r="44" fill="none" stroke="#ffffff" stroke-opacity="0.25" stroke-width="1.5"/>
    <circle cx="0" cy="0" r="14" fill="#ffffff" opacity="0.95"/>
  </g>

  <text x="245" y="132"
        font-family="'Inter','Segoe UI',Arial,Helvetica,sans-serif"
        font-size="80" font-weight="900"
        fill="url(#textGrad)"
        letter-spacing="-3">Lumina</text>

  <text x="250" y="176"
        font-family="'Inter','Segoe UI',Arial,Helvetica,sans-serif"
        font-size="15" font-weight="500"
        fill="#94a3c8"
        letter-spacing="3">TURN WORDS INTO LIGHT</text>

  <circle cx="530" cy="124" r="6" fill="#E879F9" opacity="0.95"/>
</svg>
"""

ICON_SVG = """
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="sunGrad2" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f0fdff"/>
      <stop offset="25%" stop-color="#22d3ee"/>
      <stop offset="60%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#e879f9"/>
    </radialGradient>
    <linearGradient id="rayGrad2" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#22d3ee"/>
      <stop offset="100%" stop-color="#e879f9"/>
    </linearGradient>
    <filter id="sunGlow2" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="200" height="200" rx="44" fill="#060a13"/>
  <circle cx="100" cy="100" r="88" fill="#22d3ee" opacity="0.12"/>
  <g stroke="url(#rayGrad2)" stroke-width="4" stroke-linecap="round" opacity="0.85">
    <line x1="100" y1="22" x2="100" y2="40"/>
    <line x1="100" y1="178" x2="100" y2="160"/>
    <line x1="22" y1="100" x2="40" y2="100"/>
    <line x1="178" y1="100" x2="160" y2="100"/>
    <line x1="45" y1="45" x2="58" y2="58"/>
    <line x1="155" y1="45" x2="142" y2="58"/>
    <line x1="45" y1="155" x2="58" y2="142"/>
    <line x1="155" y1="155" x2="142" y2="142"/>
  </g>
  <circle cx="100" cy="100" r="46" fill="url(#sunGrad2)" filter="url(#sunGlow2)"/>
  <circle cx="100" cy="100" r="38" fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1.5"/>
  <circle cx="100" cy="100" r="12" fill="#ffffff" opacity="0.95"/>
</svg>
"""


def svg_to_data_uri(svg_string: str) -> str:
    encoded = base64.b64encode(svg_string.strip().encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


LOGO_DATA_URI = svg_to_data_uri(LOGO_SVG)
ICON_DATA_URI = svg_to_data_uri(ICON_SVG)

# =========================
# STORAGE
# =========================

HISTORY_FILE = Path("history.json")
THUMBNAIL_DIR = Path("thumbnails")
THUMBNAIL_DIR.mkdir(exist_ok=True)
SETTINGS_FILE = Path("settings.json")

DEFAULT_SETTINGS = {
    "quality": "High",
    "aspect_ratio": "Square (1:1)",
    "resolution": "1024 × 1024",
    "image_format": "PNG",
}


def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_history(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def save_thumbnail(image, entry_id):
    try:
        thumb = image.copy()
        thumb.thumbnail((300, 300))
        path = THUMBNAIL_DIR / f"{entry_id}.jpg"
        thumb.convert("RGB").save(path, format="JPEG", quality=80)
        return str(path)
    except Exception:
        return ""


def add_history_entry(image, prompt, provider, quality, width, height):
    entry_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    thumb_path = save_thumbnail(image, entry_id)
    entry = {
        "id": entry_id,
        "timestamp": datetime.now().strftime("%b %d, %Y · %H:%M"),
        "prompt": prompt,
        "provider": provider,
        "quality": quality,
        "width": width,
        "height": height,
        "thumbnail": thumb_path,
    }
    history = load_history()
    history.insert(0, entry)
    history = history[:50]
    save_history(history)
    return entry


def delete_history_entry(entry_id):
    history = load_history()
    history = [h for h in history if h["id"] != entry_id]
    save_history(history)
    thumb = THUMBNAIL_DIR / f"{entry_id}.jpg"
    if thumb.exists():
        try:
            thumb.unlink()
        except Exception:
            pass


def clear_history():
    history = load_history()
    for entry in history:
        thumb = Path(entry.get("thumbnail", ""))
        if thumb.exists():
            try:
                thumb.unlink()
            except Exception:
                pass
    save_history([])


def load_settings():
    if not SETTINGS_FILE.exists():
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        merged = DEFAULT_SETTINGS.copy()
        merged.update(data)
        return merged
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings_file(settings):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except Exception:
        pass


# =========================
# SESSION STATE
# =========================

if "settings" not in st.session_state:
    st.session_state.settings = load_settings()
if "settings_saved_msg" not in st.session_state:
    st.session_state.settings_saved_msg = False
if "settings_reset_msg" not in st.session_state:
    st.session_state.settings_reset_msg = False
if "settings_version" not in st.session_state:
    st.session_state.settings_version = 0

# =========================
# CSS — Teal / Violet / Magenta
# =========================

st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at 15% 5%, #22d3ee11 0%, transparent 45%),
            radial-gradient(circle at 85% 95%, #e879f911 0%, transparent 45%),
            linear-gradient(180deg, #060a13 0%, #0f0c29 100%);
        background-attachment: fixed;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}

    /* Hero */
    .hero {
        display: flex;
        justify-content: center;
        padding: 1rem 0 0.4rem 0;
    }
    .hero img {
        width: 100%;
        max-width: 420px;
        height: auto;
        filter: drop-shadow(0 20px 50px rgba(34, 211, 238, 0.35));
    }

    /* Description block */
    .desc-block {
        text-align: center;
        max-width: 640px;
        margin: 0.5rem auto 1.2rem auto;
        padding: 0 1rem;
    }
    .desc-tagline {
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(90deg, #22d3ee, #8b5cf6, #e879f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .desc-text {
        color: #94a3c8;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1220 0%, #121426 100%);
        border-right: 1px solid rgba(34, 211, 238, 0.12);
    }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #22d3ee; }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div { color: #c8d4e8; }
    section[data-testid="stSidebar"] small,
    section[data-testid="stSidebar"] .stCaption { color: #7a8bb0 !important; }

    section[data-testid="stSidebar"] button[data-baseweb="tab"] {
        background: transparent !important; color: #7a8bb0 !important;
        font-weight: 600 !important; font-size: 0.82rem !important;
        padding: 0.5rem 0.6rem !important; border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] button[data-baseweb="tab"][aria-selected="true"] {
        color: #22d3ee !important; background: rgba(34, 211, 238, 0.1) !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="tab-list"] {
        background: rgba(15, 17, 21, 0.6) !important;
        border: 1px solid rgba(34, 211, 238, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.25rem !important;
        gap: 0.15rem !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="tab-highlight"] { display: none !important; }
    section[data-testid="stSidebar"] div[data-baseweb="tab-border"] { display: none !important; }

    .side-brand {
        display: flex; align-items: center; gap: 0.7rem;
        padding: 0.4rem 0.3rem 1.2rem 0.3rem;
        border-bottom: 1px solid rgba(34, 211, 238, 0.15);
        margin-bottom: 1rem;
    }
    .side-logo {
        width: 38px; height: 38px;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 14px rgba(34, 211, 238, 0.45);
    }
    .side-logo img { width: 38px; height: 38px; display: block; }
    .side-brand-text h3 {
        font-size: 1rem; font-weight: 800; margin: 0; line-height: 1.1;
        background: linear-gradient(90deg, #22D3EE, #8B5CF6, #E879F9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.3px;
    }
    .side-brand-text p {
        font-size: 0.62rem; color: #7a8bb0; margin: 1px 0 0 0;
        letter-spacing: 0.6px;
    }

    /* Main buttons */
    .stButton > button {
        background: linear-gradient(135deg, #22d3ee 0%, #8b5cf6 100%);
        color: #060a13; border: none; border-radius: 12px;
        padding: 0.9rem 1.6rem; font-weight: 800; font-size: 0.95rem;
        transition: all 0.3s ease; width: 100%;
        box-shadow: 0 4px 22px rgba(34, 211, 238, 0.4);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #e879f9 100%);
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.6);
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: #111827 !important;
        color: #c8d4e8 !important;
        border: 1px solid #1f2937 !important;
        box-shadow: none !important;
        padding: 0.55rem 1rem !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        transform: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        border-color: #22d3ee !important;
        color: #22d3ee !important;
        background: #1a2332 !important;
    }

    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(34, 211, 238, 0.3) !important;
        border-radius: 14px !important;
        color: #e0e0e8 !important;
        font-size: 1rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #22d3ee !important;
        box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.2) !important;
    }

    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(34, 211, 238, 0.25) !important;
        border-radius: 10px !important;
        color: #e0e0e8 !important;
    }

    div[data-testid="stImage"] img {
        border-radius: 16px;
        border: 1px solid rgba(34, 211, 238, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
    }

    .chips-row {
        display: flex; gap: 0.5rem; flex-wrap: wrap;
        margin-top: 1rem; justify-content: center;
    }
    .chip {
        display: inline-flex; align-items: center; gap: 0.4rem;
        padding: 0.35rem 0.85rem;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(34, 211, 238, 0.25);
        border-radius: 999px;
        font-size: 0.75rem; color: #94a3c8; font-weight: 500;
    }
    .chip strong { color: #e0e0e8; font-weight: 700; }

    .scanning {
        padding: 2.5rem;
        background: rgba(34, 211, 238, 0.05);
        border: 1px dashed rgba(34, 211, 238, 0.35);
        border-radius: 20px; text-align: center;
        position: relative; overflow: hidden;
    }
    .scanning::before {
        content: ""; position: absolute;
        top: 0; left: -100%; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, #22d3ee, transparent);
        animation: scanline 2s linear infinite;
    }
    @keyframes scanline { 0% { left: -100%; } 100% { left: 100%; } }
    .scanning-icon {
        font-size: 2.8rem;
        animation: pulse 1.6s ease-in-out infinite;
        display: inline-block;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.15); opacity: 0.7; }
    }
    .scanning-label {
        color: #22d3ee; font-size: 0.85rem; letter-spacing: 3px;
        text-transform: uppercase; font-weight: 700; margin-top: 1rem;
    }

    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
    }
    .empty-state-icon { font-size: 3rem; opacity: 0.4; margin-bottom: 1rem; }
    .empty-state-title { font-size: 1rem; color: #64748b; font-weight: 500; }

    .result-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 0.8rem 1rem;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(34, 211, 238, 0.2);
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    .result-header-title {
        font-size: 0.72rem; color: #94a3c8;
        letter-spacing: 2px; text-transform: uppercase;
        font-weight: 700;
    }
    .result-header-meta { font-size: 0.72rem; color: #7a8bb0; }
    .result-header-dot {
        width: 8px; height: 8px;
        background: #22d3ee; border-radius: 50%;
        box-shadow: 0 0 10px #22d3ee;
        display: inline-block; margin-right: 0.5rem;
    }

    .hist-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(34, 211, 238, 0.15);
        border-radius: 12px;
        padding: 0.7rem;
        margin-bottom: 0.6rem;
        display: flex;
        gap: 0.7rem;
        align-items: flex-start;
    }
    .hist-card img {
        width: 54px; height: 54px;
        border-radius: 8px;
        object-fit: cover;
        border: 1px solid rgba(34, 211, 238, 0.2);
        flex-shrink: 0;
    }
    .hist-meta { flex: 1; min-width: 0; }
    .hist-time { font-size: 0.68rem; color: #7a8bb0; font-weight: 600; margin-bottom: 0.2rem; }
    .hist-prompt {
        font-size: 0.78rem; color: #c8d4e8; line-height: 1.4;
        display: -webkit-box; -webkit-line-clamp: 2;
        -webkit-box-orient: vertical; overflow: hidden;
    }
    .hist-tag {
        display: inline-block;
        padding: 0.1rem 0.4rem;
        background: rgba(34, 211, 238, 0.12);
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 4px;
        font-size: 0.6rem;
        color: #22d3ee;
        font-weight: 600;
        margin-top: 0.3rem;
    }

    .side-section-title {
        font-size: 0.68rem; color: #7a8bb0; text-transform: uppercase;
        letter-spacing: 1.5px; font-weight: 700; margin: 1rem 0 0.6rem 0;
    }

    .side-empty {
        text-align: center;
        padding: 1.5rem 0.5rem;
        color: #64748b;
        font-size: 0.82rem;
    }
    .side-empty-icon { font-size: 1.8rem; opacity: 0.4; margin-bottom: 0.5rem; }

    .success-banner {
        background: linear-gradient(135deg, rgba(34, 211, 238, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(34, 211, 238, 0.4);
        border-radius: 10px;
        padding: 0.7rem 0.9rem;
        color: #22d3ee;
        font-weight: 600;
        font-size: 0.8rem;
        margin-bottom: 0.8rem;
    }

    .stAlert { border-radius: 12px; }

    p, span, div, label { color: #c8d4e8; }
    .stCaption, small { color: #7a8bb0 !important; }
    .stSpinner > div { border-top-color: #22d3ee !important; }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #e879f9 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.6rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.35) !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(232, 121, 249, 0.55) !important;
    }

    hr { border-color: rgba(34, 211, 238, 0.1); margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# =========================
# API KEYS
# =========================

def _get_secret(name, default=None):
    try:
        return st.secrets[name]
    except Exception:
        return default

CLOUDFLARE_ACCOUNT_ID = _get_secret("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = _get_secret("CLOUDFLARE_API_TOKEN")
REPLICATE_API_TOKEN = _get_secret("REPLICATE_API_TOKEN")
TOGETHER_API_KEY = _get_secret("TOGETHER_API_KEY")
FAL_API_KEY = _get_secret("FAL_API_KEY")

# =========================
# PROVIDERS — 5+ model chain (NO Hugging Face)
# =========================


def generate_cloudflare_flux(prompt, width, height):
    if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
        raise Exception("Cloudflare not configured")

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-2-klein-4b"
    )
    files = {
        "prompt": (None, prompt),
        "width": (None, str(width)),
        "height": (None, str(height))
    }
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"},
        files=files,
        timeout=180
    )
    if response.status_code != 200:
        raise Exception(f"Cloudflare FLUX error {response.status_code}")
    data = response.json()
    if not data.get("success"):
        raise Exception("Cloudflare FLUX failed")
    return base64.b64decode(data["result"]["image"])


def generate_cloudflare_sdxl(prompt, width, height):
    if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
        raise Exception("Cloudflare not configured")

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0"
    )
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"},
        json={"prompt": prompt, "width": width, "height": height},
        timeout=180
    )
    if response.status_code != 200:
        raise Exception(f"Cloudflare SDXL error {response.status_code}")
    return response.content


def generate_cloudflare_schnell(prompt, width, height):
    if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
        raise Exception("Cloudflare not configured")

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    )
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"},
        json={"prompt": prompt, "width": width, "height": height},
        timeout=180
    )
    if response.status_code != 200:
        raise Exception(f"Cloudflare Schnell error {response.status_code}")
    data = response.json()
    if not data.get("success"):
        raise Exception("Cloudflare Schnell failed")
    return base64.b64decode(data["result"]["image"])


def generate_replicate(prompt, width, height):
    if not REPLICATE_API_TOKEN:
        raise Exception("Replicate not configured")

    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
        "Prefer": "wait"
    }
    payload = {
        "version": "black-forest-labs/flux-schnell",
        "input": {"prompt": prompt, "width": width, "height": height}
    }
    response = requests.post(url, headers=headers, json=payload, timeout=180)
    if response.status_code not in [200, 201]:
        raise Exception(f"Replicate error {response.status_code}")

    prediction = response.json()
    if prediction.get("status") == "succeeded":
        output = prediction.get("output")
        image_url = output[0] if isinstance(output, list) else output
        return requests.get(image_url, timeout=60).content

    get_url = prediction["urls"]["get"]
    for _ in range(60):
        time.sleep(2)
        status_data = requests.get(get_url, headers=headers, timeout=30).json()
        if status_data["status"] == "succeeded":
            output = status_data.get("output")
            image_url = output[0] if isinstance(output, list) else output
            return requests.get(image_url, timeout=60).content
        if status_data["status"] == "failed":
            raise Exception("Replicate prediction failed")
    raise Exception("Replicate timeout")


def generate_together(prompt, width, height):
    if not TOGETHER_API_KEY:
        raise Exception("Together AI not configured")

    url = "https://api.together.xyz/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "black-forest-labs/FLUX.1-schnell-Free",
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": 4,
        "n": 1,
        "response_format": "b64_json"
    }
    response = requests.post(url, headers=headers, json=payload, timeout=180)
    if response.status_code != 200:
        raise Exception(f"Together error {response.status_code}")
    data = response.json()
    return base64.b64decode(data["data"][0]["b64_json"])


def generate_fal(prompt, width, height):
    if not FAL_API_KEY:
        raise Exception("fal.ai not configured")

    url = "https://fal.run/fal-ai/flux/schnell"
    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "image_size": {"width": width, "height": height},
        "num_inference_steps": 4
    }
    response = requests.post(url, headers=headers, json=payload, timeout=180)
    if response.status_code != 200:
        raise Exception(f"fal.ai error {response.status_code}")
    data = response.json()
    image_url = data["images"][0]["url"]
    return requests.get(image_url, timeout=60).content


def generate_pollinations(prompt, width, height):
    encoded_prompt = urllib.parse.quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}&nologo=true"
    )
    response = requests.get(url, timeout=120)
    if response.status_code != 200:
        raise Exception(f"Pollinations error {response.status_code}")
    return response.content


def generate_with_fallback(prompt, width, height):
    providers = []

    if CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN:
        providers.append(("Cloudflare FLUX", generate_cloudflare_flux))
        providers.append(("Cloudflare SDXL", generate_cloudflare_sdxl))
        providers.append(("Cloudflare Schnell", generate_cloudflare_schnell))

    if REPLICATE_API_TOKEN:
        providers.append(("Replicate", generate_replicate))
    if TOGETHER_API_KEY:
        providers.append(("Together AI", generate_together))
    if FAL_API_KEY:
        providers.append(("fal.ai", generate_fal))

    providers.append(("Pollinations", generate_pollinations))

    last_error = None
    for name, func in providers:
        try:
            image_bytes = func(prompt, width, height)
            if image_bytes and len(image_bytes) > 1000:
                return image_bytes, name
        except Exception as e:
            last_error = f"{name}: {e}"
            continue

    raise Exception(f"All image providers failed. Last error: {last_error}")


# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.markdown(
        f"""
        <div class="side-brand">
            <div class="side-logo"><img src="{ICON_DATA_URI}" alt="Lumina" /></div>
            <div class="side-brand-text">
                <h3>Lumina</h3>
                <p>TURN WORDS INTO LIGHT</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_create, tab_history, tab_settings = st.tabs(["🎨 Create", "📚 History", "⚙️ Settings"])

    with tab_create:
        st.markdown('<div class="side-section-title">Quality</div>', unsafe_allow_html=True)
        quality = st.selectbox(
            "Quality",
            ["Standard", "High", "Maximum"],
            index=["Standard", "High", "Maximum"].index(st.session_state.settings["quality"]),
            label_visibility="collapsed",
            key="side_quality"
        )

        st.markdown('<div class="side-section-title">Aspect Ratio</div>', unsafe_allow_html=True)
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            ["Square (1:1)", "Landscape (16:9)", "Portrait (9:16)"],
            index=["Square (1:1)", "Landscape (16:9)", "Portrait (9:16)"].index(
                st.session_state.settings["aspect_ratio"]
            ),
            label_visibility="collapsed",
            key="side_aspect"
        )

        if aspect_ratio == "Square (1:1)":
            resolution_options = {
                "512 × 512": (512, 512),
                "768 × 768": (768, 768),
                "1024 × 1024": (1024, 1024)
            }
        elif aspect_ratio == "Landscape (16:9)":
            resolution_options = {
                "1280 × 720": (1280, 720),
                "1920 × 1080": (1920, 1080)
            }
        else:
            resolution_options = {
                "720 × 1280": (720, 1280),
                "1080 × 1920": (1080, 1920)
            }

        st.markdown('<div class="side-section-title">Resolution</div>', unsafe_allow_html=True)
        resolution = st.selectbox(
            "Resolution",
            list(resolution_options.keys()),
            index=0,
            label_visibility="collapsed",
            key="side_resolution"
        )

        st.markdown('<div class="side-section-title">Image Format</div>', unsafe_allow_html=True)
        image_format = st.selectbox(
            "Image Format",
            ["PNG", "JPEG", "WEBP"],
            index=["PNG", "JPEG", "WEBP"].index(st.session_state.settings["image_format"]),
            label_visibility="collapsed",
            key="side_format"
        )

        st.markdown("---")

        active = []
        if CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN:
            active.append("Cloudflare")
        if REPLICATE_API_TOKEN:
            active.append("Replicate")
        if TOGETHER_API_KEY:
            active.append("Together")
        if FAL_API_KEY:
            active.append("fal.ai")
        active.append("Pollinations")
        st.caption(f"🔗 {' · '.join(active)}")

    with tab_history:
        history = load_history()

        if not history:
            st.markdown(
                """
                <div class="side-empty">
                    <div class="side-empty-icon">📚</div>
                    <div>No images yet</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="side-section-title">{len(history)} saved</div>',
                unsafe_allow_html=True
            )

            if st.button("🗑️  Clear All", use_container_width=True, key="side_clear_all"):
                clear_history()
                st.rerun()

            st.markdown("")

            for idx, entry in enumerate(history):
                thumb_path = entry.get("thumbnail", "")
                thumb_exists = Path(thumb_path).exists()

                if thumb_exists:
                    thumb_html = (
                        f'<img src="data:image/jpeg;base64,'
                        f'{base64.b64encode(open(thumb_path, "rb").read()).decode()}" />'
                    )
                else:
                    thumb_html = (
                        '<div style="width:54px;height:54px;background:#1f2937;'
                        'border-radius:8px;display:flex;align-items:center;'
                        'justify-content:center;color:#475569;flex-shrink:0;">🖼️</div>'
                    )

                st.markdown(
                    f"""
                    <div class="hist-card">
                        {thumb_html}
                        <div class="hist-meta">
                            <div class="hist-time">🕐 {entry['timestamp']}</div>
                            <div class="hist-prompt">{entry['prompt'][:80]}</div>
                            <span class="hist-tag">{entry['provider']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                with st.expander("View / Delete", expanded=False):
                    st.markdown(
                        f"<div style='font-size:0.82rem;color:#c8d4e8;"
                        f"line-height:1.6;'>{entry['prompt']}</div>",
                        unsafe_allow_html=True
                    )
                    st.caption(
                        f"Provider: **{entry['provider']}** · "
                        f"Size: **{entry['width']}×{entry['height']}** · "
                        f"Quality: **{entry['quality']}**"
                    )
                    if st.button("🗑️ Delete", key=f"del_{idx}_{entry['id']}", use_container_width=True):
                        delete_history_entry(entry['id'])
                        st.rerun()

    with tab_settings:
        if st.session_state.settings_saved_msg:
            st.markdown(
                '<div class="success-banner">✅ Settings saved</div>',
                unsafe_allow_html=True
            )
            st.session_state.settings_saved_msg = False

        if st.session_state.settings_reset_msg:
            st.markdown(
                '<div class="success-banner">✅ Reset to defaults</div>',
                unsafe_allow_html=True
            )
            st.session_state.settings_reset_msg = False

        v = st.session_state.settings_version

        st.markdown('<div class="side-section-title">Default Quality</div>', unsafe_allow_html=True)
        new_quality = st.radio(
            "Default Quality",
            options=["Standard", "High", "Maximum"],
            index=["Standard", "High", "Maximum"].index(st.session_state.settings["quality"]),
            horizontal=True,
            label_visibility="collapsed",
            key=f"settings_quality_v{v}"
        )

        st.markdown('<div class="side-section-title">Default Aspect Ratio</div>', unsafe_allow_html=True)
        new_aspect = st.radio(
            "Default Aspect",
            options=["Square (1:1)", "Landscape (16:9)", "Portrait (9:16)"],
            index=["Square (1:1)", "Landscape (16:9)", "Portrait (9:16)"].index(
                st.session_state.settings["aspect_ratio"]
            ),
            horizontal=False,
            label_visibility="collapsed",
            key=f"settings_aspect_v{v}"
        )

        st.markdown('<div class="side-section-title">Default Format</div>', unsafe_allow_html=True)
        new_format = st.radio(
            "Default Format",
            options=["PNG", "JPEG", "WEBP"],
            index=["PNG", "JPEG", "WEBP"].index(st.session_state.settings["image_format"]),
            horizontal=True,
            label_visibility="collapsed",
            key=f"settings_format_v{v}"
        )

        st.markdown("")

        if st.button("💾  Save Settings", use_container_width=True, key=f"save_settings_v{v}"):
            st.session_state.settings["quality"] = new_quality
            st.session_state.settings["aspect_ratio"] = new_aspect
            st.session_state.settings["image_format"] = new_format
            save_settings_file(st.session_state.settings)
            st.session_state.settings_saved_msg = True
            st.rerun()

        if st.button("↺  Reset to Defaults", use_container_width=True, key=f"reset_settings_v{v}"):
            st.session_state.settings = DEFAULT_SETTINGS.copy()
            save_settings_file(DEFAULT_SETTINGS)
            st.session_state.settings_version += 1
            for k in list(st.session_state.keys()):
                if k.startswith("side_") or k.startswith("settings_"):
                    try:
                        del st.session_state[k]
                    except Exception:
                        pass
            st.session_state.settings_reset_msg = True
            st.rerun()

        st.markdown("---")
        st.markdown('<div class="side-section-title">Currently Saved</div>', unsafe_allow_html=True)

        current = st.session_state.settings
        st.markdown(
            f"""
            <div style="font-size:0.82rem;line-height:1.9;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#94a3c8;">Quality</span>
                    <strong style="color:#22d3ee;">{current['quality']}</strong>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#94a3c8;">Aspect</span>
                    <strong style="color:#22d3ee;">{current['aspect_ratio']}</strong>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#94a3c8;">Format</span>
                    <strong style="color:#22d3ee;">{current['image_format']}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# HERO + DESCRIPTION
# =========================

st.markdown(
    f"""
    <div class="hero">
        <img src="{LOGO_DATA_URI}" alt="Lumina logo" />
    </div>
    <div class="desc-block">
        <div class="desc-tagline">Turn words into light.</div>
        <div class="desc-text">
            Lumina transforms your text prompts into stunning AI-generated visuals.
            Powered by a resilient multi-model chain — if one provider is down,
            another instantly takes over.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# PROMPT INPUT
# =========================

st.markdown("### 📝 Describe your image")

prompt = st.text_area(
    "Prompt",
    placeholder="Example: A bioluminescent forest at midnight, glowing mushrooms, cinematic lighting, ultra-detailed photography",
    height=140,
    label_visibility="collapsed"
)

st.write("")

# =========================
# GENERATE
# =========================

if st.button("💫  Generate Image", use_container_width=True, key="generate_btn"):

    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt first.")
        st.stop()

    quality_text = {
        "Standard": "good image quality",
        "High": "highly detailed and sharp image quality",
        "Maximum": "maximum realistic detail, sharp textures, cinematic professional quality"
    }

    final_prompt = (
        f"{prompt.strip()}\n\n"
        f"Create the image with {quality_text[quality]}. "
        f"Use realistic lighting, natural textures, "
        f"professional composition and detailed visual quality."
    )

    width, height = resolution_options[resolution]

    scan_placeholder = st.empty()
    scan_placeholder.markdown(
        """
        <div class="scanning">
            <div class="scanning-icon">💫</div>
            <div class="scanning-label">Generating image</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        image_bytes, provider_used = generate_with_fallback(final_prompt, width, height)
        image = Image.open(BytesIO(image_bytes))

        scan_placeholder.empty()

        st.markdown(
            f"""
            <div class="result-header">
                <div class="result-header-title">
                    <span class="result-header-dot"></span> Image generated
                </div>
                <div class="result-header-meta">{width} × {height} · {quality}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.image(image, use_container_width=True)

        st.markdown(
            f"""
            <div class="chips-row">
                <div class="chip">📐 <strong>{width} × {height}</strong></div>
                <div class="chip">🎨 <strong>{quality}</strong></div>
                <div class="chip">🖼️ <strong>{image_format}</strong></div>
                <div class="chip">⚡ <strong>{provider_used}</strong></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(f"⚡ Generated via {provider_used}")

        output = BytesIO()

        if image_format == "PNG":
            if image.mode not in ["RGB", "RGBA"]:
                image = image.convert("RGB")
            image.save(output, format="PNG")
            mime_type = "image/png"
            filename = "lumina_image.png"

        elif image_format == "JPEG":
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(output, format="JPEG", quality=95)
            mime_type = "image/jpeg"
            filename = "lumina_image.jpg"

        else:
            if image.mode not in ["RGB", "RGBA"]:
                image = image.convert("RGB")
            image.save(output, format="WEBP", quality=95)
            mime_type = "image/webp"
            filename = "lumina_image.webp"

        st.download_button(
            label=f"⬇️  Download {image_format}",
            data=output.getvalue(),
            file_name=filename,
            mime=mime_type,
            use_container_width=True,
            key="download_btn"
        )

        add_history_entry(image, prompt.strip(), provider_used, quality, width, height)

    except requests.exceptions.Timeout:
        scan_placeholder.empty()
        st.error("⏱️ All providers timed out. Please try again.")

    except Exception as e:
        scan_placeholder.empty()
        st.error("❌ All image providers failed.")
        st.code(str(e))

else:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-state-icon">💫</div>
            <div class="empty-state-title">Enter a prompt above and click Generate</div>
        </div>
        """,
        unsafe_allow_html=True
    )
