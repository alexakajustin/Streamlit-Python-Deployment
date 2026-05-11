import streamlit as st
import pandas as pd

def apply_theme():
    """Apply Cyberpunk-themed CSS styling."""
    st.set_page_config(page_title="CDPR – Analiza Financiara | Pachete Software", layout="wide", page_icon="🎮")
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
    .main { background: linear-gradient(135deg, #0a0a0f 0%, #12121f 50%, #0a0a0f 100%); color: #e0e0e0; }
    h1 { color: #f3e600 !important; font-family: 'Orbitron', monospace !important; font-size: 2rem !important;
         text-shadow: 0 0 20px rgba(243,230,0,0.3); letter-spacing: 2px; border-bottom: 2px solid #f3e600; padding-bottom: 10px; }
    h2 { color: #00e5ff !important; font-family: 'Orbitron', monospace !important; font-size: 1.3rem !important; margin-top: 1.5rem; }
    h3 { color: #ff6ec7 !important; font-family: 'Inter', sans-serif !important; font-size: 1.1rem !important; }
    .stMarkdown p, .stMarkdown li { font-family: 'Inter', sans-serif; line-height: 1.7; color: #c8c8d0; font-size: 0.95rem; }
    .stMetric { background: linear-gradient(135deg, #1a1a2e, #16213e); border: 1px solid #f3e60066;
                padding: 15px; border-radius: 10px; box-shadow: 0 0 15px rgba(243,230,0,0.1); }
    [data-testid="stMetricValue"] { color: #f3e600 !important; font-family: 'Orbitron', monospace !important; }
    [data-testid="stMetricLabel"] { color: #00e5ff !important; }
    .stButton>button { background: linear-gradient(90deg, #f3e600, #ffb800); color: #0a0a0f;
                       border: none; font-weight: 700; border-radius: 8px; transition: all 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(243,230,0,0.4); }
    .stTabs [data-baseweb="tab"] { color: #00e5ff; font-family: 'Inter', sans-serif; }
    .stTabs [aria-selected="true"] { background: linear-gradient(90deg, #f3e600, #ffb800); color: #0a0a0f !important; border-radius: 8px 8px 0 0; }
    .stSidebar { background: linear-gradient(180deg, #0d0d1a, #1a1a2e) !important; }
    .stSidebar .stRadio label { color: #c8c8d0 !important; font-family: 'Inter', sans-serif; }
    div[data-testid="stExpander"] { background: #1a1a2e; border: 1px solid #00e5ff33; border-radius: 10px; }
    div[data-testid="stExpander"] summary { color: #00e5ff !important; font-weight: 600; }
    .info-box { background: linear-gradient(135deg, #1a1a2e, #0d1b2a); border-left: 4px solid #00e5ff;
                padding: 15px 20px; border-radius: 0 8px 8px 0; margin: 10px 0; }
    .formula-box { background: #12121f; border: 1px solid #f3e60044; padding: 15px 20px;
                   border-radius: 8px; font-family: 'Courier New', monospace; color: #f3e600; margin: 10px 0; }
    .interpret-box { background: linear-gradient(135deg, #1a0a2e, #2a1a3e); border-left: 4px solid #ff6ec7;
                     padding: 15px 20px; border-radius: 0 8px 8px 0; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    import os
    # Cale relativă la folderul Data_Source
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, "..", "Data_Source", "cdpr_cleaned.csv")
    df = pd.read_csv(data_path)
    return df

def section_header(icon, title, subtitle):
    st.markdown(f"# {icon} {title}")
    st.markdown(f"*{subtitle}*")
    st.markdown("---")

def problem_box(text):
    st.markdown(f'<div class="info-box">📋 <b>Definirea Problemei:</b><br>{text}</div>', unsafe_allow_html=True)

def method_box(text):
    st.markdown(f'<div class="formula-box">🔬 <b>Metodologie:</b><br>{text}</div>', unsafe_allow_html=True)

def interpret_box(text):
    st.markdown(f'<div class="interpret-box">💡 <b>Interpretare Economică:</b><br>{text}</div>', unsafe_allow_html=True)

def info_box(text):
    st.markdown(f'<div class="info-box">📊 <b>Informații necesare:</b><br>{text}</div>', unsafe_allow_html=True)
