"""Stage 5: Interaction Examination (Automated Structuring)."""

import streamlit as st
from domain_data import (
    NIST_DOMAINS,
    PFCE_DOMAINS,
    RELATIONSHIP_TYPES,
    RELATIONSHIP_COLORS,
    RELATIONSHIP_DESCRIPTIONS,
)


def _get_actions():
    """Return list of non-empty actions with their indices."""
    return [
        (i, action)
        for i, action in enumerate(st.session_state.actions)
        if action.strip()
    ]


def _get_response_text(action_idx, domain_key, domain_type):
    """Get the consideration text for an action+domain pair.

    Returns selected pattern labels as formatted list.
    Falls back to Tier 1 prompt if no Tier 2 selections were made.
    """
    action_key = str(action_idx)

    # Check "same as" first
    same_as = st.session_state.tier2_same_as.get(action_key, {}).get(domain_key)
    if same_as is not None:
        action_key = str(same_as)

    if domain_type == "nist":
        domain_defs = NIST_DOMAINS
    else:
        domain_defs = PFCE_DOMAINS

    responses = st.session_state.tier2_responses.get(action_key, {}).get(
        domain_key, {}
    )

    # Under new structure, all patterns stored under key "0"
    composite = responses.get("0", "").strip()

    if composite == "N/A":
        return "N/A"
    elif composite:
        # Split pipe-separated patterns and format as list
        patterns = [p.strip() for p in composite.split("|") if p.strip()]
        lines = [f"- {p}" for p in patterns]
        return "\n".join(lines)
    else:
        # Fallback: show the Tier 1 prompt as context
        return (
            f"*Domain activated but no specific considerations selected.*\n\n"
            f"*Tier 1:* {domain_defs[domain_key]['prompt']}"
        )


