"""Stage 5: Consolidated Visibility — read-only review of elicited considerations."""

import streamlit as st
from domain_data import NIST_DOMAINS, PFCE_DOMAINS


def _get_actions():
    """Return list of non-empty actions with their indices."""
    return [
        (i, action)
        for i, action in enumerate(st.session_state.actions)
        if action.strip()
    ]


def _get_response_text(action_idx, domain_key, domain_type):
    """Get selected patterns for an action+domain pair, formatted as a list."""
    action_key = str(action_idx)

    same_as = st.session_state.tier2_same_as.get(action_key, {}).get(domain_key)
    if same_as is not None:
        action_key = str(same_as)

    responses = st.session_state.tier2_responses.get(action_key, {}).get(
        domain_key, {}
    )

    composite = responses.get("0", "").strip()

    if composite == "N/A":
        return "N/A"
    elif composite:
        patterns = [p.strip() for p in composite.split("|") if p.strip()]
        return "\n".join(f"- {p}" for p in patterns)
    else:
        return "*No considerations selected.*"


def _render_action_profile(action_idx, action_text):
    """Render the consolidated consideration profile for one action."""
    st.markdown(f"### Action {action_idx + 1}")
    st.markdown(f"> {action_text}")

    col_tech, col_eth = st.columns(2)

    with col_tech:
        st.markdown(
            '<div class="section-header-tech">'
            "Technical Considerations (NIST CSF)</div>",
            unsafe_allow_html=True,
        )
        for domain_key in st.session_state.selected_nist_domains:
            st.markdown(f"**{domain_key}**")
            st.markdown(_get_response_text(action_idx, domain_key, "nist"))

        if not st.session_state.selected_nist_domains:
            st.markdown("*No technical domains activated.*")

    with col_eth:
        st.markdown(
            '<div class="section-header-eth">'
            "Ethical Considerations (PFCE)</div>",
            unsafe_allow_html=True,
        )
        for domain_key in st.session_state.selected_pfce_domains:
            st.markdown(f"**{domain_key}**")
            st.markdown(_get_response_text(action_idx, domain_key, "pfce"))

        if not st.session_state.selected_pfce_domains:
            st.markdown("*No ethical domains activated.*")


def _render_cross_action_comparison(actions):
    """Side-by-side comparison of all actions across every activated domain."""
    st.markdown("## Cross-Action Comparison")
    st.markdown(
        "Side-by-side view showing how each action produces different "
        "considerations within the same domain."
    )

    # Technical domains
    if st.session_state.selected_nist_domains:
        st.markdown(
            '<div class="section-header-tech">'
            "Technical Considerations (NIST CSF)</div>",
            unsafe_allow_html=True,
        )
        for domain_key in st.session_state.selected_nist_domains:
            st.markdown(f"**{domain_key}**")
            cols = st.columns(len(actions))
            for col, (action_idx, action_text) in zip(cols, actions):
                with col:
                    st.markdown(f"*Action {action_idx + 1}*")
                    st.markdown(
                        _get_response_text(action_idx, domain_key, "nist")
                    )

    # Ethical domains
    if st.session_state.selected_pfce_domains:
        st.markdown(
            '<div class="section-header-eth">'
            "Ethical Considerations (PFCE)</div>",
            unsafe_allow_html=True,
        )
        for domain_key in st.session_state.selected_pfce_domains:
            st.markdown(f"**{domain_key}**")
            cols = st.columns(len(actions))
            for col, (action_idx, action_text) in zip(cols, actions):
                with col:
                    st.markdown(f"*Action {action_idx + 1}*")
                    st.markdown(
                        _get_response_text(action_idx, domain_key, "pfce")
                    )


def render_stage5():
    """Consolidated visibility stage — read-only review."""
    st.header("Stage 5: Consolidated Visibility")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Review the complete consideration profile "
        "for each action and compare across actions. This stage is read-only "
        "— return to Stage 4 to modify considerations."
        "</div>",
        unsafe_allow_html=True,
    )

    actions = _get_actions()

    if not actions:
        st.warning("No actions declared. Return to Stage 3.")
        return

    # Part 1: Per-Action Consolidated Views
    st.markdown("## Per-Action Consideration Profiles")
    for action_idx, action_text in actions:
        _render_action_profile(action_idx, action_text)
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # Part 2: Cross-Action Comparison
    if len(actions) >= 2:
        _render_cross_action_comparison(actions)
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    if st.button(
        "Proceed to Stage 6: Documentation →",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.current_stage = 6
        st.session_state.max_unlocked_stage = max(
            st.session_state.max_unlocked_stage, 6
        )
        st.rerun()
