import streamlit as st

def apply_custom_ui():
    st.set_page_config(
        page_title="Vision-Mart AI",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif !important; }

    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding: 2rem 2rem 2rem 2rem;
        max-width: 1100px;
    }

    /* Header */
    .header-card {
        background: linear-gradient(135deg, #161b22, #1c2333);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 20px;
        text-align: center;
    }
    .header-card h1 {
        font-size: 1.8rem;
        font-weight: 700;
        color: #a5d6ff;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }
    .header-card p {
        font-size: 0.72rem;
        color: #8b949e;
        margin: 0;
        font-weight: 400;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* Stat Cards */
    .stat-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: center;
    }
    .stat-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #a5d6ff;
        margin-bottom: 4px;
    }
    .stat-label {
        font-size: 0.7rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 500;
    }

    /* Section Cards */
    .section-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .section-title {
        font-size: 0.7rem;
        font-weight: 600;
        color: #8b949e;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 16px;
        padding-bottom: 10px;
        border-bottom: 1px solid #21262d;
    }

    /* Result Card */
    .result-card {
        background: #0d1117;
        border: 1px solid #a5d6ff;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin-top: 12px;
    }
    .result-label {
        font-size: 0.7rem;
        font-weight: 500;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .result-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #a5d6ff;
        margin-bottom: 6px;
    }
    .result-confidence {
        font-size: 0.78rem;
        color: #3fb950;
        font-weight: 500;
        margin-bottom: 10px;
    }
    .result-price {
        font-size: 1.2rem;
        font-weight: 700;
        color: #e6edf3;
        background: #21262d;
        display: inline-block;
        padding: 6px 20px;
        border-radius: 8px;
        margin-top: 6px;
    }

    /* Probability Bars */
    .prob-title {
        font-size: 0.7rem;
        font-weight: 600;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 20px 0 12px 0;
    }
    .prob-row {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        gap: 10px;
    }
    .prob-label {
        font-size: 0.75rem;
        color: #c9d1d9;
        width: 120px;
        flex-shrink: 0;
    }
    .prob-bar-bg {
        flex: 1;
        background: #21262d;
        border-radius: 4px;
        height: 6px;
        overflow: hidden;
    }
    .prob-bar-fill {
        height: 100%;
        border-radius: 4px;
        background: #30363d;
    }
    .prob-bar-fill.top { background: #3fb950; }
    .prob-percent {
        font-size: 0.72rem;
        color: #8b949e;
        width: 36px;
        text-align: right;
        flex-shrink: 0;
    }

    /* History Table */
    .history-header {
        display: flex;
        padding: 8px 12px;
        font-size: 0.68rem;
        font-weight: 600;
        color: #484f58;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        border-bottom: 1px solid #21262d;
        margin-bottom: 4px;
    }
    .history-row {
        display: flex;
        padding: 10px 12px;
        font-size: 0.78rem;
        border-bottom: 1px solid #161b22;
        border-radius: 6px;
    }
    .history-row:hover { background: #1c2333; }

    /* Message Boxes */
    .warn-box {
        background: #1c1f26;
        border: 1px solid #d29922;
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 0.78rem;
        color: #d29922;
        margin-top: 12px;
    }
    .info-box {
        background: #1c1f26;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 0.78rem;
        color: #8b949e;
        margin-top: 12px;
        text-align: center;
    }
    .error-box {
        background: #1c1f26;
        border: 1px solid #f85149;
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 0.78rem;
        color: #f85149;
        margin-top: 12px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #0d1117;
        border-bottom: 1px solid #21262d;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #8b949e;
        font-size: 0.75rem;
        font-weight: 500;
        padding: 8px 20px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        color: #a5d6ff !important;
        border-bottom: 2px solid #a5d6ff !important;
        background: transparent !important;
    }

    /* Camera */
    .stCameraInput > div {
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .stCameraInput button {
        background: #21262d !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        padding: 8px 20px !important;
        margin-top: 8px !important;
    }
    .stCameraInput button:hover {
        border-color: #a5d6ff !important;
        color: #a5d6ff !important;
    }

    /* File Uploader */
    .stFileUploader section {
        background: #161b22 !important;
        border: 1px dashed #a5d6ff !important;
        border-radius: 10px !important;
    }
    .stFileUploader section > div {
        background: #161b22 !important;
        color: #c9d1d9 !important;
    }
    .stFileUploader section span {
        color: #8b949e !important;
        font-size: 0.75rem !important;
    }
    .stFileUploader section small {
        color: #484f58 !important;
        font-size: 0.7rem !important;
    }
    .stFileUploader button {
        background: #21262d !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        font-size: 0.75rem !important;
    }

    /* Buttons */
    .stButton > button {
        background: #21262d !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        padding: 6px 16px !important;
    }
    .stButton > button:hover {
        border-color: #a5d6ff !important;
        color: #a5d6ff !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        color: #c9d1d9 !important;
        font-size: 0.78rem !important;
    }

    /* Number Input */
    .stNumberInput > div > div > input {
        background: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        color: #c9d1d9 !important;
        font-size: 0.78rem !important;
    }

    /* Text Input */
    .stTextInput > div > div > input {
        background: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        color: #c9d1d9 !important;
        font-size: 0.78rem !important;
    }

    /* Input Labels */
    .stTextInput label,
    .stSelectbox label,
    .stNumberInput label {
        color: #8b949e !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.3px !important;
    }

    /* Password eye icon */
    .stTextInput button {
        background: #21262d !important;
        border: none !important;
        color: #8b949e !important;
    }
                
                
    /* Success */
    .stSuccess {
        background: #1c2a1c !important;
        border: 1px solid #3fb950 !important;
        border-radius: 8px !important;
        font-size: 0.78rem !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 36px;
        padding-top: 16px;
        border-top: 1px solid #21262d;
        font-size: 0.7rem;
        color: #484f58;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #a5d6ff; }

    </style>
    """, unsafe_allow_html=True)
