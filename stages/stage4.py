"""Stage 4: Consideration Elicitation (Two-Tier)."""

import streamlit as st
from domain_data import NIST_DOMAINS, PFCE_DOMAINS


def _render_domain_card(domain_key: str, prompt: str, description: str,
                        selected: bool, card_key: str) -> bool:
    """Render a selectable domain as an inline checkbox. Returns the new selected state."""
    return st.checkbox(
        f"**{domain_key}** :gray[ — {prompt}]",
        value=selected,
        key=card_key,
    )


def _render_tier1():
    """Tier 1: Domain Identification — select applicable domains."""
    st.subheader("Tier 1: Domain Identification")
    st.markdown(
        "Select all domains that apply to this decision point."
    )

    # PFCE domains
    st.markdown(
        '<div class="section-header-eth">PFCE Principles — '
        "Ethical Domains</div>",
        unsafe_allow_html=True,
    )

    pfce_selected = list(st.session_state.selected_pfce_domains)
    for domain_key, domain_info in PFCE_DOMAINS.items():
        is_selected = domain_key in pfce_selected
        new_state = _render_domain_card(
            domain_key,
            domain_info["prompt"],
            domain_info["description"],
            is_selected,
            f"tier1_pfce_{domain_key}",
        )
        if new_state and domain_key not in pfce_selected:
            pfce_selected.append(domain_key)
        elif not new_state and domain_key in pfce_selected:
            pfce_selected.remove(domain_key)

    st.session_state.selected_pfce_domains = pfce_selected

    st.markdown("<br>", unsafe_allow_html=True)

    # NIST CSF domains
    st.markdown(
        '<div class="section-header-tech">NIST CSF Functions — '
        "Technical Domains</div>",
        unsafe_allow_html=True,
    )

    nist_selected = list(st.session_state.selected_nist_domains)
    for domain_key, domain_info in NIST_DOMAINS.items():
        is_selected = domain_key in nist_selected
        new_state = _render_domain_card(
            domain_key,
            domain_info["prompt"],
            domain_info["description"],
            is_selected,
            f"tier1_nist_{domain_key}",
        )
        if new_state and domain_key not in nist_selected:
            nist_selected.append(domain_key)
        elif not new_state and domain_key in nist_selected:
            nist_selected.remove(domain_key)

    st.session_state.selected_nist_domains = nist_selected

    return True


def _get_actions():
    """Return list of non-empty actions with their indices."""
    return [
        (i, action)
        for i, action in enumerate(st.session_state.actions)
        if action.strip()
    ]


def _render_tier2():
    """Tier 2: Consideration Specification per action per activated domain."""
    st.subheader("Tier 2: Consideration Specification")
    st.markdown(
        "For each declared action and each activated domain, describe "
        "the considerations that apply. Use the guiding questions to "
        "direct your attention."
    )

    actions = _get_actions()
    all_domains = (
        [(d, "pfce") for d in st.session_state.selected_pfce_domains]
        + [(d, "nist") for d in st.session_state.selected_nist_domains]
    )

    if not isinstance(st.session_state.tier2_responses, dict):
        st.session_state.tier2_responses = {}

    for action_idx, action_text in actions:
        action_key = str(action_idx)

        if action_key not in st.session_state.tier2_responses:
            st.session_state.tier2_responses[action_key] = {}

        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
        st.markdown(f"### Action {action_idx + 1}")
        st.markdown(f"> {action_text}")

        eth_domains = [
            (d, t) for d, t in all_domains if t == "pfce"
        ]
        tech_domains = [
            (d, t) for d, t in all_domains if t == "nist"
        ]

        if eth_domains:
            st.markdown(
                '<div class="section-header-eth">'
                "Ethical Considerations (PFCE)</div>",
                unsafe_allow_html=True,
            )
            _render_domain_prompts(
                action_idx, action_key, eth_domains, actions, PFCE_DOMAINS
            )

        if tech_domains:
            st.markdown(
                '<div class="section-header-tech">'
                "Technical Considerations (NIST CSF)</div>",
                unsafe_allow_html=True,
            )
            _render_domain_prompts(
                action_idx, action_key, tech_domains, actions, NIST_DOMAINS
            )


def _render_domain_prompts(action_idx, action_key, domains, all_actions,
                           domain_defs):
    """Render Tier 2 prompt with free-text input and optional pattern checkboxes."""
    for domain_key, domain_type in domains:
        domain_info = domain_defs[domain_key]

        with st.expander(
            f"{domain_key}: {domain_info['description']}",
            expanded=True,
        ):

            if domain_key not in st.session_state.tier2_responses.get(
                action_key, {}
            ):
                st.session_state.tier2_responses[action_key][domain_key] = {}

            responses = st.session_state.tier2_responses[action_key][domain_key]

            # 1. Tier 2 prompt
            st.markdown(f"**{domain_info['tier2_prompt']}**")

            # 2. Guidance questions — always visible
            for g in domain_info["guidance"]:
                st.markdown(f"- {g}")

            # 3. Free-text area — primary input
            uid = f"{action_key}_{domain_key}"
            text_uid = f"text_{action_key}_{domain_key}"

            existing = responses.get("0", {})
            if isinstance(existing, dict):
                existing_text = existing.get("text", "")
            else:
                existing_text = ""

            text_val = st.text_area(
                "Describe the considerations that apply to this action for this domain.",
                value=st.session_state.get(text_uid, existing_text),
                key=text_uid,
                height=100,
                placeholder="Based on the guiding questions above, describe any considerations that apply...",
            )

            # 4. Pattern checkboxes — inside collapsed expander
            selected_patterns = []
            with st.expander(
                "Common considerations in this domain (select any that also apply)",
                expanded=False,
            ):
                for pat_idx, pattern_label in enumerate(domain_info["patterns"]):
                    pat_uid = f"pat_{uid}_{pat_idx}"
                    is_checked = st.checkbox(
                        pattern_label,
                        value=st.session_state.get(pat_uid, False),
                        key=pat_uid,
                    )
                    if is_checked:
                        selected_patterns.append(pattern_label)

            # 5. N/A checkbox
            na_uid = f"pat_na_{uid}"
            na_val = st.checkbox(
                "Not applicable to this action",
                value=st.session_state.get(na_uid, False),
                key=na_uid,
            )
            if na_val:
                st.warning(
                    "You indicated this domain was relevant at Tier 1. "
                    "Are you sure no considerations apply to this action?"
                )

            # 6. Store as dict
            if na_val:
                responses["0"] = {"text": "", "patterns": [], "na": True}
            elif text_val.strip() or selected_patterns:
                responses["0"] = {
                    "text": text_val.strip(),
                    "patterns": selected_patterns,
                    "na": False,
                }
            else:
                responses["0"] = {"text": "", "patterns": [], "na": False}


def _check_tier2_complete():
    """No mandatory completion required for Tier 2. User may proceed at any time."""
    return True


def render_stage4():
    """Two-tier consideration elicitation."""
    st.header("Stage 4: Consideration Elicitation")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Systematically elicit ethical and technical "
        "considerations using PFCE and NIST CSF 2.0 as interpretive lenses."
        "</div>",
        unsafe_allow_html=True,
    )

    tier1_complete = _render_tier1()

    if not tier1_complete:
        return

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
    _render_tier2()

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    tier2_complete = _check_tier2_complete()

    if tier2_complete:
        st.success("Ready to proceed to review.")
        if st.button(
            "Proceed to Stage 5: Consideration Review →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.current_stage = 5
            st.session_state.max_unlocked_stage = max(
                st.session_state.max_unlocked_stage, 5
            )
            st.rerun()