def _render_within_action_matrix(action_idx, action_text):
    """Render the pairing matrix for a single action."""
    action_key = str(action_idx)

    tech_domains = st.session_state.selected_nist_domains
    eth_domains = st.session_state.selected_pfce_domains

    if action_key not in st.session_state.interaction_matrix:
        st.session_state.interaction_matrix[action_key] = {}

    matrix = st.session_state.interaction_matrix[action_key]

    st.markdown(f"### Action {action_idx + 1}: Interaction Matrix")
    st.markdown(f"> {action_text}")

    # Show relationship type legend
    with st.expander("Relationship Type Definitions", expanded=False):
        for rel_type, desc in RELATIONSHIP_DESCRIPTIONS.items():
            css_class = RELATIONSHIP_COLORS[rel_type]
            st.markdown(
                f'<div class="{css_class}"><strong>{rel_type}:</strong> {desc}</div>',
                unsafe_allow_html=True,
            )

    for tech_domain in tech_domains:
        tech_text = _get_response_text(action_idx, tech_domain, "nist")

        for eth_domain in eth_domains:
            eth_text = _get_response_text(action_idx, eth_domain, "pfce")

            cell_key = f"{tech_domain}|{eth_domain}"
            if cell_key not in matrix:
                matrix[cell_key] = {
                    "relationship": "",
                    "explanation": "",
                    "at_stake": "",
                }

            cell = matrix[cell_key]

            with st.expander(
                f"{tech_domain} × {eth_domain}",
                expanded=True,
            ):
                col_tech, col_eth = st.columns(2)
                with col_tech:
                    st.markdown(
                        f'<div class="section-header-tech">'
                        f"{tech_domain} (Technical)</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(tech_text)
                with col_eth:
                    st.markdown(
                        f'<div class="section-header-eth">'
                        f"{eth_domain} (Ethical)</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(eth_text)

                # Relationship selector
                rel_idx = 0
                if cell["relationship"] in RELATIONSHIP_TYPES:
                    rel_idx = RELATIONSHIP_TYPES.index(cell["relationship"])

                rel_choice = st.selectbox(
                    "Relationship type",
                    RELATIONSHIP_TYPES,
                    index=rel_idx,
                    key=f"rel_{action_key}_{tech_domain}_{eth_domain}",
                    help="Select the relationship between these considerations.",
                )
                cell["relationship"] = rel_choice

                # Color-coded display
                if rel_choice and rel_choice in RELATIONSHIP_COLORS:
                    css_class = RELATIONSHIP_COLORS[rel_choice]
                    st.markdown(
                        f'<div class="{css_class}">'
                        f"<strong>{rel_choice}</strong>: "
                        f"{RELATIONSHIP_DESCRIPTIONS.get(rel_choice, '')}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                # Optional explanation for alignment/independence
                if rel_choice in ("Alignment", "Independence"):
                    cell["explanation"] = st.text_area(
                        "Brief explanation (optional)",
                        value=cell.get("explanation", ""),
                        key=f"expl_{action_key}_{tech_domain}_{eth_domain}",
                        height=60,
                        placeholder="Optionally explain this relationship...",
                    )

                # Follow-up for tension/conflict
                if rel_choice in ("Tension", "Conflict"):
                    cell["at_stake"] = st.text_area(
                        "Briefly, what is at stake in this tension?",
                        value=cell.get("at_stake", ""),
                        key=f"atstake_{action_key}_{tech_domain}_{eth_domain}",
                        height=80,
                        placeholder="One to two sentences describing what is in tension and why it matters...",
                    )

            matrix[cell_key] = cell

    st.session_state.interaction_matrix[action_key] = matrix


def _render_cross_action_comparison():
    """Display side-by-side specification text across actions per domain."""
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
    st.markdown("## Cross-Action Comparison")
    st.markdown(
        "View-only display showing how different actions produce different "
        "considerations within the same domain."
    )

    actions = _get_actions()
    all_domains = (
        [(d, "nist") for d in st.session_state.selected_nist_domains]
        + [(d, "pfce") for d in st.session_state.selected_pfce_domains]
    )

    for domain_key, domain_type in all_domains:
        if domain_type == "nist":
            header_class = "section-header-tech"
            label = f"{domain_key} (NIST CSF)"
        else:
            header_class = "section-header-eth"
            label = f"{domain_key} (PFCE)"

        st.markdown(
            f'<div class="{header_class}">{label}</div>',
            unsafe_allow_html=True,
        )

        cols = st.columns(len(actions))
        for col, (action_idx, action_text) in zip(cols, actions):
            with col:
                st.markdown(f"**Action {action_idx + 1}**")
                st.caption(
                    action_text[:100] + ("..." if len(action_text) > 100 else "")
                )
                text = _get_response_text(action_idx, domain_key, domain_type)
                st.markdown(text)

        st.markdown("")


def _check_stage5_complete():
    """Check all matrix cells have relationships and tension/conflict have follow-ups."""
    actions = _get_actions()
    tech_domains = st.session_state.selected_nist_domains
    eth_domains = st.session_state.selected_pfce_domains

    for action_idx, _ in actions:
        action_key = str(action_idx)
        matrix = st.session_state.interaction_matrix.get(action_key, {})

        for tech_domain in tech_domains:
            for eth_domain in eth_domains:
                cell_key = f"{tech_domain}|{eth_domain}"
                cell = matrix.get(cell_key, {})

                rel = cell.get("relationship", "")
                if not rel:
                    return False

                if rel in ("Tension", "Conflict"):
                    if not cell.get("at_stake", "").strip():
                        return False
    return True


def render_stage5():
    """Interaction examination with within-action matrices and cross-action comparison."""
    st.header("Stage 5: Interaction Examination")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Make relationships among elicited "
        "considerations visible. For each action, pair every technical "
        "consideration with every ethical consideration and characterize "
        "the relationship."
        "</div>",
        unsafe_allow_html=True,
    )

    actions = _get_actions()

    # Component 1: Within-Action Pairing Matrices
    st.markdown("## Within-Action Pairing Matrices")
    for action_idx, action_text in actions:
        _render_within_action_matrix(action_idx, action_text)
        st.markdown("")

    # Component 2: Cross-Action Comparison
    _render_cross_action_comparison()

    # Validation
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
    complete = _check_stage5_complete()

    if not complete:
        st.info(
            "Select a relationship type for every cell. For tension and "
            "conflict relationships, complete both follow-up questions."
        )
    else:
        st.success("Interaction examination complete.")
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
