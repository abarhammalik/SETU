"""
app.py
======
PROJECT SETU (सेतु) // Subterranean Mine Rescue & Multi-Spectral Reconnaissance Rover
Ground Control Station (GCS) Telemetry Console & Analytics Platform

SIH 2026 Problem Statement ID: SIH26039
Compliance Target: DGMS / PESO Ex d I Mb Flameproof Standard
National Initiatives: Atmanirbhar Bharat · Make in India

Official Links:
- Web Platform: https://setu-mine-rescue-rover.vercel.app/
- GitHub Repository: https://github.com/abarhammalik/SETU-Dashboard
- 6 Field Demos: https://setu-mine-rescue-rover.vercel.app/#demonstrations
- Hardware Schematic: https://setu-mine-rescue-rover.vercel.app/#hardware-labeling
- OCU Terminal Simulator: https://setu-mine-rescue-rover.vercel.app/#ocu-sim
- DGMS Roadmap: https://setu-mine-rescue-rover.vercel.app/#credibility
"""

from datetime import datetime
import math
import textwrap
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from mine_analytics import (
    CoExposureState,
    HazardLevel,
    MineAtmosphericAnalyzer,
    OxygenState,
)

# --------------------------------------------------------------------------- #
# Page Configuration
# --------------------------------------------------------------------------- #

