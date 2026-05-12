"""Stage 5: Integration — display-only integration of elicited considerations."""

import streamlit as st
from domain_data import NIST_DOMAINS, PFCE_DOMAINS

PFCE_DISPLAY_ORDER = ["BENEFICENCE", "NON-MALEFICENCE", "AUTONOMY", "JUSTICE", "EXPLICABILITY"]
NIST_DISPLAY_ORDER = ["GOVERN", "IDENTIFY", "PROTECT", "DETECT", "RESPOND", "RECOVER"]


def _get_actions():
    return [
        (i, action)
        for i, action in enumerate(st.session_state.actions)
        if action.strip()
    ]


def _get_consideration_text(action_idx, domain_key):
    """Get the stored consideration text for an action+domain pair.

    Returns None if the domain was marked N/A or has no content.
    """
    action_key = str(action_idx)

    responses = st.session_state.tier2_responses.get(action_key, {}).get(
        domain_key, {}
    )
    data = responses.get("0", {})

    if isinstance(data, str):
        if not data.strip() or data.strip() == "N/A":
            return None
        patterns = [p.strip() for p in data.split("|") if p.strip()]
        return "\n".join(f"- {p}" for p in patterns)

    if data.get("na", False):
        return None

    text = data.get("text", "").strip()
    patterns = data.get("patterns", [])

    if not text and not patterns:
        return None

    parts = []
    if text:
        parts.append(text)
    if patterns:
        for p in patterns:
            parts.append(f"- {p}")

    return "\n".join(parts)


def _render_action_review(action_idx, action_text):
    """Render the consideration review for one action."""
    st.subheader(f"Action {action_idx + 1}: {action_text}")

    col_eth, col_tech = st.columns(2)

    with col_eth:
        st.markdown(
            '<div class="section-header-eth">'
            "Ethical Considerations (PFCE)</div>",
            unsafe_allow_html=True,
        )
        has_pfce = False
        for domain_key in PFCE_DISPLAY_ORDER:
            if domain_key not in st.session_state.selected_pfce_domains:
                continue
            text = _get_consideration_text(action_idx, domain_key)
            if text is None:
                continue
            has_pfce = True
            st.markdown(f"**{domain_key}**")
            st.markdown(text)

        if not has_pfce:
            st.markdown(
                "No ethical considerations were identified for this action."
            )

    with col_tech:
        st.markdown(
            '<div class="section-header-tech">'
            "Technical Considerations (NIST CSF 2.0)</div>",
            unsafe_allow_html=True,
        )
        has_nist = False
        for domain_key in NIST_DISPLAY_ORDER:
            if domain_key not in st.session_state.selected_nist_domains:
                continue
            text = _get_consideration_text(action_idx, domain_key)
            if text is None:
                continue
            has_nist = True
            st.markdown(f"**{domain_key}**")
            st.markdown(text)

        if not has_nist:
            st.markdown(
                "No technical considerations were identified for this action."
            )


def render_stage5():
    """Display-only integration of elicited considerations."""
    st.header("Stage 5: Integration")
    st.markdown(
        "This stage presents the full landscape of ethical and technical "
        "considerations you elicited, organized by action. This is the "
        "integration moment — see the considerations together before "
        "documenting your reasoning."
    )

    actions = _get_actions()

    if not actions:
        st.warning("No actions declared. Return to Stage 3.")
        return

    for i, (action_idx, action_text) in enumerate(actions):
        if i > 0:
            st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
        _render_action_review(action_idx, action_text)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    if st.button(
        "Proceed to Documentation →",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.current_stage = 6
        st.session_state.max_unlocked_stage = max(
            st.session_state.max_unlocked_stage, 6
        )
        st.rerun()
