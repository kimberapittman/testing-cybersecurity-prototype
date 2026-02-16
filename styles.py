"""Custom CSS styling for the cybersecurity decision-support prototype.

Design adapted from the Municipal Cybersecurity Reasoning Prototype:
  - Dark navy theme (#0b0f19 background, #e5e7eb text)
  - Blue accent system (#378AED brand, #55CAFF secondary)
  - Glassy card aesthetic with semi-transparent overlays
  - Inter font family
  - Gradient dividers and glow effects
"""

import streamlit as st


def inject_custom_css():
    st.markdown(
        """
    <style>
    /* === FONT === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, .stApp {
        font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto,
                     Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji" !important;
    }

    /* === TOKENS === */
    :root {
        --brand: #378AED;
        --brand-2: #55CAFF;
        --bg-soft: #0b1020;
        --text-strong: #e5e7eb;
        --text-muted: #94a3b8;
        --card-bg: rgba(255,255,255,0.05);
        --tile-x-pad: 14px;
        --tile-edge-offset: 5px;
    }

    /* === APP BACKGROUND === */
    div[data-testid="stAppViewContainer"] {
        background:
            radial-gradient(1200px 600px at 10% -10%, rgba(76,139,245,0.15), transparent 60%),
            radial-gradient(900px 500px at 100% 0%, rgba(122,168,255,0.10), transparent 60%),
            var(--bg-soft);
    }

    /* === HIDE STREAMLIT CHROME === */
    header[data-testid="stHeader"] { background: transparent; }
    footer, #MainMenu { visibility: hidden; }
    div[data-testid="stMarkdownContainer"] h1 a,
    div[data-testid="stMarkdownContainer"] h2 a,
    div[data-testid="stMarkdownContainer"] h3 a,
    div[data-testid="stMarkdownContainer"] h4 a,
    div[data-testid="stMarkdownContainer"] h5 a,
    div[data-testid="stMarkdownContainer"] h6 a {
        display: none !important;
        visibility: hidden !important;
    }
    button[aria-label*="Copy link"],
    button[title*="Copy link"] {
        display: none !important;
    }

    /* === SIDEBAR === */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
        border-right: 1px solid rgba(255,255,255,0.10);
        backdrop-filter: blur(6px);
    }
    section[data-testid="stSidebar"] .sb-details {
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03)) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 14px !important;
        padding: 0 !important;
        margin: 0.35rem 0 0.75rem 0 !important;
        overflow: visible !important;
    }
    section[data-testid="stSidebar"] .sb-details > summary {
        list-style: none !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03)) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        margin: 0 !important;
        color: var(--text-strong) !important;
        font-weight: 800 !important;
        cursor: pointer !important;
        transition: background-color 0.12s ease, border-color 0.12s ease,
                    box-shadow 0.12s ease, filter 0.12s ease, transform 0.12s ease;
    }
    section[data-testid="stSidebar"] .sb-details > summary:hover {
        background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.05)) !important;
        border-color: rgba(255,255,255,0.24) !important;
        box-shadow: 0 0 0 1px rgba(255,255,255,0.18), 0 0 12px rgba(255,255,255,0.18),
                    0 0 24px rgba(255,255,255,0.08), 0 16px 26px rgba(255,255,255,0.12);
        filter: brightness(1.04) !important;
        transform: translateY(-2px);
    }
    section[data-testid="stSidebar"] .sb-details[open] > summary {
        border-bottom-left-radius: 0 !important;
        border-bottom-right-radius: 0 !important;
    }
    section[data-testid="stSidebar"] .sb-details > summary::-webkit-details-marker { display: none !important; }
    section[data-testid="stSidebar"] .sb-details > summary::marker { content: "" !important; }
    section[data-testid="stSidebar"] .sb-details > summary::before {
        content: ">";
        font-size: 1rem;
        font-weight: 800;
        line-height: 1;
        opacity: 0.8;
        margin-top: -1px;
        transition: transform 0.12s ease, opacity 0.12s ease;
    }
    section[data-testid="stSidebar"] .sb-details[open] > summary::before {
        transform: rotate(90deg);
    }
    section[data-testid="stSidebar"] .sb-details-body {
        padding: 12px 12px !important;
        padding-left: 6px !important;
        background: rgba(255,255,255,0.03) !important;
    }
    section[data-testid="stSidebar"] details.sb-details[open] > .sb-details-body {
        margin-top: 0.6rem !important;
        padding-bottom: 0.2rem !important;
    }
    section[data-testid="stSidebar"] .sb-details-body .sb-section {
        font-weight: 800 !important;
        padding: 0 !important;
        line-height: 1.2;
        color: #ffffff !important;
        text-decoration: underline !important;
        text-decoration-color: rgba(255,255,255,0.85) !important;
        text-decoration-thickness: 2px !important;
        text-underline-offset: 4px !important;
        margin: 0 !important;
        margin-top: 0.75rem !important;
    }
    section[data-testid="stSidebar"] .sb-section-body {
        margin-left: 1rem;
        margin-top: 0.5rem;
    }
    section[data-testid="stSidebar"] .sb-p {
        margin: 0 0 0.4rem 0 !important;
    }
    section[data-testid="stSidebar"] .sb-details-body a,
    section[data-testid="stSidebar"] .sb-details-body p,
    section[data-testid="stSidebar"] .sb-details-body li,
    section[data-testid="stSidebar"] .sb-details-body span {
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        white-space: normal !important;
    }

    /* === BUTTONS (from reference repo) === */
    div[data-testid="stButton"] > button {
        box-sizing: border-box !important;
        padding: 0.7rem 1rem !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        background: rgba(255,255,255,0.06) !important;
        color: var(--text-strong) !important;
        border: 1px solid rgba(76,139,245,0.55) !important;
        box-shadow: 0 0 0 1px rgba(76,139,245,0.35),
                    0 10px 20px rgba(76,139,245,0.35) !important;
        transition: transform .06s ease, box-shadow .15s ease, filter .15s ease !important;
        font-weight: 600 !important;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-3px) !important;
        cursor: pointer !important;
        box-shadow: 0 0 0 3px rgba(76,139,245,0.65),
                    0 18px 38px rgba(76,139,245,0.45) !important;
        border-color: rgba(76,139,245,0.95) !important;
        filter: brightness(1.05) !important;
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(-1px) !important;
        box-shadow: 0 0 0 1px rgba(76,139,245,0.45),
                    0 8px 16px rgba(76,139,245,0.30) !important;
    }
    div[data-testid="stButton"] > button:disabled {
        opacity: 0.55 !important;
        background: rgba(255,255,255,0.10) !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
        color: var(--text-strong) !important;
        box-shadow: none !important;
        transform: none !important;
        filter: none !important;
    }
    div[data-testid="stButton"] > button:disabled:hover {
        transform: none !important;
        cursor: default !important;
        box-shadow: none !important;
        border-color: rgba(255,255,255,0.22) !important;
        filter: none !important;
    }
    div[data-testid="stButton"] > button:focus-visible {
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(76,139,245,0.75),
                    0 0 0 6px rgba(76,139,245,0.25) !important;
    }

    /* === INPUTS === */
    input, textarea, select, .stTextInput input, .stTextArea textarea {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: var(--text-strong) !important;
        border-radius: 10px !important;
    }
    textarea::placeholder {
        color: rgba(229,231,235,0.55);
        font-size: 0.95rem;
    }
    label, .stRadio, .stSelectbox, .stMultiSelect, .stExpander {
        color: var(--text-strong) !important;
    }

    /* === PROGRESS BAR — GLASSY STAGE INDICATORS === */
    .stage-indicator {
        text-align: center;
        padding: 12px 8px;
        border-radius: 12px;
        transition: all 0.15s ease;
        cursor: default;
        margin-bottom: 4px;
        border: 1px solid rgba(255,255,255,0.10);
    }
    .stage-indicator:hover {
        transform: translateY(-2px);
        filter: brightness(1.05);
    }
    .stage-number {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .stage-label {
        font-size: 0.75rem;
        font-weight: 500;
    }
    .stage-current {
        background: linear-gradient(180deg, rgba(76,139,245,0.35), rgba(76,139,245,0.15));
        color: var(--text-strong);
        border-color: rgba(76,139,245,0.55);
        box-shadow: 0 0 0 1px rgba(76,139,245,0.35), 0 8px 20px rgba(76,139,245,0.30);
    }
    .stage-completed {
        background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
        color: var(--text-strong);
        border-color: rgba(76,139,245,0.35);
        cursor: pointer;
    }
    .stage-completed:hover {
        border-color: rgba(76,139,245,0.65);
        box-shadow: 0 0 0 1px rgba(76,139,245,0.45), 0 10px 24px rgba(76,139,245,0.25);
    }
    .stage-locked {
        background: rgba(255,255,255,0.03);
        color: var(--text-muted);
        border-color: rgba(255,255,255,0.06);
        opacity: 0.5;
    }

    /* === SELECTABLE DOMAIN CARDS (Stage 4 Tier 1) — GLASSY === */
    .domain-card {
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.15s ease;
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
    }
    .domain-card:hover {
        border-color: rgba(76,139,245,0.55);
        background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.05));
        box-shadow: 0 0 0 1px rgba(76,139,245,0.35), 0 8px 18px rgba(76,139,245,0.15);
        transform: translateY(-1px);
    }
    .domain-card-selected {
        border: 1px solid rgba(76,139,245,0.65);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.15s ease;
        background: linear-gradient(180deg, rgba(76,139,245,0.20), rgba(76,139,245,0.08));
        box-shadow: 0 0 0 1px rgba(76,139,245,0.45), 0 8px 18px rgba(76,139,245,0.20);
    }
    .domain-card-selected:hover {
        border-color: rgba(76,139,245,0.85);
        filter: brightness(1.05);
    }
    .domain-card-title {
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 4px;
        color: var(--text-strong);
    }
    .domain-card-desc {
        font-size: 0.85rem;
        color: var(--text-muted);
    }
    .checkmark {
        float: right;
        font-size: 1.2rem;
        color: #60a5fa;
    }

    /* === RELATIONSHIP COLOR CODING (Stage 5) — DARK THEME === */
    .rel-alignment {
        background-color: rgba(16,185,129,0.12);
        border-left: 4px solid #10b981;
        padding: 8px 12px;
        border-radius: 4px;
        margin: 4px 0;
        color: var(--text-strong);
    }
    .rel-tension {
        background-color: rgba(245,158,11,0.12);
        border-left: 4px solid #f59e0b;
        padding: 8px 12px;
        border-radius: 4px;
        margin: 4px 0;
        color: var(--text-strong);
    }
    .rel-conflict {
        background-color: rgba(239,68,68,0.12);
        border-left: 4px solid #ef4444;
        padding: 8px 12px;
        border-radius: 4px;
        margin: 4px 0;
        color: var(--text-strong);
    }
    .rel-independence {
        background-color: rgba(255,255,255,0.05);
        border-left: 4px solid rgba(255,255,255,0.25);
        padding: 8px 12px;
        border-radius: 4px;
        margin: 4px 0;
        color: var(--text-strong);
    }
    .rel-na {
        background-color: rgba(255,255,255,0.03);
        border-left: 4px solid rgba(255,255,255,0.12);
        padding: 8px 12px;
        border-radius: 4px;
        margin: 4px 0;
        color: var(--text-muted);
    }

    /* === SECTION HEADERS — DIFFERENT BLUE SHADES === */
    /* Technical (NIST CSF): deeper blue */
    .section-header-tech {
        background: linear-gradient(90deg, rgba(30,64,175,0.6), rgba(59,130,246,0.3));
        color: var(--text-strong);
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin: 16px 0 8px 0;
        border: 1px solid rgba(59,130,246,0.25);
    }
    /* Ethical (PFCE): lighter cyan-blue */
    .section-header-eth {
        background: linear-gradient(90deg, rgba(85,202,255,0.25), rgba(96,165,250,0.12));
        color: var(--text-strong);
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin: 16px 0 8px 0;
        border: 1px solid rgba(85,202,255,0.25);
    }

    /* === STAGE PURPOSE BOX — DARK THEME === */
    .stage-purpose {
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
        border: 1px solid rgba(76,139,245,0.25);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 0.9rem;
        color: var(--text-strong);
    }

    /* === EXPANDER STYLING === */
    .streamlit-expanderHeader {
        font-weight: 600;
        border-radius: 12px;
    }

    /* === RESPONSE PATTERN CARDS (Stage 4 Tier 2) — DARK THEME === */
    .response-pattern {
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 6px;
        cursor: pointer;
        transition: all 0.15s ease;
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
        font-size: 0.88rem;
    }
    .response-pattern:hover {
        border-color: rgba(76,139,245,0.55);
        background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.05));
        box-shadow: 0 0 0 1px rgba(76,139,245,0.25);
        transform: translateY(-1px);
    }
    .response-pattern-selected {
        border: 1px solid rgba(76,139,245,0.65);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 6px;
        cursor: pointer;
        transition: all 0.15s ease;
        background: linear-gradient(180deg, rgba(76,139,245,0.18), rgba(76,139,245,0.08));
        box-shadow: 0 0 0 1px rgba(76,139,245,0.35);
        font-size: 0.88rem;
    }
    .response-pattern-selected:hover {
        border-color: rgba(76,139,245,0.85);
        filter: brightness(1.05);
    }
    .rp-checkmark {
        float: left;
        margin-right: 8px;
        color: #60a5fa;
        font-weight: 700;
    }
    .rp-label {
        color: var(--text-strong);
    }
    .other-pattern {
        border: 1px dashed rgba(255,255,255,0.15);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 6px;
        transition: all 0.15s ease;
        background: rgba(255,255,255,0.03);
        font-size: 0.88rem;
    }
    .other-pattern:hover {
        border-color: rgba(76,139,245,0.45);
        background: rgba(255,255,255,0.06);
    }

    /* === PDF EXPORT === */
    .pdf-download {
        text-align: center;
        margin: 24px 0;
    }

    /* === GRADIENT DIVIDER === */
    .gradient-divider {
        margin: 14px 0 20px 0;
        border: none;
        height: 2px;
        background: linear-gradient(
            90deg,
            rgba(76,139,245,0.15),
            rgba(76,139,245,0.55),
            rgba(76,139,245,0.15)
        );
    }

    /* === RESPONSIVE === */
    @media (max-width: 520px) {
        div[data-testid="stButton"] > button {
            white-space: normal !important;
            text-align: center !important;
            line-height: 1.2 !important;
            padding: 0.7rem 1rem !important;
        }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