st.set_page_config(
    page_title="PROJECT SETU // Mine Rescue Rover GCS",
    page_icon="⌖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------- #
# Theme State Initialization (Default to Light Mode)
# --------------------------------------------------------------------------- #

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

is_light = st.session_state.theme_mode == "light"

# --------------------------------------------------------------------------- #
# Theme Design Tokens
# --------------------------------------------------------------------------- #

if is_light:
    # High-Visibility Enterprise Industrial Light Console
    APP_BG = "#F8FAFC"
    APP_TEXT = "#0F172A"
    APP_TEXT_MUTED = "#475569"
    PANEL_BG = "#FFFFFF"
    PANEL_BORDER = "#CBD5E1"
    PANEL_SHADOW = "0 4px 18px rgba(0, 0, 0, 0.06)"
    HEADER_BG = "linear-gradient(135deg, #1E293B 0%, #0F172A 100%)"
    SIDEBAR_BG = "#F1F5F9"
    SIDEBAR_BORDER = "#CBD5E1"
    SIDEBAR_HEADER = "#0F172A"
    METRIC_BG = "#FFFFFF"
    METRIC_VAL = "#0F172A"
    METRIC_LABEL = "#475569"
    FEED_BG = "#F1F5F9"
    FEED_BORDER = "#CBD5E1"
    BTN_BG = "#FFFFFF"
    BTN_TEXT = "#0F172A"
    BTN_BORDER = "#CBD5E1"
    BTN_HOVER_BG = "#F8FAFC"
    BTN_HOVER_BORDER = "#0284C7"
    CHART_GRID = "#E2E8F0"
    CHART_LABEL = "#475569"
    CHART_TITLE = "#0F172A"
    ACCENT_PRIMARY = "#0284C7"
    ACCENT_SECONDARY = "#D97706"
    BADGE_BG_INFO = "rgba(2, 132, 199, 0.12)"
    BADGE_TEXT_INFO = "#0284C7"
    TOOLBAR_BG = "#FFFFFF"
    TOOLBAR_BORDER = "#CBD5E1"
else:
    # Subterranean 0-Lux Tactical Dark Cockpit — High Contrast Mil-Spec
    APP_BG = "radial-gradient(circle at top left, #101925 0%, #060B12 100%)"
    APP_TEXT = "#FFFFFF"
    APP_TEXT_MUTED = "#CBD5E1"
    PANEL_BG = "#121C2B"
    PANEL_BORDER = "#243549"
    PANEL_SHADOW = "0 6px 25px rgba(0, 0, 0, 0.45)"
    HEADER_BG = "linear-gradient(135deg, #131E2D 0%, #0A121B 100%)"
    SIDEBAR_BG = "#0B121A"
    SIDEBAR_BORDER = "#1E2C3D"
    SIDEBAR_HEADER = "#00F0FF"
    METRIC_BG = "#131E2C"
    METRIC_VAL = "#FFFFFF"
    METRIC_LABEL = "#CBD5E1"
    FEED_BG = "#070B10"
    FEED_BORDER = "rgba(255, 255, 255, 0.2)"
    BTN_BG = "#182434"
    BTN_TEXT = "#FFFFFF"
    BTN_BORDER = "#2E4259"
    BTN_HOVER_BG = "#1F3247"
    BTN_HOVER_BORDER = "#00F0FF"
    CHART_GRID = "#233346"
    CHART_LABEL = "#94A3B8"
    CHART_TITLE = "#F1F5F9"
    ACCENT_PRIMARY = "#00F0FF"
    ACCENT_SECONDARY = "#F59E0B"
    BADGE_BG_INFO = "rgba(56, 189, 248, 0.18)"
    BADGE_TEXT_INFO = "#38BDF8"
    TOOLBAR_BG = "#131C28"
    TOOLBAR_BORDER = "#233346"

ACCENT_AMBER = "#F59E0B"
DANGER_RED = "#EF4444"
SAFE_GREEN = "#10B981"
INFO_BLUE = "#38BDF8"

# --------------------------------------------------------------------------- #
# Sidebar Tactical Header & Mode Switcher
# --------------------------------------------------------------------------- #

st.sidebar.markdown(
    textwrap.dedent(f"""
    <div class="sidebar-header-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: {SAFE_GREEN}; display: flex; align-items: center; gap: 4px;">
                <span class="pulse-dot" style="width: 8px; height: 8px; margin-right: 2px;"></span> RF LINK SYNC
            </span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 700; color: {'#0284C7' if is_light else '#00F0FF'}; background: {'rgba(2, 132, 199, 0.1)' if is_light else 'rgba(0, 240, 255, 0.12)'}; padding: 0.15rem 0.45rem; border-radius: 4px; border: 1px solid {'rgba(2, 132, 199, 0.25)' if is_light else 'rgba(0, 240, 255, 0.25)'};">
                Ex d I Mb
            </span>
        </div>
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; font-weight: 800; color: {APP_TEXT}; letter-spacing: -0.01em;">
            SETU ROVER CONSOLE
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: {'#CBD5E1' if not is_light else '#475569'}; margin-top: 3px; white-space: nowrap;">
            Node: <b style="color: {'#00F0FF' if not is_light else '#0284C7'};">ALPHA-01</b> · 865MHz LoRa
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

_theme_label = "◐ Switch to 0-Lux Dark HUD" if is_light else "☼ Switch to High-Vis Light HUD"
if st.sidebar.button(_theme_label, key="theme_toggle_btn", use_container_width=True):
    st.session_state.theme_mode = "dark" if is_light else "light"
    st.rerun()

# --------------------------------------------------------------------------- #
# Custom CSS
# --------------------------------------------------------------------------- #

# Font Awesome 6 Professional Icon System
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">', unsafe_allow_html=True)

st.markdown(
    textwrap.dedent(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: {APP_BG};
        color: {APP_TEXT};
        -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; text-rendering: optimizeLegibility;
    }}

    /* Top Branding Navigation Bar */
    .setu-top-header {{
        background: {HEADER_BG};
        border: 1px solid {PANEL_BORDER};
        border-radius: 12px;
        padding: 1.25rem 1.6rem;
        margin-bottom: 0.8rem;
        box-shadow: {PANEL_SHADOW};
    }}
    .setu-brand-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        flex-wrap: wrap;
    }}
    .setu-badge-hindi {{
        background: linear-gradient(135deg, #FF9933, #138808);
        color: #FFFFFF;
        font-size: 0.92rem;
        font-weight: 700;
        padding: 0.22rem 0.65rem;
        border-radius: 6px;
        letter-spacing: 0.05em;
    }}
    .setu-subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #CBD5E1;
        margin-top: 0.4rem;
        line-height: 1.45;
    }}

    /* Sidebar Tactical Styling & Controls */
    [data-testid="stSidebar"] {{
        background: {SIDEBAR_BG} !important;
        border-right: 2px solid {SIDEBAR_BORDER} !important;
        box-shadow: {'2px 0 12px rgba(0, 0, 0, 0.03)' if is_light else '4px 0 20px rgba(0, 0, 0, 0.4)'} !important;
    }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: {SIDEBAR_HEADER} !important;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 0.02em;
    }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{
        color: {APP_TEXT} !important;
    }}
    /* Sidebar Slider Readouts */
    [data-testid="stSidebar"] [data-testid="stSlider"] label p {{
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.84rem !important;
        color: {'#0F172A' if is_light else '#E2E8F0'} !important;
    }}
    [data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] {{
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 800 !important;
        font-size: 0.8rem !important;
        color: {'#0284C7' if is_light else '#00F0FF'} !important;
        background: {'#FFFFFF' if is_light else '#0D1622'} !important;
        border: 1px solid {'#CBD5E1' if is_light else '#243447'} !important;
        border-radius: 4px !important;
        padding: 1px 5px !important;
    }}
    /* Sidebar Checkbox Labels */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label span p {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
        color: {'#1E293B' if is_light else '#F1F5F9'} !important;
    }}
    /* Sidebar Section Cards */
    .sidebar-header-card {{
        background: {'linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%)' if is_light else 'linear-gradient(135deg, #131C28 0%, #0A1018 100%)'};
        border: 1.5px solid {'#CBD5E1' if is_light else '#2A3B4F'};
        border-left: 4px solid {'#0284C7' if is_light else '#00F0FF'};
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.85rem;
        box-shadow: {'0 2px 8px rgba(0,0,0,0.05)' if is_light else '0 4px 16px rgba(0,0,0,0.3)'};
    }}
    .sidebar-section-card {{
        background: {'#FFFFFF' if is_light else 'rgba(19, 28, 40, 0.75)'};
        border: 1px solid {'#CBD5E1' if is_light else '#233346'};
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.85rem;
        box-shadow: {'0 2px 6px rgba(0,0,0,0.04)' if is_light else '0 4px 14px rgba(0,0,0,0.25)'};
    }}
    .sidebar-mod-badge {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 0.6rem;
        padding-bottom: 0.35rem;
        border-bottom: 1px solid {'#E2E8F0' if is_light else 'rgba(255,255,255,0.08)'};
    }}
    .sidebar-compliance-card {{
        background: {'#F8FAFC' if is_light else 'rgba(10, 16, 24, 0.8)'};
        border: 1px dashed {'#CBD5E1' if is_light else '#233346'};
        border-radius: 8px;
        padding: 0.75rem 0.9rem;
        margin-top: 1rem;
        font-size: 0.78rem;
        color: {'#475569' if is_light else '#94A3B8'};
    }}

    /* ================================================================== */
    /* Multi-Domain Tactical Navigation Deck — Industrial GCS Console    */
    /* Streamlit 1.65+ uses div[data-testid="stTab"] role="tab"          */
    /* ================================================================== */

    /* Tab List Container */
    [data-baseweb="tab-list"],
    div[role="tablist"] {{
        background: {'#060B12' if not is_light else '#EFF3F8'} !important;
        border: 2px solid {'#1A2536' if not is_light else '#C8D2DE'} !important;
        border-radius: 14px !important;
        padding: 8px 10px !important;
        gap: 8px !important;
        display: flex !important;
        align-items: stretch !important;
        margin-top: 0.6rem !important;
        margin-bottom: 1.6rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, {'0.5' if not is_light else '0.08'}),
                    inset 0 1px 0 rgba(255, 255, 255, {'0.04' if not is_light else '0.8'}) !important;
    }}

    /* Hide default Streamlit tab decoration */
    [data-baseweb="tab-highlight"],
    [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* Base Tab Button (both old + new Streamlit selectors) */
    button[data-baseweb="tab"],
    div[data-testid="stTab"] {{
        flex: 1 1 0% !important;
        min-width: 0 !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-family: 'Space Grotesk', 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        border: 1px solid {'#1E293B' if not is_light else '#D4DCE6'} !important;
        background: {'rgba(14, 22, 33, 0.85)' if not is_light else '#FFFFFF'} !important;
        color: {APP_TEXT_MUTED} !important;
        cursor: pointer !important;
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
        white-space: nowrap !important;
        letter-spacing: 0.03em !important;
        position: relative !important;
        overflow: hidden !important;
    }}

    /* Tab inner text */
    button[data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stTab"] div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stTab"] p {{
        font-family: 'Space Grotesk', 'Inter', sans-serif !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: 0.03em !important;
        color: inherit !important;
    }}

    /* ── Tab 1: Electric Cyan · MISSION FLIGHT DECK ──────────────────── */
    button[data-baseweb="tab"]:nth-of-type(1),
    div[data-testid="stTab"]:nth-of-type(1) {{
        border-left: 4px solid #00F0FF !important;
        color: {'#5CCFE6' if not is_light else '#0284C7'} !important;
    }}
    button[data-baseweb="tab"]:nth-of-type(1):hover,
    div[data-testid="stTab"]:nth-of-type(1):hover {{
        background: {'rgba(0, 240, 255, 0.12)' if not is_light else 'rgba(2, 132, 199, 0.08)'} !important;
        border-color: #00F0FF !important;
        color: {'#00F0FF' if not is_light else '#0369A1'} !important;
        box-shadow: 0 6px 24px rgba(0, 240, 255, {'0.35' if not is_light else '0.2'}) !important;
        transform: translateY(-2px) !important;
    }}
    button[data-baseweb="tab"]:nth-of-type(1)[aria-selected="true"],
    div[data-testid="stTab"]:nth-of-type(1)[data-selected="true"],
    div[data-testid="stTab"]:nth-of-type(1)[aria-selected="true"] {{
        background: {'linear-gradient(180deg, rgba(0, 240, 255, 0.22) 0%, rgba(0, 180, 220, 0.08) 100%)' if not is_light else 'linear-gradient(180deg, rgba(2, 132, 199, 0.14) 0%, rgba(2, 132, 199, 0.04) 100%)'} !important;
        border: 2px solid #00F0FF !important;
        border-left: 5px solid #00F0FF !important;
        color: {'#FFFFFF' if not is_light else '#0369A1'} !important;
        box-shadow: 0 0 28px rgba(0, 240, 255, {'0.45' if not is_light else '0.22'}),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    }}

    /* ── Tab 2: Combustible Amber · 5-GAS ATMOSPHERICS ───────────────── */
    button[data-baseweb="tab"]:nth-of-type(2),
    div[data-testid="stTab"]:nth-of-type(2) {{
        border-left: 4px solid #F59E0B !important;
        color: {'#FBBF24' if not is_light else '#D97706'} !important;
    }}
    button[data-baseweb="tab"]:nth-of-type(2):hover,
    div[data-testid="stTab"]:nth-of-type(2):hover {{
        background: {'rgba(245, 158, 11, 0.12)' if not is_light else 'rgba(245, 158, 11, 0.08)'} !important;
        border-color: #F59E0B !important;
        color: {'#FCD34D' if not is_light else '#B45309'} !important;
        box-shadow: 0 6px 24px rgba(245, 158, 11, {'0.35' if not is_light else '0.2'}) !important;
        transform: translateY(-2px) !important;
    }}
    button[data-baseweb="tab"]:nth-of-type(2)[aria-selected="true"],
    div[data-testid="stTab"]:nth-of-type(2)[data-selected="true"],
    div[data-testid="stTab"]:nth-of-type(2)[aria-selected="true"] {{
        background: {'linear-gradient(180deg, rgba(245, 158, 11, 0.22) 0%, rgba(217, 119, 6, 0.08) 100%)' if not is_light else 'linear-gradient(180deg, rgba(245, 158, 11, 0.14) 0%, rgba(245, 158, 11, 0.04) 100%)'} !important;
        border: 2px solid #F59E0B !important;
        border-left: 5px solid #F59E0B !important;
        color: {'#FFFFFF' if not is_light else '#B45309'} !important;
        box-shadow: 0 0 28px rgba(245, 158, 11, {'0.45' if not is_light else '0.22'}),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    }}

    /* ── Tab 3: Pulse Crimson · FMCW BIO-RADAR ───────────────────────── */
    button[data-baseweb="tab"]:nth-of-type(3),
    div[data-testid="stTab"]:nth-of-type(3) {{
        border-left: 4px solid #F43F5E !important;
        color: {'#FB7185' if not is_light else '#E11D48'} !important;
    }}
    button[data-baseweb="tab"]:nth-of-type(3):hover,
    div[data-testid="stTab"]:nth-of-type(3):hover {{
        background: {'rgba(244, 63, 94, 0.12)' if not is_light else 'rgba(244, 63, 94, 0.08)'} !important;
        border-color: #F43F5E !important;
        color: {'#FDA4AF' if not is_light else '#BE123C'} !important;
        box-shadow: 0 6px 24px rgba(244, 63, 94, {'0.35' if not is_light else '0.2'}) !important;
        transform: translateY(-2px) !important;
    }}
    button[data-baseweb="tab"]:nth-of-type(3)[aria-selected="true"],
    div[data-testid="stTab"]:nth-of-type(3)[data-selected="true"],
    div[data-testid="stTab"]:nth-of-type(3)[aria-selected="true"] {{
        background: {'linear-gradient(180deg, rgba(244, 63, 94, 0.22) 0%, rgba(225, 29, 72, 0.08) 100%)' if not is_light else 'linear-gradient(180deg, rgba(244, 63, 94, 0.14) 0%, rgba(244, 63, 94, 0.04) 100%)'} !important;
        border: 2px solid #F43F5E !important;
        border-left: 5px solid #F43F5E !important;
        color: {'#FFFFFF' if not is_light else '#BE123C'} !important;
        box-shadow: 0 0 28px rgba(244, 63, 94, {'0.45' if not is_light else '0.22'}),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    }}

    /* ── Tab 4: Neural Violet · EDGE AI & 3D SLAM ────────────────────── */
    button[data-baseweb="tab"]:nth-of-type(4),
    div[data-testid="stTab"]:nth-of-type(4) {{
        border-left: 4px solid #A855F7 !important;
        color: {'#C084FC' if not is_light else '#7C3AED'} !important;
    }}
    button[data-baseweb="tab"]:nth-of-type(4):hover,
    div[data-testid="stTab"]:nth-of-type(4):hover {{
        background: {'rgba(168, 85, 247, 0.12)' if not is_light else 'rgba(168, 85, 247, 0.08)'} !important;
        border-color: #A855F7 !important;
        color: {'#D8B4FE' if not is_light else '#6D28D9'} !important;
        box-shadow: 0 6px 24px rgba(168, 85, 247, {'0.35' if not is_light else '0.2'}) !important;
        transform: translateY(-2px) !important;
    }}
    button[data-baseweb="tab"]:nth-of-type(4)[aria-selected="true"],
    div[data-testid="stTab"]:nth-of-type(4)[data-selected="true"],
    div[data-testid="stTab"]:nth-of-type(4)[aria-selected="true"] {{
        background: {'linear-gradient(180deg, rgba(168, 85, 247, 0.22) 0%, rgba(124, 58, 237, 0.08) 100%)' if not is_light else 'linear-gradient(180deg, rgba(168, 85, 247, 0.14) 0%, rgba(168, 85, 247, 0.04) 100%)'} !important;
        border: 2px solid #A855F7 !important;
        border-left: 5px solid #A855F7 !important;
        color: {'#FFFFFF' if not is_light else '#6D28D9'} !important;
        box-shadow: 0 0 28px rgba(168, 85, 247, {'0.45' if not is_light else '0.22'}),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    }}

    /* ── Tab 5: Cyber Emerald · SETU ECOSYSTEM ───────────────────────── */
    button[data-baseweb="tab"]:nth-of-type(5),
    div[data-testid="stTab"]:nth-of-type(5) {{
        border-left: 4px solid #10B981 !important;
        color: {'#34D399' if not is_light else '#059669'} !important;
    }}
    button[data-baseweb="tab"]:nth-of-type(5):hover,
    div[data-testid="stTab"]:nth-of-type(5):hover {{
        background: {'rgba(16, 185, 129, 0.12)' if not is_light else 'rgba(16, 185, 129, 0.08)'} !important;
        border-color: #10B981 !important;
        color: {'#6EE7B7' if not is_light else '#047857'} !important;
        box-shadow: 0 6px 24px rgba(16, 185, 129, {'0.35' if not is_light else '0.2'}) !important;
        transform: translateY(-2px) !important;
    }}
    button[data-baseweb="tab"]:nth-of-type(5)[aria-selected="true"],
    div[data-testid="stTab"]:nth-of-type(5)[data-selected="true"],
    div[data-testid="stTab"]:nth-of-type(5)[aria-selected="true"] {{
        background: {'linear-gradient(180deg, rgba(16, 185, 129, 0.22) 0%, rgba(5, 150, 105, 0.08) 100%)' if not is_light else 'linear-gradient(180deg, rgba(16, 185, 129, 0.14) 0%, rgba(16, 185, 129, 0.04) 100%)'} !important;
        border: 2px solid #10B981 !important;
        border-left: 5px solid #10B981 !important;
        color: {'#FFFFFF' if not is_light else '#047857'} !important;
        box-shadow: 0 0 28px rgba(16, 185, 129, {'0.45' if not is_light else '0.22'}),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    }}

    /* ── High-Impact Quick-Action Link Buttons — Domain-Colored ────── */
    div[data-testid="stHorizontalBlock"] .stLinkButton > a {{
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.84rem !important;
        border-radius: 10px !important;
        padding: 0.7rem 0.8rem !important;
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid {'#2A3A4E' if not is_light else '#CBD5E1'} !important;
        border-bottom: 3px solid {'#2A3A4E' if not is_light else '#CBD5E1'} !important;
        background: {'linear-gradient(180deg, rgba(19, 28, 40, 0.9) 0%, rgba(14, 22, 33, 0.95) 100%)' if not is_light else 'linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%)'} !important;
        box-shadow: 0 3px 12px rgba(0, 0, 0, {'0.3' if not is_light else '0.06'}) !important;
        text-align: center !important;
        color: {ACCENT_PRIMARY} !important;
        letter-spacing: 0.02em !important;
    }}
    div[data-testid="stHorizontalBlock"] .stLinkButton > a:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 24px rgba(0, 240, 255, {'0.35' if not is_light else '0.18'}) !important;
        border-color: {ACCENT_PRIMARY} !important;
        border-bottom-color: {ACCENT_PRIMARY} !important;
        color: {'#FFFFFF' if not is_light else '#0369A1'} !important;
        background: {'linear-gradient(180deg, rgba(0, 240, 255, 0.15) 0%, rgba(0, 180, 220, 0.06) 100%)' if not is_light else 'linear-gradient(180deg, rgba(2, 132, 199, 0.08) 0%, rgba(2, 132, 199, 0.02) 100%)'} !important;
    }}

    /* Industrial KPI Metric Containers */
    div[data-testid="stMetric"] {{
        background: {'rgba(19, 28, 40, 0.75)' if not is_light else '#FFFFFF'} !important;
        border: 1px solid {PANEL_BORDER} !important;
        border-radius: 10px !important;
        padding: 0.85rem 1rem !important;
        box-shadow: {PANEL_SHADOW} !important;
        transition: all 0.2s ease !important;
    }}
    div[data-testid="stMetric"]:hover {{
        border-color: {ACCENT_PRIMARY} !important;
        box-shadow: 0 4px 16px {'rgba(2, 132, 199, 0.18)' if is_light else 'rgba(0, 240, 255, 0.25)'} !important;
        transform: translateY(-2px);
    }}
    div[data-testid="stMetricLabel"] {{
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        color: {METRIC_LABEL} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}
    div[data-testid="stMetricValue"] {{
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 800 !important;
        font-size: 1.55rem !important;
        color: {METRIC_VAL} !important;
    }}

    /* ── Scenario Command Toolbar — Mil-Spec Mission Control ──────────── */
    .scenario-toolbar {{
        background: {'linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)' if is_light else 'linear-gradient(135deg, rgba(19, 28, 40, 0.95) 0%, rgba(10, 16, 24, 0.98) 100%)'};
        border: 1px solid {'#CBD5E1' if is_light else '#233346'};
        border-left: 4px solid {ACCENT_PRIMARY};
        border-radius: 12px;
        padding: 1.1rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: {PANEL_SHADOW}, 0 4px 20px rgba(0, 0, 0, {'0.06' if is_light else '0.3'});
        position: relative;
        overflow: hidden;
    }}
    .scenario-toolbar::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, {ACCENT_PRIMARY}, transparent);
        opacity: 0.6;
    }}
    .scenario-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: {APP_TEXT};
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.5rem;
        letter-spacing: 0.02em;
    }}
    .briefing-box {{
        background: {'rgba(2, 132, 199, 0.06)' if is_light else 'rgba(0, 240, 255, 0.06)'};
        border-left: 4px solid {ACCENT_PRIMARY};
        border-radius: 6px;
        padding: 0.8rem 1.1rem;
        margin-top: 0.7rem;
        font-size: 0.9rem;
        backdrop-filter: blur(4px);
    }}

    /* Hazard & Notification Banners */
    .hazard-banner {{
        padding: 1.1rem 1.4rem;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        color: #FFFFFF;
        margin: 0.6rem 0 1.2rem 0;
        box-shadow: {PANEL_SHADOW};
        border-left: 6px solid #FFFFFF;
    }}
    .hazard-advisory {{
        font-family: 'Inter', sans-serif;
        font-size: 0.92rem;
        font-weight: 400;
        color: rgba(255,255,255,0.92);
        margin-top: 0.4rem;
    }}

    /* Panel & Metric Cards */
    [data-testid="stMetric"] {{
        background-color: {METRIC_BG} !important;
        border: 1px solid {PANEL_BORDER} !important;
        border-radius: 8px !important;
        padding: 0.9rem 1.1rem !important;
        box-shadow: {PANEL_SHADOW} !important;
    }}
    [data-testid="stMetricValue"] {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.85rem !important;
        font-weight: 700 !important;
        color: {METRIC_VAL} !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {METRIC_LABEL} !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
    }}

    .panel-card {{
        background-color: {PANEL_BG};
        border: 1px solid {PANEL_BORDER};
        border-radius: 8px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
        box-shadow: {PANEL_SHADOW};
    }}
    .panel-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.92rem;
        padding: 0.55rem 0;
        border-bottom: 1px solid {PANEL_BORDER};
    }}
    .panel-row:last-child {{ border-bottom: none; }}
    .panel-row .label {{ color: {APP_TEXT_MUTED}; font-weight: 500; }}
    .panel-row .val {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        color: {APP_TEXT};
    }}

    /* Tactical Status Badges */
    .badge {{
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.2rem 0.55rem;
        border-radius: 4px;
        letter-spacing: 0.03em;
    }}
    .badge-safe {{ background-color: rgba(16, 185, 129, 0.16); color: {SAFE_GREEN}; border: 1px solid rgba(16, 185, 129, 0.35); }}
    .badge-warn {{ background-color: rgba(245, 158, 11, 0.16); color: {ACCENT_AMBER}; border: 1px solid rgba(245, 158, 11, 0.35); }}
    .badge-danger {{ background-color: rgba(239, 68, 68, 0.16); color: {DANGER_RED}; border: 1px solid rgba(239, 68, 68, 0.35); }}
    .badge-info {{ background-color: {BADGE_BG_INFO}; color: {BADGE_TEXT_INFO}; border: 1px solid rgba(2, 132, 199, 0.35); }}

    /* ── Hazard Tape Divider — Industrial Safety Striping ──────────────── */
    .hazard-stripe {{
        height: 5px;
        width: 100%;
        margin: 0.5rem 0 0.9rem 0;
        border-radius: 3px;
        background: repeating-linear-gradient(
            135deg,
            {ACCENT_AMBER} 0px, {ACCENT_AMBER} 12px,
            {'#1E293B' if not is_light else '#E2E8F0'} 12px, {'#1E293B' if not is_light else '#E2E8F0'} 24px
        );
        box-shadow: 0 2px 8px rgba(245, 158, 11, {'0.25' if not is_light else '0.15'});
        opacity: 0.85;
    }}

    /* ── Streamlit Button & Link Button — Tactical GCS Style ──────────── */
    div.stButton > button {{
        background: {'linear-gradient(180deg, #182434 0%, #101925 100%)' if not is_light else '#FFFFFF'} !important;
        color: {'#FFFFFF' if not is_light else '#0F172A'} !important;
        border: 1.5px solid {'#2E4259' if not is_light else '#CBD5E1'} !important;
        border-radius: 9px !important;
        font-family: 'Space Grotesk', 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: center !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, {'0.35' if not is_light else '0.05'}) !important;
        padding: 0.5rem 0.25rem !important;
        position: relative !important;
        overflow: hidden !important;
        white-space: nowrap !important;
    }}
    div.stButton > button p {{
        font-family: 'Space Grotesk', 'Inter', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        color: inherit !important;
        margin: 0 !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }}
    div.stButton > button:hover {{
        border-color: {'#00F0FF' if not is_light else '#0284C7'} !important;
        color: {'#00F0FF' if not is_light else '#0284C7'} !important;
        background: {'rgba(0, 240, 255, 0.12)' if not is_light else '#F1F5F9'} !important;
        box-shadow: 0 4px 14px rgba({'0, 240, 255' if not is_light else '2, 132, 199'}, 0.25) !important;
        transform: translateY(-2px) !important;
    }}
    div.stButton > button:active {{
        transform: translateY(0) !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3) !important;
    }}

    div[data-testid="stLinkButton"] > a {{
        background: {'linear-gradient(180deg, rgba(19, 28, 40, 0.9) 0%, rgba(14, 22, 33, 0.95) 100%)' if not is_light else 'linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%)'} !important;
        color: {ACCENT_PRIMARY} !important;
        border: 1px solid {'#2A3A4E' if not is_light else '#CBD5E1'} !important;
        border-radius: 10px !important;
        font-family: 'Space Grotesk', 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.84rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: center !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, {'0.25' if not is_light else '0.06'}) !important;
        padding: 0.65rem 0.8rem !important;
        text-decoration: none !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    div[data-testid="stLinkButton"] > a:hover {{
        border-color: {ACCENT_PRIMARY} !important;
        color: #FFFFFF !important;
        background: {'linear-gradient(135deg, rgba(0, 240, 255, 0.18) 0%, rgba(0, 180, 220, 0.08) 100%)' if not is_light else 'linear-gradient(135deg, rgba(2, 132, 199, 0.12) 0%, rgba(2, 132, 199, 0.04) 100%)'} !important;
        box-shadow: 0 6px 20px rgba({'0, 240, 255' if not is_light else '2, 132, 199'}, 0.3) !important;
        transform: translateY(-2px) !important;
    }}

    /* ── Quick-Action Command Card Grid ──────────────────────────────── */
    .quick-action-grid {{
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 10px;
        margin-bottom: 0.4rem;
    }}
    .qa-card {{
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 0.7rem 0.9rem;
        border-radius: 10px;
        text-decoration: none !important;
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.82rem;
        letter-spacing: 0.02em;
        border: 1px solid {'#2A3A4E' if not is_light else '#D4DCE6'};
        background: {'linear-gradient(180deg, rgba(19, 28, 40, 0.92) 0%, rgba(12, 18, 28, 0.96) 100%)' if not is_light else 'linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%)'};
        box-shadow: 0 3px 12px rgba(0, 0, 0, {'0.3' if not is_light else '0.06'});
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    .qa-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        opacity: 0;
        transition: opacity 0.28s ease;
    }}
    .qa-card:hover::before {{
        opacity: 1;
    }}
    .qa-card:hover {{
        transform: translateY(-3px);
        border-bottom-width: 2px;
    }}
    .qa-icon {{
        font-size: 1.1rem;
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 7px;
        flex-shrink: 0;
    }}
    .qa-label {{
        flex: 1;
        white-space: nowrap;
    }}
    .qa-arrow {{
        opacity: 0.4;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }}
    .qa-card:hover .qa-arrow {{
        opacity: 1;
        transform: translateX(3px);
    }}

    /* Primary Button Active Luminous State (Used by Active Stage Button) */
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="stBaseButton-primary"] {{
        background: {'linear-gradient(135deg, #0284C7 0%, #0369A1 100%)' if is_light else 'linear-gradient(135deg, #0284C7 0%, #0891B2 100%)'} !important;
        border: 2px solid {'#0284C7' if is_light else '#00F0FF'} !important;
        color: #FFFFFF !important;
        box-shadow: {'0 4px 14px rgba(2, 132, 199, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.3)' if is_light else '0 0 22px rgba(0, 240, 255, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.35)'} !important;
        font-weight: 800 !important;
        transform: translateY(-2px) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35) !important;
    }}
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="stBaseButton-primary"]:hover {{
        background: {'linear-gradient(135deg, #0369A1 0%, #0284C7 100%)' if is_light else 'linear-gradient(135deg, #0891B2 0%, #00F0FF 100%)'} !important;
        color: #FFFFFF !important;
        box-shadow: {'0 6px 18px rgba(2, 132, 199, 0.55)' if is_light else '0 0 30px rgba(0, 240, 255, 0.75)'} !important;
    }}

    /* Live Telemetry Pulse Animation */
    @keyframes livePulse {{
        0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
        70% {{ transform: scale(1.1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }}
        100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
    }}
    .pulse-dot {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #10B981;
        display: inline-block;
        animation: livePulse 2s infinite;
        vertical-align: middle;
        margin-right: 6px;
    }}

    /* SIH & Regulatory Header Badges */
    .badge-sih {{
        background: linear-gradient(135deg, rgba(255, 153, 51, 0.2), rgba(19, 136, 8, 0.2));
        border: 1px solid rgba(255, 153, 51, 0.5);
        color: #FFB366;
        font-size: 0.78rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}
    .badge-cert {{
        background: rgba(0, 240, 255, 0.12);
        border: 1px solid rgba(0, 240, 255, 0.4);
        color: #00F0FF;
        font-size: 0.78rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}

    /* Quick Action Card Typography Enhancement */
    .qa-card {{
        padding: 0.65rem 0.85rem !important;
    }}
    .qa-card .qa-content {{
        display: flex;
        flex-direction: column;
        text-align: left;
        flex: 1;
        min-width: 0;
    }}
    .qa-card .qa-micro-tag {{
        font-size: 0.68rem;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 800;
        margin-bottom: 2px;
        color: {'#94A3B8' if not is_light else '#64748B'};
    }}
    .qa-card .qa-label {{
        font-size: 0.88rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: {'#FFFFFF' if not is_light else '#0F172A'};
    }}
    .qa-card:hover .qa-label {{
        color: {'#00F0FF' if not is_light else '#0284C7'};
    }}
    .qa-card .qa-arrow {{
        font-size: 0.95rem;
        font-weight: 800;
        color: {'#94A3B8' if not is_light else '#64748B'};
        transition: all 0.2s ease;
    }}
    .qa-card:hover .qa-arrow {{
        color: #FFFFFF;
        transform: translateX(3px);
    }}

    /* Domain Color Variants */
    .qa-emerald {{
        color: {'#34D399' if not is_light else '#059669'};
        border-left: 3px solid #10B981;
    }}
    .qa-emerald::before {{ background: linear-gradient(90deg, #10B981, transparent); }}
    .qa-emerald .qa-icon {{ background: rgba(16, 185, 129, 0.15); color: #10B981; }}
    .qa-emerald:hover {{
        box-shadow: 0 6px 24px rgba(16, 185, 129, {'0.35' if not is_light else '0.18'});
        border-color: #10B981;
        background: {'rgba(16, 185, 129, 0.08)' if not is_light else 'rgba(16, 185, 129, 0.04)'};
    }}

    .qa-violet {{
        color: {'#C084FC' if not is_light else '#7C3AED'};
        border-left: 3px solid #A855F7;
    }}
    .qa-violet::before {{ background: linear-gradient(90deg, #A855F7, transparent); }}
    .qa-violet .qa-icon {{ background: rgba(168, 85, 247, 0.15); color: #A855F7; }}
    .qa-violet:hover {{
        box-shadow: 0 6px 24px rgba(168, 85, 247, {'0.35' if not is_light else '0.18'});
        border-color: #A855F7;
        background: {'rgba(168, 85, 247, 0.08)' if not is_light else 'rgba(168, 85, 247, 0.04)'};
    }}

    .qa-cyan {{
        color: {'#5CCFE6' if not is_light else '#0284C7'};
        border-left: 3px solid #00F0FF;
    }}
    .qa-cyan::before {{ background: linear-gradient(90deg, #00F0FF, transparent); }}
    .qa-cyan .qa-icon {{ background: rgba(0, 240, 255, 0.12); color: #00F0FF; }}
    .qa-cyan:hover {{
        box-shadow: 0 6px 24px rgba(0, 240, 255, {'0.35' if not is_light else '0.18'});
        border-color: #00F0FF;
        background: {'rgba(0, 240, 255, 0.08)' if not is_light else 'rgba(0, 240, 255, 0.04)'};
    }}

    .qa-amber {{
        color: {'#FBBF24' if not is_light else '#D97706'};
        border-left: 3px solid #F59E0B;
    }}
    .qa-amber::before {{ background: linear-gradient(90deg, #F59E0B, transparent); }}
    .qa-amber .qa-icon {{ background: rgba(245, 158, 11, 0.15); color: #F59E0B; }}
    .qa-amber:hover {{
        box-shadow: 0 6px 24px rgba(245, 158, 11, {'0.35' if not is_light else '0.18'});
        border-color: #F59E0B;
        background: {'rgba(245, 158, 11, 0.08)' if not is_light else 'rgba(245, 158, 11, 0.04)'};
    }}

    .qa-crimson {{
        color: {'#FB7185' if not is_light else '#E11D48'};
        border-left: 3px solid #F43F5E;
    }}
    .qa-crimson::before {{ background: linear-gradient(90deg, #F43F5E, transparent); }}
    .qa-crimson .qa-icon {{ background: rgba(244, 63, 94, 0.15); color: #F43F5E; }}
    .qa-crimson:hover {{
        box-shadow: 0 6px 24px rgba(244, 63, 94, {'0.35' if not is_light else '0.18'});
        border-color: #F43F5E;
        background: {'rgba(244, 63, 94, 0.08)' if not is_light else 'rgba(244, 63, 94, 0.04)'};
    }}

    .qa-blue {{
        color: {'#38BDF8' if not is_light else '#0369A1'};
        border-left: 3px solid #0EA5E9;
    }}
    .qa-blue::before {{ background: linear-gradient(90deg, #0EA5E9, transparent); }}
    .qa-blue .qa-icon {{ background: rgba(14, 165, 233, 0.15); color: #0EA5E9; }}
    .qa-blue:hover {{
        box-shadow: 0 6px 24px rgba(14, 165, 233, {'0.35' if not is_light else '0.18'});
        border-color: #0EA5E9;
        background: {'rgba(14, 165, 233, 0.08)' if not is_light else 'rgba(14, 165, 233, 0.04)'};
    }}

    @media (max-width: 900px) {{
        .quick-action-grid {{
            grid-template-columns: repeat(3, 1fr);
        }}
    }}
    @media (max-width: 560px) {{
        .quick-action-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
    }}
    </style>
    """),
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Operational Scenarios Master Catalog
# --------------------------------------------------------------------------- #

SCENARIOS = [
    {
        "id": "01_nominal",
        "title": "01: Routine Patrol",
        "short_title": "S1 · Patrol",
        "tag": "NOMINAL PATROL",
        "badge": "safe",
        "icon": "⌖",
        "color": "#10B981",
        "ch4": 0.35, "o2": 20.8, "co": 8.0, "co2": 0.04, "h2": 0.0, "rssi": -65, "tilt": 3.5, "victim": False,
        "briefing": "Routine autonomous reconnaissance through unmapped Heading 4. All atmospheric readings and kinematic attitudes are well within safe operating limits.",
        "proves": "Baseline multi-sensor fusion stability, low-power mesh connectivity, and smooth tracked propulsion in zero-hazard conditions.",
    },
    {
        "id": "02_survivor",
        "title": "02: Trapped Survivor",
        "short_title": "S2 · BioLock",
        "tag": "BIO-RADAR LOCK",
        "badge": "safe",
        "icon": "◎",
        "color": "#F43F5E",
        "ch4": 0.50, "o2": 20.1, "co": 12.0, "co2": 0.08, "h2": 0.0, "rssi": -68, "tilt": 6.8, "victim": True,
        "briefing": "Sub-surface 400 MHz FMCW Bio-Radar locked onto rhythmic human micro-Doppler chest movement (0.32 Hz breathing) under 4.2m of collapsed rock/coal rubble.",
        "proves": "Sub-surface victim localization through void collapses without optical line of sight, unmuting duplex acoustic intercom for direct psychological rescue directives.",
    },
    {
        "id": "03_heating",
        "title": "03: Seam Heating",
        "short_title": "S3 · Heating",
        "tag": "SPONTANEOUS HEATING",
        "badge": "warn",
        "icon": "⌬",
        "color": "#F59E0B",
        "ch4": 0.85, "o2": 19.3, "co": 65.0, "co2": 0.65, "h2": 15.0, "rssi": -72, "tilt": 5.2, "victim": False,
        "briefing": "Elevated Carbon Monoxide (65 PPM) and oxygen deficit trigger a Graham's Ratio of 0.72, signaling the confirmed onset of spontaneous coal combustion.",
        "proves": "Real-time calculation of stoichiometric geochemical ratios to warn command brigades of invisible underground coal seam fires before smoke or flames break out.",
    },
    {
        "id": "04_dgms_trip",
        "title": "04: DGMS CH₄ Interlock",
        "short_title": "S4 · CH₄ Trip",
        "tag": "1.25% LEL INTERLOCK",
        "badge": "danger",
        "icon": "⬡",
        "color": "#EF4444",
        "ch4": 1.45, "o2": 18.9, "co": 18.0, "co2": 0.12, "h2": 5.0, "rssi": -70, "tilt": 4.1, "victim": False,
        "briefing": "Methane reaches 1.45% vol (crossing the mandatory 1.25% DGMS limit). Electrical actuator power is automatically isolated to eliminate ignition sparks.",
        "proves": "Full compliance with statutory DGMS Technical Circular 02/2021 safety interlocks for mobile electrical equipment in Degree III Gassy Coal Mines.",
    },
    {
        "id": "05_incline",
        "title": "05: Slag Incline / Tilt",
        "short_title": "S5 · Incline",
        "tag": "ROLLOVER ALERT",
        "badge": "danger",
        "icon": "▲",
        "color": "#EAB308",
        "ch4": 0.40, "o2": 20.4, "co": 10.0, "co2": 0.03, "h2": 0.0, "rssi": -75, "tilt": 38.5, "victim": False,
        "briefing": "Chassis enters a steep 38.5° rubble slag slope exceeding the 30° safe traversal threshold. Active flipper sub-tracks engage to prevent rollover.",
        "proves": "Articulated twin-chassis dynamic tilt compensation, 220 mm step clearance, and safety cutoff preventing vehicle stranding in irregular collapse terrain.",
    },
    {
        "id": "06_mesh_drop",
        "title": "06: Mesh Relay Hop",
        "short_title": "S6 · Mesh Hop",
        "tag": "RF SIGNAL DEGRADED",
        "badge": "warn",
        "icon": "⎇",
        "color": "#06B6D4",
        "ch4": 0.45, "o2": 20.2, "co": 11.0, "co2": 0.04, "h2": 0.0, "rssi": -96, "tilt": 4.0, "victim": False,
        "briefing": "Sub-1GHz LoRa signal drops to -96 dBm around deep blind pillars. Rover engages multi-hop relay forwarding through deployed repeater pods.",
        "proves": "Sub-surface communication resilience and non-line-of-sight RF link maintenance across complex room-and-pillar mining geometries.",
    },
]

# --------------------------------------------------------------------------- #
# Helpers & Badge Generators
# --------------------------------------------------------------------------- #

def get_badge(text: str, kind: str) -> str:
    return f'<span class="badge badge-{kind}">{text}</span>'

def get_oxygen_kind(state: OxygenState) -> str:
    return {
        OxygenState.NORMAL: "safe",
        OxygenState.ACCEPTABLE: "warn",
        OxygenState.DEFICIENT: "danger",
        OxygenState.DANGEROUS: "danger",
    }[state]

def get_co_kind(state: CoExposureState) -> str:
    return {
        CoExposureState.NORMAL: "safe",
        CoExposureState.ELEVATED: "warn",
        CoExposureState.HIGH: "warn",
        CoExposureState.SEVERE: "danger",
        CoExposureState.IDLH: "danger",
    }[state]

def combine_hazard_level(base: HazardLevel, rssi: float, tilt: float, ch4_pct: float) -> HazardLevel:
    order = [HazardLevel.NOMINAL, HazardLevel.CAUTION, HazardLevel.WARNING, HazardLevel.CRITICAL]
    level = base
    if ch4_pct >= 1.25 and order.index(level) < order.index(HazardLevel.WARNING):
        level = HazardLevel.WARNING
    if rssi <= -95 or tilt > 45 or ch4_pct >= 5.0:
        level = HazardLevel.CRITICAL
    elif rssi <= -82 or tilt > 30:
        if order.index(HazardLevel.WARNING) > order.index(level):
            level = HazardLevel.WARNING
    return level

# --------------------------------------------------------------------------- #
# Session State Initialization
# --------------------------------------------------------------------------- #

if "analyzer" not in st.session_state:
    st.session_state.analyzer = MineAtmosphericAnalyzer(history_window=50, sample_interval_s=2.0)
if "telemetry_log" not in st.session_state:
    st.session_state.telemetry_log = []
if "radar_tick" not in st.session_state:
    st.session_state.radar_tick = 0
if "active_scenario_idx" not in st.session_state:
    st.session_state.active_scenario_idx = 0  # Default to Scenario 01: Routine Patrol
if "is_custom_mode" not in st.session_state:
    st.session_state.is_custom_mode = False

analyzer = st.session_state.analyzer

# --------------------------------------------------------------------------- #
# Top Header Banner
# --------------------------------------------------------------------------- #

st.markdown(
    textwrap.dedent(f"""
    <div class="setu-top-header">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1.2rem;">
            <div style="display: flex; align-items: center; gap: 1.1rem;">
                <!-- Authentic Tactical Insignia Crest -->
                <div style="flex-shrink: 0; filter: drop-shadow(0 0 12px rgba(0, 240, 255, 0.4));">
                    <svg width="56" height="56" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <polygon points="50,4 92,26 92,74 50,96 8,74 8,26" stroke="#00F0FF" stroke-width="3" fill="rgba(0, 240, 255, 0.09)"/>
                        <polygon points="50,14 82,31 82,69 50,86 18,69 18,31" stroke="rgba(245, 158, 11, 0.6)" stroke-width="1.8" fill="rgba(19, 28, 40, 0.6)"/>
                        <circle cx="50" cy="50" r="22" stroke="#00F0FF" stroke-width="1.6" stroke-dasharray="4 3" opacity="0.8"/>
                        <circle cx="50" cy="50" r="10" stroke="#10B981" stroke-width="1.4" opacity="0.9"/>
                        <circle cx="50" cy="50" r="4" fill="#00F0FF"/>
                        <line x1="50" y1="8" x2="50" y2="92" stroke="#00F0FF" stroke-width="1" opacity="0.35"/>
                        <line x1="8" y1="50" x2="92" y2="50" stroke="#00F0FF" stroke-width="1" opacity="0.35"/>
                    </svg>
                </div>
                <div>
                    <div class="setu-brand-title">
                        <span>PROJECT SETU</span>
                        <span class="setu-badge-hindi">सेतु</span>
                        <span class="badge-cert">
                            <i class="fas fa-shield-halved" style="color: #00F0FF;"></i> DGMS Ex d I Mb
                        </span>
                        <span class="badge-sih">
                            🇮🇳 SIH 2026 // PS: SIH26039
                        </span>
                        <span style="font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; background: rgba(255,255,255,0.1); color: #FFFFFF; padding: 0.2rem 0.55rem; border-radius: 5px; border: 1px solid rgba(255,255,255,0.2);">
                            {'☼ HIGH-VIS HUD' if is_light else '◐ 0-LUX HUD'}
                        </span>
                    </div>
                    <div class="setu-subtitle">
                        <b>Subterranean Mine Rescue & Multi-Spectral Reconnaissance Ground Control Station</b><br>
                        Autonomous Tracked Crawler · 400 MHz FMCW Bio-Radar Array · 5-Gas Geochemical Diagnostics · 3D LIO-SAM SLAM
                    </div>
                </div>
            </div>
            <div style="text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 0.84rem; background: rgba(0, 0, 0, 0.25); padding: 0.75rem 1rem; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08);">
                <div style="display: flex; align-items: center; justify-content: flex-end; gap: 6px;">
                    <span class="pulse-dot"></span>
                    <span style="color: {SAFE_GREEN}; font-weight: 800; letter-spacing: 0.03em;">MESH TELEMETRY SYNCED</span>
                </div>
                <div style="color: #94A3B8; margin-top: 0.3rem;">Tactical Node: <span style="color: #FFFFFF; font-weight: 700;">SETU-ROVER-ALPHA-01</span></div>
                <div style="color: #94A3B8;">RF Carriers: <span style="color: #00F0FF; font-weight: 600;">865MHz LoRa</span> · <span style="color: #F59E0B; font-weight: 600;">5.8GHz COFDM</span></div>
            </div>
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Rich Color-Coded Quick-Action Command Cards (Font Awesome + Domain Colors)
# --------------------------------------------------------------------------- #

st.markdown(
    textwrap.dedent(f"""
    <div class="quick-action-grid">
        <a href="https://setu-mine-rescue-rover.vercel.app/" target="_blank" class="qa-card qa-emerald">
            <div class="qa-icon"><i class="fas fa-globe"></i></div>
            <div class="qa-content">
                <span class="qa-micro-tag">OFFICIAL CLOUD</span>
                <span class="qa-label">Web Platform</span>
            </div>
            <div class="qa-arrow">→</div>
        </a>
        <a href="https://github.com/abarhammalik/SETU-Dashboard" target="_blank" class="qa-card qa-violet">
            <div class="qa-icon"><i class="fab fa-github"></i></div>
            <div class="qa-content">
                <span class="qa-micro-tag">OPEN SOURCE</span>
                <span class="qa-label">GitHub Repo</span>
            </div>
            <div class="qa-arrow">→</div>
        </a>
        <a href="https://setu-mine-rescue-rover.vercel.app/#demonstrations" target="_blank" class="qa-card qa-cyan">
            <div class="qa-icon"><i class="fas fa-play-circle"></i></div>
            <div class="qa-content">
                <span class="qa-micro-tag">6 MISSIONS</span>
                <span class="qa-label">Field Demos</span>
            </div>
            <div class="qa-arrow">→</div>
        </a>
        <a href="https://setu-mine-rescue-rover.vercel.app/#hardware-labeling" target="_blank" class="qa-card qa-amber">
            <div class="qa-icon"><i class="fas fa-microchip"></i></div>
            <div class="qa-content">
                <span class="qa-micro-tag">AVIONICS CAD</span>
                <span class="qa-label">Rover Schematic</span>
            </div>
            <div class="qa-arrow">→</div>
        </a>
        <a href="https://setu-mine-rescue-rover.vercel.app/#ocu-sim" target="_blank" class="qa-card qa-crimson">
            <div class="qa-icon"><i class="fas fa-gamepad"></i></div>
            <div class="qa-content">
                <span class="qa-micro-tag">OPERATOR HUD</span>
                <span class="qa-label">OCU Simulator</span>
            </div>
            <div class="qa-arrow">→</div>
        </a>
        <a href="https://setu-mine-rescue-rover.vercel.app/#credibility" target="_blank" class="qa-card qa-blue">
            <div class="qa-icon"><i class="fas fa-shield-halved"></i></div>
            <div class="qa-content">
                <span class="qa-micro-tag">COMPLIANCE</span>
                <span class="qa-label">DGMS Roadmap</span>
            </div>
            <div class="qa-arrow">→</div>
        </a>
    </div>
    """),
    unsafe_allow_html=True,
)

st.markdown('<div class="hazard-stripe"></div>', unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# NEW UX: Tactical Operational Scenarios Command Toolbar (Main Screen Stepper)
# --------------------------------------------------------------------------- #

st.markdown(
    textwrap.dedent(f"""
    <div class="scenario-toolbar">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
            <div class="scenario-title">
                <i class="fas fa-crosshairs" style="color: {ACCENT_PRIMARY}; font-size: 1.1rem;"></i>
                <span>OPERATIONAL MISSION SCENARIO SELECTOR</span>
                <span style="font-size: 0.78rem; font-weight: 500; color: {APP_TEXT_MUTED}; opacity: 0.8;">// Jury Evaluation & Demonstration Deck</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <div style="display: flex; gap: 3px;">
                    {''.join([f'<div style="width: 8px; height: 8px; border-radius: 50%; background: {"' + ACCENT_PRIMARY + '" if i <= st.session_state.active_scenario_idx else "' + APP_TEXT_MUTED + '"}; opacity: {"1" if i <= st.session_state.active_scenario_idx else "0.3"};"></div>' for i in range(6)])}
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 700; color: {ACCENT_PRIMARY}; background: {'rgba(0, 240, 255, 0.08)' if not is_light else 'rgba(2, 132, 199, 0.08)'}; padding: 0.25rem 0.65rem; border-radius: 6px; border: 1px solid {'rgba(0, 240, 255, 0.2)' if not is_light else 'rgba(2, 132, 199, 0.2)'};">
                    STAGE {st.session_state.active_scenario_idx + 1} / 6
                </div>
            </div>
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

# Stepper Control Row
step_col_prev, step_col_pills, step_col_next, step_col_custom = st.columns([1.1, 7.8, 1.1, 1.8])

with step_col_prev:
    if st.button("◀ Prev Stage", use_container_width=True):
        st.session_state.active_scenario_idx = (st.session_state.active_scenario_idx - 1) % len(SCENARIOS)
        st.session_state.is_custom_mode = False
        st.rerun()

with step_col_pills:
    # Segmented scenario pill buttons with high-contrast active states
    p_cols = st.columns(len(SCENARIOS))
    for idx, sc in enumerate(SCENARIOS):
        with p_cols[idx]:
            is_active = (not st.session_state.is_custom_mode) and (st.session_state.active_scenario_idx == idx)
            label_text = sc.get("short_title", f"Stage {idx+1}")
            btn_label = f"{sc['icon']} {label_text}"
            if st.button(btn_label, key=f"sc_btn_{idx}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.active_scenario_idx = idx
                st.session_state.is_custom_mode = False
                st.rerun()

with step_col_next:
    if st.button("Next Stage ▶", use_container_width=True):
        st.session_state.active_scenario_idx = (st.session_state.active_scenario_idx + 1) % len(SCENARIOS)
        st.session_state.is_custom_mode = False
        st.rerun()

with step_col_custom:
    custom_label = "⚙ Manual Sliders" if not st.session_state.is_custom_mode else "✓ Sliders Active"
    if st.button(custom_label, use_container_width=True, type="primary" if st.session_state.is_custom_mode else "secondary"):
        st.session_state.is_custom_mode = not st.session_state.is_custom_mode
        st.rerun()

# Scenario Briefing Box
active_sc = SCENARIOS[st.session_state.active_scenario_idx]
if st.session_state.is_custom_mode:
    st.markdown(
        textwrap.dedent(f"""
        <div class="briefing-box" style="border-left-color: {ACCENT_AMBER};">
            <div style="font-weight: 700; color: {APP_TEXT};">
                ⚙ CUSTOM MANUAL TELEMETRY MODE ACTIVE
            </div>
            <div style="color: {APP_TEXT_MUTED}; margin-top: 0.2rem;">
                Adjust any sensor slider freely in the sidebar to simulate custom coal mine atmospheric mixtures or kinematics.
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        textwrap.dedent(f"""
        <div class="briefing-box" style="border-left: 5px solid {active_sc.get('color', ACCENT_PRIMARY)}; box-shadow: 0 4px 20px rgba(0, 0, 0, {'0.25' if not is_light else '0.06'}), inset 0 0 15px {active_sc.get('color', ACCENT_PRIMARY)}15;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <span style="font-size: 1.25rem; color: {active_sc.get('color', ACCENT_PRIMARY)}; filter: drop-shadow(0 0 6px {active_sc.get('color', ACCENT_PRIMARY)}88);">{active_sc['icon']}</span>
                    <span style="font-weight: 800; color: {APP_TEXT}; font-size: 1.02rem; font-family: 'Space Grotesk', sans-serif;">
                        {active_sc['title']}
                    </span>
                    {get_badge(active_sc['tag'], active_sc['badge'])}
                </div>
                <div style="font-size: 0.82rem; font-family: 'JetBrains Mono', monospace; color: {active_sc.get('color', ACCENT_PRIMARY)}; font-weight: 700; background: {active_sc.get('color', ACCENT_PRIMARY)}18; border: 1px solid {active_sc.get('color', ACCENT_PRIMARY)}40; padding: 0.25rem 0.65rem; border-radius: 5px;">
                    MISSION PROFILE {st.session_state.active_scenario_idx + 1} OF 6
                </div>
            </div>
            <div style="color: {'#F1F5F9' if not is_light else '#1E293B'}; margin-top: 0.5rem; line-height: 1.55; font-size: 0.95rem;">
                <b style="color: {active_sc.get('color', ACCENT_PRIMARY)}; font-weight: 800;">Tactical Briefing:</b> {active_sc['briefing']}
            </div>
            <div style="color: {'#CBD5E1' if not is_light else '#475569'}; font-size: 0.88rem; margin-top: 0.4rem; line-height: 1.45; border-top: 1px dashed {'rgba(255,255,255,0.18)' if not is_light else 'rgba(0,0,0,0.1)'}; padding-top: 0.4rem;">
                <b style="color: {'#FFFFFF' if not is_light else '#0F172A'}; font-weight: 800;">Engineering & Regulatory Verification:</b> {active_sc['proves']}
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------- #
# Telemetry Parameters Selection (From Scenario or Sliders)
# --------------------------------------------------------------------------- #

if not st.session_state.is_custom_mode:
    ch4_val = active_sc["ch4"]
    o2_val = active_sc["o2"]
    co_val = active_sc["co"]
    co2_val = active_sc["co2"]
    h2_val = active_sc["h2"]
    rssi_val = active_sc["rssi"]
    tilt_val = active_sc["tilt"]
    victim_active = active_sc["victim"]
else:
    ch4_val = 0.4
    o2_val = 20.4
    co_val = 12.0
    co2_val = 0.04
    h2_val = 0.0
    rssi_val = -68
    tilt_val = 4.2
    victim_active = False

# --------------------------------------------------------------------------- #
# Left Side Panel: Tactical Telemetry & Sensor Calibration Deck
# --------------------------------------------------------------------------- #

calib_status_text = "⚙ MANUAL SLIDERS ACTIVE" if st.session_state.is_custom_mode else f"🔒 SYNCED: S{st.session_state.active_scenario_idx + 1} PROFILE"
calib_status_color = ACCENT_AMBER if st.session_state.is_custom_mode else SAFE_GREEN

st.sidebar.markdown(
    textwrap.dedent(f"""
    <div style="margin-top: 1rem; margin-bottom: 0.75rem; background: {'#FFFFFF' if is_light else '#121C2B'}; border: 1.5px solid {'#CBD5E1' if is_light else '#233549'}; border-radius: 10px; padding: 0.85rem 1rem; box-shadow: {'0 2px 8px rgba(0,0,0,0.04)' if is_light else '0 4px 14px rgba(0,0,0,0.3)'};">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.96rem; font-weight: 800; color: {'#0F172A' if is_light else '#FFFFFF'}; letter-spacing: -0.01em;">
                ⚙ TELEMETRY CALIBRATION
            </span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 800; color: {calib_status_color}; background: {calib_status_color}18; border: 1px solid {calib_status_color}45; padding: 0.15rem 0.45rem; border-radius: 4px;">
                {calib_status_text}
            </span>
        </div>
        <div style="font-size: 0.76rem; color: {'#64748B' if is_light else '#CBD5E1'}; font-family: 'Inter', sans-serif; line-height: 1.4;">
            Fine-tune multi-gas mixtures, kinematics, and sub-surface vital parameters in real-time.
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

# Tactical Quick-Launch Command Buttons
sb_col1, sb_col2 = st.sidebar.columns(2)
with sb_col1:
    st.link_button("🌐 Web Platform", "https://setu-mine-rescue-rover.vercel.app/", use_container_width=True)
with sb_col2:
    st.link_button("⌥ GitHub Repo", "https://github.com/abarhammalik/SETU-Dashboard", use_container_width=True)

# Module 1: 5-Gas Atmospheric Suite
st.sidebar.markdown(
    textwrap.dedent(f"""
    <div class="sidebar-mod-badge" style="color: {'#B45309' if is_light else '#F59E0B'}; margin-top: 1rem; display: flex; align-items: center; justify-content: space-between;">
        <span>⌬ MODULE 01 · 5-GAS ATMOSPHERICS</span>
        <span style="font-size: 0.68rem; font-family: 'JetBrains Mono', monospace; opacity: 0.85;">CH₄·CO·O₂·CO₂·H₂</span>
    </div>
    """),
    unsafe_allow_html=True,
)
ch4_input = st.sidebar.slider("CH₄ Methane (% vol)", 0.0, 15.0, float(ch4_val), 0.05, help="DGMS Mandatory Cutoff threshold: 1.25% vol")
o2_input = st.sidebar.slider("O₂ Oxygen (% vol)", 5.0, 21.5, float(o2_val), 0.1, help="Safe atmospheric range: 19.5% – 21.0%")
co_input = st.sidebar.slider("CO Carbon Monoxide (PPM)", 0.0, 300.0, float(co_val), 5.0, help="Graham's Ratio spontaneous coal heating tracker")
co2_input = st.sidebar.slider("CO₂ Carbon Dioxide (% vol)", 0.0, 3.5, float(co2_val), 0.01)
h2_input = st.sidebar.slider("H₂ Hydrogen (PPM)", 0.0, 500.0, float(h2_val), 5.0)

# Module 2: Kinematics & Mesh RF
st.sidebar.markdown(
    textwrap.dedent(f"""
    <div class="sidebar-mod-badge" style="color: {'#0369A1' if is_light else '#00F0FF'}; margin-top: 1rem; display: flex; align-items: center; justify-content: space-between;">
        <span>⌖ MODULE 02 · KINEMATICS & RF MESH</span>
        <span style="font-size: 0.68rem; font-family: 'JetBrains Mono', monospace; opacity: 0.85;">RSSI · TILT</span>
    </div>
    """),
    unsafe_allow_html=True,
)
rssi_input = st.sidebar.slider("Sub-GHz Mesh RSSI (dBm)", -110, -40, int(rssi_val), 1, help="Signal drop below -95 dBm triggers multi-hop autonomous relay")
tilt_input = st.sidebar.slider("Chassis Pitch/Roll Tilt (°)", 0.0, 55.0, float(tilt_val), 0.5, help="30° safe traversal margin; flipper compensation above 33°")

# Module 3: FMCW Sub-Surface Bio-Radar
st.sidebar.markdown(
    textwrap.dedent(f"""
    <div class="sidebar-mod-badge" style="color: {'#BE123C' if is_light else '#F43F5E'}; margin-top: 1rem; display: flex; align-items: center; justify-content: space-between;">
        <span>◎ MODULE 03 · FMCW BIO-RADAR VITAL ARRAY</span>
        <span style="font-size: 0.68rem; font-family: 'JetBrains Mono', monospace; opacity: 0.85;">400MHz UWB</span>
    </div>
    """),
    unsafe_allow_html=True,
)
sim_victim = st.sidebar.checkbox("Trigger Trapped Survivor Respiration (0.32 Hz)", value=victim_active)
sim_drift = st.sidebar.checkbox("Inject Dynamic Sensor Noise & Drift", value=False)

# Sidebar Compliance Seal & Clock Footer
st.sidebar.markdown(
    textwrap.dedent(f"""
    <div class="sidebar-compliance-card">
        <div style="display: flex; align-items: center; gap: 6px; font-weight: 700; color: {'#0F172A' if is_light else '#F1F5F9'};">
            <i class="fas fa-shield-halved" style="color: {'#0284C7' if is_light else '#00F0FF'};"></i> STATUTORY DGMS COMPLIANCE
        </div>
        <div style="margin-top: 4px; line-height: 1.45;">
            • DGMS Tech Circular 02/2021<br>
            • Flameproof Enclosure: Ex d I Mb<br>
            • CH₄ 1.25% Electrical Cutoff: <b style="color: {'#16A34A' if is_light else '#10B981'};">ACTIVE</b>
        </div>
        <div style="margin-top: 6px; padding-top: 4px; border-top: 1px dashed rgba(128,128,128,0.25); font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;">
            GCS Live Timestamp: {datetime.now().strftime('%H:%M:%S')} IST
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Run Atmospheric Analytics
# --------------------------------------------------------------------------- #

res = analyzer.analyze(ch4_input, o2_input, co_input, co2_pct=co2_input, h2_ppm=h2_input)
overall_hazard = combine_hazard_level(res.hazard_level, rssi_input, tilt_input, ch4_input)

# Log to rolling telemetry history
st.session_state.telemetry_log.append(
    {
        "sample": len(st.session_state.telemetry_log),
        "CH4": ch4_input,
        "CO": co_input,
        "CO2": co2_input,
        "O2": o2_input,
        "GR": res.grahams_ratio,
        "Tilt": tilt_input,
        "RSSI": rssi_input,
    }
)
st.session_state.telemetry_log = st.session_state.telemetry_log[-60:]

# --------------------------------------------------------------------------- #
# Dynamic Hazard Notification Banner
# --------------------------------------------------------------------------- #

hazard_key = overall_hazard.name if hasattr(overall_hazard, "name") else str(overall_hazard)
hazard_colors = {
    "NOMINAL": SAFE_GREEN,
    "CAUTION": ACCENT_AMBER,
    "WARNING": "#EA580C",
    "CRITICAL": DANGER_RED,
}

hazard_messages = {
    "NOMINAL": "SYSTEM NOMINAL // MINE ATMOSPHERE STABLE · 4-BELT CRAWLER READY · MESH LINK ACTIVE",
    "CAUTION": "TACTICAL CAUTION // ATMOSPHERIC TREND DEVIATION DETECTED · INCREASE LOGGING FREQUENCY",
    "WARNING": "HAZARD WARNING // ELEVATED FIREDAMP OR SEAM HEATING · PREPARE EMERGENCY EXTRACTION",
    "CRITICAL": "CRITICAL HAZARD // LETHAL ATMOSPHERE OR IMMINENT ROLLOVER CONFIRMED · EMERGENCY HALT",
}

banner_bg = hazard_colors.get(hazard_key, SAFE_GREEN)
banner_msg = hazard_messages.get(hazard_key, "SYSTEM NOMINAL // MINE MONITORING ACTIVE")
dgms_interlock_msg = ""
if ch4_input >= 1.25:
    dgms_interlock_msg = " [DGMS 1.25% CH4 INTERLOCK TRIPPED: ELECTRICAL ACTUATORS CUTOFF]"

st.markdown(
    textwrap.dedent(f"""
    <div class="hazard-banner" style="background: linear-gradient(90deg, {banner_bg} 0%, rgba(30, 41, 59, 0.96) 100%);">
        <div>{banner_msg}{dgms_interlock_msg}</div>
        <div class="hazard-advisory">{res.advisory} | Kinematics: Tilt {tilt_input:.1f}° (Max 33° rock slag margin) | RF RSSI: {rssi_input} dBm</div>
    </div>
    """),
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Primary KPI Metric Ribbon
# --------------------------------------------------------------------------- #

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    ch4_status = "DGMS TRIP ≥1.25%" if ch4_input >= 1.25 else f"LEL {analyzer.CH4_LEL:.0f}%"
    st.metric("CH₄ Methane", f"{ch4_input:.2f}%", ch4_status, delta_color="inverse" if ch4_input >= 1.25 else "normal")
    st.markdown(get_badge(res.methane_state.value, "danger" if ch4_input >= 1.25 else "safe"), unsafe_allow_html=True)

with kpi2:
    st.metric("O₂ Oxygen", f"{o2_input:.1f}%", f"{o2_input - 20.93:+.2f}% vs Air")
    st.markdown(get_badge(res.oxygen_state.value, get_oxygen_kind(res.oxygen_state)), unsafe_allow_html=True)

with kpi3:
    st.metric("CO Monoxide", f"{co_input:.0f} PPM", "Safe < 25 PPM", delta_color="inverse" if co_input >= 25 else "normal")
    st.markdown(get_badge(res.co_exposure_state.value, get_co_kind(res.co_exposure_state)), unsafe_allow_html=True)

with kpi4:
    st.metric("Graham's Ratio", f"{res.grahams_ratio}", res.grahams_status.replace("_", " ").title())
    gr_badge = "safe" if res.grahams_ratio < 0.4 else ("warn" if res.grahams_ratio < 1.0 else "danger")
    st.markdown(get_badge(f"GR {res.grahams_ratio}", gr_badge), unsafe_allow_html=True)

with kpi5:
    bio_label = "BREATHING LOCK" if sim_victim else "SCANNING VOIDS"
    st.metric("FMCW Bio-Radar", "SURVIVOR DETECTED" if sim_victim else "NO TARGET", bio_label)
    st.markdown(get_badge("0.32 Hz Human Vital" if sim_victim else "Standby Array", "safe" if sim_victim else "info"), unsafe_allow_html=True)

with kpi6:
    mesh_status = "Optimal" if rssi_input > -80 else ("Marginal" if rssi_input > -92 else "Critical Dropout")
    st.metric("LoRa Mesh Signal", f"{rssi_input} dBm", mesh_status)
    st.markdown(get_badge(f"Node 01 // {mesh_status}", "safe" if rssi_input > -85 else "danger"), unsafe_allow_html=True)

st.markdown("")

# --------------------------------------------------------------------------- #
# Multi-Domain Mission Control Navigation & Theme Toggle
# --------------------------------------------------------------------------- #

nav_bar_col1, nav_bar_col2 = st.columns([7.6, 2.4], vertical_alignment="center")

with nav_bar_col1:
    st.markdown(
        textwrap.dedent(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.8rem; background: {'rgba(19, 28, 40, 0.75)' if not is_light else '#FFFFFF'}; border: 1px solid {PANEL_BORDER}; border-radius: 10px; padding: 0.65rem 1rem; box-shadow: {PANEL_SHADOW};">
            <div style="display: flex; align-items: center; gap: 0.65rem;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 1.08rem; font-weight: 800; color: {APP_TEXT}; letter-spacing: -0.01em;">
                    ◈ SUBSYSTEM COMMAND MATRIX
                </span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #00F0FF; background: rgba(0, 240, 255, 0.12); border: 1px solid rgba(0, 240, 255, 0.35); padding: 0.15rem 0.5rem; border-radius: 4px;">
                    5 TELEMETRY DOMAINS
                </span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.45rem; font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; flex-wrap: wrap;">
                <span style="color: {'#00F0FF' if not is_light else '#0284C7'}; background: rgba(0, 240, 255, 0.1); padding: 0.15rem 0.45rem; border-radius: 4px; border: 1px solid rgba(0, 240, 255, 0.3); font-weight: 600;">⌖ HUD 30 FPS</span>
                <span style="color: {'#F59E0B' if not is_light else '#D97706'}; background: rgba(245, 158, 11, 0.1); padding: 0.15rem 0.45rem; border-radius: 4px; border: 1px solid rgba(245, 158, 11, 0.3); font-weight: 600;">⌬ 5-GAS RUN</span>
                <span style="color: {'#F43F5E' if not is_light else '#E11D48'}; background: rgba(244, 63, 94, 0.1); padding: 0.15rem 0.45rem; border-radius: 4px; border: 1px solid rgba(244, 63, 94, 0.3); font-weight: 600;">◎ 400MHz FMCW</span>
                <span style="color: {'#A855F7' if not is_light else '#7C3AED'}; background: rgba(168, 85, 247, 0.1); padding: 0.15rem 0.45rem; border-radius: 4px; border: 1px solid rgba(168, 85, 247, 0.3); font-weight: 600;">◈ YOLOv10 &lt;3ms</span>
                <span style="color: {'#10B981' if not is_light else '#059669'}; background: rgba(16, 185, 129, 0.1); padding: 0.15rem 0.45rem; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.3); font-weight: 600;">◫ MESH ONLINE</span>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )

with nav_bar_col2:
    nav_theme_label = "◐ 0-LUX TACTICAL DARK" if is_light else "☼ HIGH-VIS LIGHT HUD"
    if st.button(nav_theme_label, key="nav_theme_toggle_btn", use_container_width=True, help="Toggle between 0-Lux Tactical Dark HUD and High-Visibility Light HUD"):
        st.session_state.theme_mode = "dark" if is_light else "light"
        st.rerun()

tab_ops, tab_gas, tab_radar, tab_ai, tab_eco = st.tabs([
    "⌖ 01 · MISSION FLIGHT DECK",
    "⌬ 02 · 5-GAS ATMOSPHERICS",
    "◎ 03 · FMCW BIO-RADAR ARRAY",
    "◈ 04 · EDGE AI & 3D SLAM",
    "◫ 05 · SETU ECOSYSTEM & WEB",
])

# --------------------------------------------------------------------------- #
# Tab 1: Operational Mission Deck
# --------------------------------------------------------------------------- #

with tab_ops:
    c_left, c_right = st.columns([7, 5])

    with c_left:
        st.subheader("Subterranean Quad-Feed Telemetry HUD")
        hud_col1, hud_col2 = st.columns(2)
        with hud_col1:
            st.markdown(
                textwrap.dedent(f"""
                <div class="panel-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                        <span style="font-weight: 700; color: {APP_TEXT}; font-size: 0.88rem;">CAM 01 // SONY IMX662 RGB</span>
                        <span class="badge badge-safe">FHD 30 FPS</span>
                    </div>
                    <div style="height: 120px; background: {FEED_BG}; border-radius: 6px; display: flex; align-items: center; justify-content: center; border: 1px dashed {FEED_BORDER};">
                        <div style="text-align: center; color: {APP_TEXT_MUTED}; font-size: 0.82rem; font-family: 'JetBrains Mono', monospace; line-height: 1.5;">
                            <b style="color: {APP_TEXT};">[ 5.8 GHz COFDM DIGITAL STREAM ]</b><br>
                            <span style="color: {SAFE_GREEN};">Active · &lt; 180ms Latency</span><br>
                            Resolution: 1920x1080p
                        </div>
                    </div>
                </div>
                """),
                unsafe_allow_html=True,
            )
        with hud_col2:
            st.markdown(
                textwrap.dedent(f"""
                <div class="panel-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                        <span style="font-weight: 700; color: {APP_TEXT}; font-size: 0.88rem;">CAM 02 // FLIR BOSON THERMAL</span>
                        <span class="badge badge-warn">&lt;50 mK NETD</span>
                    </div>
                    <div style="height: 120px; background: {'#FFF1F2' if is_light else '#1A0D0D'}; border-radius: 6px; display: flex; align-items: center; justify-content: center; border: 1px dashed rgba(239, 68, 68, 0.4);">
                        <div style="text-align: center; color: {APP_TEXT_MUTED}; font-size: 0.82rem; font-family: 'JetBrains Mono', monospace; line-height: 1.5;">
                            <b style="color: {APP_TEXT};">[ RADIOMETRIC 8–14 µm LWIR ]</b><br>
                            <span style="color: {ACCENT_AMBER};">Coal Seam: 28.4°C · Normal</span><br>
                            Human Signature: Standby
                        </div>
                    </div>
                </div>
                """),
                unsafe_allow_html=True,
            )

        hud_col3, hud_col4 = st.columns(2)
        with hud_col3:
            st.markdown(
                textwrap.dedent(f"""
                <div class="panel-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                        <span style="font-weight: 700; color: {APP_TEXT}; font-size: 0.88rem;">CAM 03 // 850nm NoIR NIGHT VISION</span>
                        <span class="badge badge-info">0-LUX ILLUM</span>
                    </div>
                    <div style="height: 120px; background: {'#F0FDF4' if is_light else '#051410'}; border-radius: 6px; display: flex; align-items: center; justify-content: center; border: 1px dashed rgba(16, 185, 129, 0.4);">
                        <div style="text-align: center; color: {APP_TEXT_MUTED}; font-size: 0.82rem; font-family: 'JetBrains Mono', monospace; line-height: 1.5;">
                            <b style="color: {APP_TEXT};">[ 850nm IR LED ARRAY ]</b><br>
                            <span style="color: {SAFE_GREEN};">Active · Penetrating Heavy Dust</span><br>
                            Depth Clarity: Nominal
                        </div>
                    </div>
                </div>
                """),
                unsafe_allow_html=True,
            )
        with hud_col4:
            st.markdown(
                textwrap.dedent(f"""
                <div class="panel-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                        <span style="font-weight: 700; color: {APP_TEXT}; font-size: 0.88rem;">OCCUPANCY // OUSTER OS0-128</span>
                        <span class="badge badge-safe">3D LIO-SAM</span>
                    </div>
                    <div style="height: 120px; background: {'#F0F9FF' if is_light else '#0A111C'}; border-radius: 6px; display: flex; align-items: center; justify-content: center; border: 1px dashed rgba(2, 132, 199, 0.4);">
                        <div style="text-align: center; color: {APP_TEXT_MUTED}; font-size: 0.82rem; font-family: 'JetBrains Mono', monospace; line-height: 1.5;">
                            <b style="color: {APP_TEXT};">[ 128 CH 360° LiDAR ]</b><br>
                            <span style="color: {ACCENT_PRIMARY};">655k pts/sec · Drift-Free SLAM</span><br>
                            Heading: Room & Pillar Seam #3
                        </div>
                    </div>
                </div>
                """),
                unsafe_allow_html=True,
            )

    with c_right:
        st.subheader("Subsystem Telemetry Matrix")
        tilt_status = "CRITICAL TILT" if tilt_input > 35 else ("Warning Tilt" if tilt_input > 25 else "Stable Nominal")
        tilt_badge = "danger" if tilt_input > 35 else ("warn" if tilt_input > 25 else "safe")

        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card">
                <div class="panel-row">
                    <span class="label">Chassis Locomotion</span>
                    <span class="val">Articulated Twin-Crawler</span>
                </div>
                <div class="panel-row">
                    <span class="label">Motor Drivers</span>
                    <span class="val">4x BTS7960 43A H-Bridges</span>
                </div>
                <div class="panel-row">
                    <span class="label">Rollover Pitch / Roll</span>
                    <span class="val">{tilt_input:.1f}° {get_badge(tilt_status, tilt_badge)}</span>
                </div>
                <div class="panel-row">
                    <span class="label">Incline Max Grade</span>
                    <span class="val">33° Rock Slag Cleared</span>
                </div>
                <div class="panel-row">
                    <span class="label">Step Obstacle Clearance</span>
                    <span class="val">220 mm Flipper Sub-Tracks</span>
                </div>
                <div class="panel-row">
                    <span class="label">Comm Loss Watchdog</span>
                    <span class="val"><span style="color:{SAFE_GREEN}; font-weight: 700;">100 ms Auto-Cutoff Armed</span></span>
                </div>
                <div class="panel-row">
                    <span class="label">Enclosure Flameproof</span>
                    <span class="val">Ex d I Mb Target (Gap &lt; 0.1mm)</span>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card">
                <div class="panel-row">
                    <span class="label">Two-Way Worker Intercom</span>
                    <span class="val"><span style="color:{SAFE_GREEN}; font-weight: 700;">Active Duplex Intercom</span></span>
                </div>
                <div class="panel-row">
                    <span class="label">Acoustic Audio Mic</span>
                    <span class="val">Active DSP Noise Suppression</span>
                </div>
                <div class="panel-row">
                    <span class="label">Subterranean Speaker</span>
                    <span class="val">Waterproof 95 dB Loudspeaker</span>
                </div>
                <div class="panel-row">
                    <span class="label">Cross-State Teleop</span>
                    <span class="val">Mumbai ↔ Jharkhand 4G/5G MQTT</span>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

# --------------------------------------------------------------------------- #
# Tab 2: 5-Gas Atmospheric Suite & Spontaneous Combustion
# --------------------------------------------------------------------------- #

with tab_gas:
    g_col1, g_col2 = st.columns([7, 5])

    with g_col1:
        st.subheader("Atmospheric Trend Progression (Rolling 60 Samples)")

        if sim_drift and len(st.session_state.telemetry_log) > 0:
            last = st.session_state.telemetry_log[-1].copy()
            last["sample"] = len(st.session_state.telemetry_log)
            last["CH4"] = float(np.clip(last["CH4"] + np.random.normal(0, 0.02), 0, 15))
            last["CO"] = float(np.clip(last["CO"] + np.random.normal(0, 1.2), 0, 300))
            st.session_state.telemetry_log.append(last)

        df_log = pd.DataFrame(st.session_state.telemetry_log)

        # Altair chart for CH4 with DGMS 1.25% threshold line
        ch4_line = (
            alt.Chart(df_log)
            .mark_line(color=ACCENT_SECONDARY, strokeWidth=2.5)
            .encode(
                x=alt.X("sample:Q", title="Sample #"),
                y=alt.Y("CH4:Q", title="CH4 (% vol)"),
                tooltip=["sample", "CH4"],
            )
        )
        ch4_area = (
            alt.Chart(df_log)
            .mark_area(opacity=0.18, color=ACCENT_SECONDARY)
            .encode(
                x=alt.X("sample:Q"),
                y=alt.Y("CH4:Q"),
            )
        )
        rule_dgms = (
            alt.Chart(pd.DataFrame({"y": [1.25]}))
            .mark_rule(color=DANGER_RED, strokeDash=[5, 5], strokeWidth=2)
            .encode(y="y:Q")
        )
        chart_ch4 = (ch4_area + ch4_line + rule_dgms).properties(
            title="CH4 Methane Concentration vs. DGMS 1.25% Safety Limit",
            height=200,
            background="transparent",
        ).configure_axis(
            labelColor=CHART_LABEL,
            titleColor=CHART_TITLE,
            gridColor=CHART_GRID,
            labelFont="JetBrains Mono",
        ).configure_title(color=CHART_TITLE, font="Space Grotesk")

        st.altair_chart(chart_ch4, use_container_width=True)

        # Altair chart for Carbon Monoxide
        co_line = (
            alt.Chart(df_log)
            .mark_line(color=DANGER_RED, strokeWidth=2.5)
            .encode(
                x=alt.X("sample:Q", title="Sample #"),
                y=alt.Y("CO:Q", title="CO (PPM)"),
                tooltip=["sample", "CO"],
            )
        )
        co_area = (
            alt.Chart(df_log)
            .mark_area(opacity=0.18, color=DANGER_RED)
            .encode(
                x=alt.X("sample:Q"),
                y=alt.Y("CO:Q"),
            )
        )
        chart_co = (co_area + co_line).properties(
            title="Carbon Monoxide (CO PPM) - Spontaneous Combustion Indicator",
            height=190,
            background="transparent",
        ).configure_axis(
            labelColor=CHART_LABEL,
            titleColor=CHART_TITLE,
            gridColor=CHART_GRID,
            labelFont="JetBrains Mono",
        ).configure_title(color=CHART_TITLE, font="Space Grotesk")

        st.altair_chart(chart_co, use_container_width=True)

    with g_col2:
        st.subheader("Combustion Ratios & Explosibility")

        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card">
                <div style="font-weight: 700; color: {ACCENT_PRIMARY}; margin-bottom: 0.6rem; font-family: 'Space Grotesk'; font-size: 1.05rem;">
                    Stoichiometric Fire-Risk Indices
                </div>
                <div class="panel-row">
                    <span class="label">Graham's Ratio (CO / ΔO₂)</span>
                    <span class="val">{res.grahams_ratio} <span style="font-weight:400;color:{APP_TEXT_MUTED};">({res.grahams_status.replace('_', ' ')})</span></span>
                </div>
                <div class="panel-row">
                    <span class="label">Young's Ratio (CO₂ / ΔO₂)</span>
                    <span class="val">{res.youngs_ratio if res.youngs_ratio is not None else '—'}</span>
                </div>
                <div class="panel-row">
                    <span class="label">Jones & Trickett Ratio</span>
                    <span class="val">{res.jones_trickett_ratio if res.jones_trickett_ratio is not None else '—'}</span>
                </div>
                <div class="panel-row">
                    <span class="label">Oxides of Carbon (CO/CO₂)</span>
                    <span class="val">{res.co_co2_ratio if res.co_co2_ratio is not None else '—'}</span>
                </div>
                <div class="panel-row">
                    <span class="label">Calculated O₂ Deficit</span>
                    <span class="val">{res.o2_deficiency_pct}%</span>
                </div>
                <div class="panel-row">
                    <span class="label">Nitrogen (N₂ Balance)</span>
                    <span class="val">{res.n2_pct}%</span>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

        coward_kind = "danger" if "EXPLOSIVE MIXTURE" in res.coward_status else (
            "warn" if "POTENTIALLY" in res.coward_status else "safe"
        )

        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card">
                <div style="font-weight: 700; color: {ACCENT_SECONDARY}; margin-bottom: 0.6rem; font-family: 'Space Grotesk'; font-size: 1.05rem;">
                    Coward Flammability Triangle Status
                </div>
                <div class="panel-row">
                    <span class="label">Ternary State</span>
                    <span class="val">{get_badge(res.coward_status, coward_kind)}</span>
                </div>
                <div class="panel-row">
                    <span class="label">DGMS Regulatory Limit</span>
                    <span class="val">1.25% CH₄ Cutoff</span>
                </div>
                <div class="panel-row">
                    <span class="label">Current % of LEL</span>
                    <span class="val">{(ch4_input / 5.0) * 100:.1f}% LEL</span>
                </div>
                <div class="panel-row">
                    <span class="label">Hydrogen Trace (H₂)</span>
                    <span class="val">{h2_input:.1f} PPM</span>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

# --------------------------------------------------------------------------- #
# Tab 3: Sub-Surface FMCW Bio-Radar & Life Detection
# --------------------------------------------------------------------------- #

with tab_radar:
    st.subheader("400 MHz FMCW UWB Sub-Surface Life Detection Radar")
    st.caption("Penetrates up to 10 meters of collapsed rock, timber, and coal rubble to isolate human micro-Doppler chest movements (0.2–0.5 Hz).")

    r_col1, r_col2 = st.columns([8, 4])

    with r_col1:
        st.session_state.radar_tick += 1
        t_vals = np.linspace(0, 10, 120)
        
        if sim_victim:
            wave = 2.4 * np.sin(2 * math.pi * 0.32 * t_vals + (st.session_state.radar_tick * 0.2))
            wave += 0.4 * np.sin(2 * math.pi * 1.2 * t_vals)
            wave += np.random.normal(0, 0.08, size=len(t_vals))
            bpm_est = 19
            target_depth = 4.2
            confidence = 94.6
            subsurface_state = "SURVIVOR DETECTED"
            state_color = SAFE_GREEN
        else:
            wave = np.random.normal(0, 0.15, size=len(t_vals))
            bpm_est = 0
            target_depth = 0.0
            confidence = 4.1
            subsurface_state = "NO LIFE SIGNATURE"
            state_color = APP_TEXT_MUTED

        df_radar = pd.DataFrame({"Time_s": t_vals, "Displacement_mm": wave})

        radar_chart = (
            alt.Chart(df_radar)
            .mark_line(color=ACCENT_PRIMARY, strokeWidth=2.2)
            .encode(
                x=alt.X("Time_s:Q", title="Scan Window (Seconds)"),
                y=alt.Y("Displacement_mm:Q", title="Micro-Doppler Chest Displacement (mm)", scale=alt.Scale(domain=[-3.5, 3.5])),
                tooltip=["Time_s", "Displacement_mm"],
            )
            .properties(
                title=f"Micro-Doppler Respiration Signal — 1D-CNN Isolated Band [0.2 - 0.5 Hz]",
                height=240,
                background="transparent",
            )
            .configure_axis(
                labelColor=CHART_LABEL,
                titleColor=CHART_TITLE,
                gridColor=CHART_GRID,
                labelFont="JetBrains Mono",
            )
            .configure_title(color=CHART_TITLE, font="Space Grotesk")
        )
        st.altair_chart(radar_chart, use_container_width=True)

    with r_col2:
        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card">
                <div style="font-weight: 700; color: {APP_TEXT}; font-size: 1.05rem; margin-bottom: 0.6rem; font-family: 'Space Grotesk';">
                    Bio-Radar Diagnostics
                </div>
                <div class="panel-row">
                    <span class="label">Target Classification</span>
                    <span class="val"><span style="color: {state_color}; font-weight: 700;">{subsurface_state}</span></span>
                </div>
                <div class="panel-row">
                    <span class="label">Estimated Rubble Depth</span>
                    <span class="val">{target_depth:.1f} Meters</span>
                </div>
                <div class="panel-row">
                    <span class="label">Respiration Rate</span>
                    <span class="val">{'~' + str(bpm_est) + ' Breaths/min' if bpm_est > 0 else 'N/A'}</span>
                </div>
                <div class="panel-row">
                    <span class="label">1D-CNN Confidence</span>
                    <span class="val">{confidence:.1f}%</span>
                </div>
                <div class="panel-row">
                    <span class="label">Radar Array Center Freq</span>
                    <span class="val">400 MHz FMCW UWB</span>
                </div>
                <div class="panel-row">
                    <span class="label">Max Rubble Penetration</span>
                    <span class="val">10.0 Meters</span>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

        if sim_victim:
            st.success("▲ LIVE RESCUE ALERT: Trapped miner vital detected. Loudspeaker intercom channel unmuted. Transmit calming audio directives.")

# --------------------------------------------------------------------------- #
# Tab 4: Edge AI Perception & 3D LIO-SAM SLAM
# --------------------------------------------------------------------------- #

with tab_ai:
    st.subheader("NVIDIA Jetson AGX Orin Edge AI & 3D Spatial SLAM")

    ai1, ai2 = st.columns(2)

    with ai1:
        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card">
                <div style="font-weight: 700; color: {ACCENT_PRIMARY}; font-size: 1.1rem; margin-bottom: 0.7rem; font-family: 'Space Grotesk';">
                    NVIDIA AGX Orin Edge Compute Pipeline
                </div>
                <div class="panel-row">
                    <span class="label">Compute Engine</span>
                    <span class="val">NVIDIA Jetson AGX Orin (275 TOPS)</span>
                </div>
                <div class="panel-row">
                    <span class="label">Object Detection Model</span>
                    <span class="val">TensorRT-Accelerated YOLOv10</span>
                </div>
                <div class="panel-row">
                    <span class="label">Inference Frame Latency</span>
                    <span class="val"><span style="color: {SAFE_GREEN}; font-weight: 700;">&lt; 2.8 ms / frame</span></span>
                </div>
                <div class="panel-row">
                    <span class="label">Cloud Dependency</span>
                    <span class="val"><span style="color: {SAFE_GREEN}; font-weight: 700;">0% Local Edge Offline</span></span>
                </div>
                <div class="panel-row">
                    <span class="label">Classes Tracked</span>
                    <span class="val">Human, Miner Helmet, Void, Obstacle</span>
                </div>
                <div class="panel-row">
                    <span class="label">Microcontroller Node</span>
                    <span class="val">ESP32 Dual-Core (100 Hz Loop)</span>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

    with ai2:
        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card">
                <div style="font-weight: 700; color: {INFO_BLUE}; font-size: 1.1rem; margin-bottom: 0.7rem; font-family: 'Space Grotesk';">
                    3D LIO-SAM LiDAR SLAM Telemetry
                </div>
                <div class="panel-row">
                    <span class="label">LiDAR Sensor</span>
                    <span class="val">Ouster OS0-128 (128 Channels)</span>
                </div>
                <div class="panel-row">
                    <span class="label">Laser Field of View</span>
                    <span class="val">360° Horizontal × 90° Vertical</span>
                </div>
                <div class="panel-row">
                    <span class="label">SLAM Algorithm</span>
                    <span class="val">Factor-Graph LIO-SAM</span>
                </div>
                <div class="panel-row">
                    <span class="label">GPS-Denied Positioning</span>
                    <span class="val">Subterranean Inertial Odometry</span>
                </div>
                <div class="panel-row">
                    <span class="label">Point Cloud Rate</span>
                    <span class="val">655,360 points/sec</span>
                </div>
                <div class="panel-row">
                    <span class="label">Loop Closure Confidence</span>
                    <span class="val"><span style="color: {SAFE_GREEN}; font-weight: 700;">99.2% Drift Compensated</span></span>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

# --------------------------------------------------------------------------- #
# Tab 5: Project SETU Ecosystem & Web Platform
# --------------------------------------------------------------------------- #

with tab_eco:
    st.subheader("Project SETU Ecosystem, Web Platform & Field Proving")
    st.caption("Access the official web platform, GitHub repository, video demonstrations, and certification roadmap.")

    eco1, eco2, eco3 = st.columns(3)

    with eco1:
        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card" style="min-height: 180px;">
                <div style="font-weight: 700; color: {APP_TEXT}; font-size: 1.15rem; margin-bottom: 0.5rem; font-family: 'Space Grotesk';">
                    ◫ SETU Web Platform
                </div>
                <div style="color: {APP_TEXT_MUTED}; font-size: 0.88rem; line-height: 1.45;">
                    High-fidelity interactive web application showcasing full technical specifications, 3D rover model visualization, and tactical capability breakdowns.
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )
        st.link_button("Launch Web Platform ↗", "https://setu-mine-rescue-rover.vercel.app/", use_container_width=True)

    with eco2:
        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card" style="min-height: 180px;">
                <div style="font-weight: 700; color: {APP_TEXT}; font-size: 1.15rem; margin-bottom: 0.5rem; font-family: 'Space Grotesk';">
                    ⌥ GitHub Repository
                </div>
                <div style="color: {APP_TEXT_MUTED}; font-size: 0.88rem; line-height: 1.45;">
                    Inspect the open-source codebase, ROS 2 Humble packages, DeepStream DMA video pipelines, and hardware schematics engineered for Project SETU.
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )
        st.link_button("View GitHub Repo ↗", "https://github.com/abarhammalik/SETU-Dashboard", use_container_width=True)

    with eco3:
        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card" style="min-height: 180px;">
                <div style="font-weight: 700; color: {APP_TEXT}; font-size: 1.15rem; margin-bottom: 0.5rem; font-family: 'Space Grotesk';">
                    ▷ 6 Field Video Demos
                </div>
                <div style="color: {APP_TEXT_MUTED}; font-size: 0.88rem; line-height: 1.45;">
                    Watch empirical field evidence proving 4-belt locomotion, 3D SLAM sensor fusion, handheld OCU teleop, multi-terrain traversal, and 50 kg obstacle step climbing.
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )
        st.link_button("Watch 6 Field Demos ↗", "https://setu-mine-rescue-rover.vercel.app/#demonstrations", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    eco4, eco5, eco6 = st.columns(3)

    with eco4:
        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card" style="min-height: 180px;">
                <div style="font-weight: 700; color: {APP_TEXT}; font-size: 1.15rem; margin-bottom: 0.5rem; font-family: 'Space Grotesk';">
                    ⌖ Interactive Schematics
                </div>
                <div style="color: {APP_TEXT_MUTED}; font-size: 0.88rem; line-height: 1.45;">
                    Explore the 12 hardware subsystem callouts covering flameproof seals, BTS7960 motor arrays, FLIR LWIR thermal, Ouster LiDAR, and FMCW bio-radar.
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )
        st.link_button("Open Rover Schematic ↗", "https://setu-mine-rescue-rover.vercel.app/#hardware-labeling", use_container_width=True)

    with eco5:
        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card" style="min-height: 180px;">
                <div style="font-weight: 700; color: {APP_TEXT}; font-size: 1.15rem; margin-bottom: 0.5rem; font-family: 'Space Grotesk';">
                    ⎈ OCU Terminal Simulator
                </div>
                <div style="color: {APP_TEXT_MUTED}; font-size: 0.88rem; line-height: 1.45;">
                    Simulate the dedicated handheld Operator Control Unit (OCU) with dual joysticks, glass-to-glass sub-300ms video HUD, and physical emergency stop toggles.
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )
        st.link_button("Launch OCU Simulator ↗", "https://setu-mine-rescue-rover.vercel.app/#ocu-sim", use_container_width=True)

    with eco6:
        st.markdown(
            textwrap.dedent(f"""
            <div class="panel-card" style="min-height: 180px;">
                <div style="font-weight: 700; color: {APP_TEXT}; font-size: 1.15rem; margin-bottom: 0.5rem; font-family: 'Space Grotesk';">
                    § DGMS & CIMFR Roadmap
                </div>
                <div style="color: {APP_TEXT_MUTED}; font-size: 0.88rem; line-height: 1.45;">
                    Review the certification and compliance pathway for DGMS Technical Circular 02/2021, PESO Ex d I Mb flameproof enclosure standards, and CIMFR testing.
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )
        st.link_button("Review DGMS Roadmap ↗", "https://setu-mine-rescue-rover.vercel.app/#credibility", use_container_width=True)

# --------------------------------------------------------------------------- #
# Footer
# --------------------------------------------------------------------------- #

st.markdown(
    textwrap.dedent(f"""
    <div style="margin-top: 2.5rem; padding-top: 1.2rem; border-top: 1px solid {PANEL_BORDER}; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; color: {APP_TEXT_MUTED}; font-size: 0.84rem; font-family: 'JetBrains Mono', monospace;">
        <div>
            <b>PROJECT SETU (सेतु) GCS Telemetry Dashboard</b> · SIH 2026 Problem Statement ID: SIH26039<br>
            Engineered for Degree III Gassy Coal Mines · DGMS Ex d I Mb Flameproof Compliance Target
        </div>
        <div style="text-align: right; margin-top: 0.4rem;">
            Direct links: <a href="https://setu-mine-rescue-rover.vercel.app/" target="_blank" style="color: {ACCENT_PRIMARY}; text-decoration: none;">Web Platform</a> · 
            <a href="https://github.com/abarhammalik/SETU-Dashboard" target="_blank" style="color: {ACCENT_SECONDARY}; text-decoration: none;">GitHub</a> · 
            Last Sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

if sim_drift:
    import time
    time.sleep(2.0)
    st.rerun()