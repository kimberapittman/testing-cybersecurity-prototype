"""Custom CSS styling for the cybersecurity decision-support prototype."""

import streamlit as st


def inject_custom_css():
    st.markdown(
        """
    <style>
    /* ── Progress Bar Stage Indicators ── */
    .stage-indicator {
        text-align: center;
        padding: 12px 8px;
        border-radius: 10px;
        transition: all 0.2s ease;
        cursor: default;
        margin-bottom: 4px;
    }
    .stage-indicator:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
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
        background: linear-gradient(135deg, #1a73e8, #4285f4);
        color: white;
        box-shadow: 0 3px 10px rgba(26,115,232,0.4);
    }
    .stage-completed {
        background: linear-gradient(135deg, #0d9488, #14b8a6);
        color: white;
        cursor: pointer;
    }
    .stage-locked {
        background: #e5e7eb;
        color: #9ca3af;
    }

    /* ── Selectable Cards (Stage 4 Tier 1) ── */
    .domain-card {
        border: 2px solid #d1d5db;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        background: white;
    }
    .domain-card:hover {
        border-color: #60a5fa;
        background: #eff6ff;
        box-shadow: 0 2px 8px rgba(96,165,250,0.2);
    }
    .domain-card-selected {
        border: 2px solid #2563eb;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        background: #dbeafe;
        box-shadow: 0 2px 8px rgba(37,99,235,0.2);
    }
    .domain-card-selected:hover {
        border-color: #1d4ed8;
        background: #bfdbfe;
    }
    .domain-card-title {
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }
    .domain-card-desc {
        font-size: 0.85rem;
        color: #4b5563;
    }
    .checkmark {
        float: right;
        font-size: 1.2rem;
        color: #2563eb;
    }

    /* ── Relationship Color Coding (Stage 5) ── */
    .rel-alignment {
        background-color: #d1fae5;
        border-left: 4px solid #059669;
        padding: 8px 12px;
        border-radius: 4px;
        margin: 4px 0;
    }
    .rel-tension {
        background-color: #fef3c7;
        border-left: 4px solid #d97706;
        padding: 8px 12px;
        border-radius: 4px;
        margin: 4px 0;
    }
    .rel-conflict {
        background-color: #fee2e2;
        border-left: 4px solid #dc2626;
        padding: 8px 12px;
        border-radius: 4px;
        margin: 4px 0;
    }
    .rel-independence {
        background-color: #f3f4f6;
        border-left: 4px solid #6b7280;
        padding: 8px 12px;
        border-radius: 4px;
        margin: 4px 0;
    }
    .rel-na {
        background-color: #f9fafb;
        border-left: 4px solid #d1d5db;
        padding: 8px 12px;
        border-radius: 4px;
        margin: 4px 0;
    }

    /* ── Section Headers ── */
    .section-header-tech {
        background: linear-gradient(90deg, #1e40af, #3b82f6);
        color: white;
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin: 16px 0 8px 0;
    }
    .section-header-eth {
        background: linear-gradient(90deg, #7c3aed, #a78bfa);
        color: white;
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin: 16px 0 8px 0;
    }

    /* ── Buttons ── */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
        border: 2px solid transparent;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* ── Text Areas ── */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #d1d5db;
        transition: border-color 0.2s ease;
    }
    .stTextArea textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        border-radius: 8px;
    }

    /* ── Stage Purpose Box ── */
    .stage-purpose {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 0.9rem;
        color: #0c4a6e;
    }

    /* ── Expander styling ── */
    .streamlit-expanderHeader {
        font-weight: 600;
        border-radius: 8px;
    }

    /* ── Response Pattern Cards (Stage 4 Tier 2) ── */
    .response-pattern {
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        background: #fafafa;
        font-size: 0.88rem;
    }
    .response-pattern:hover {
        border-color: #93c5fd;
        background: #eff6ff;
        box-shadow: 0 1px 4px rgba(96,165,250,0.15);
    }
    .response-pattern-selected {
        border: 2px solid #2563eb;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        background: #dbeafe;
        box-shadow: 0 1px 4px rgba(37,99,235,0.15);
        font-size: 0.88rem;
    }
    .response-pattern-selected:hover {
        border-color: #1d4ed8;
        background: #bfdbfe;
    }
    .rp-checkmark {
        float: left;
        margin-right: 8px;
        color: #2563eb;
        font-weight: 700;
    }
    .rp-label {
        color: #1f2937;
    }
    .other-pattern {
        border: 2px dashed #d1d5db;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 6px;
        transition: all 0.2s ease;
        background: #f9fafb;
        font-size: 0.88rem;
    }
    .other-pattern:hover {
        border-color: #93c5fd;
        background: #eff6ff;
    }

    /* ── PDF export button ── */
    .pdf-download {
        text-align: center;
        margin: 24px 0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
