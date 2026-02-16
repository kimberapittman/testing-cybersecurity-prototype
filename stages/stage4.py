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

    st.markdown("<br>", unsafe_allow_html=True)

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
        "For each declared action and each activated domain, select "
        "the considerations that apply. Use the guiding questions to "
        "direct your attention. Select 'Other' to add considerations "
        "not listed."
    )

    actions = _get_actions()
    all_domains = (
        [(d, "nist") for d in st.session_state.selected_nist_domains]
        + [(d, "pfce") for d in st.session_state.selected_pfce_domains]
    )

    # Ensure data structures exist
    if not isinstance(st.session_state.tier2_responses, dict):
        st.session_state.tier2_responses = {}
    if not isinstance(st.session_state.tier2_same_as, dict):
        st.session_state.tier2_same_as = {}

    for action_idx, action_text in actions:
        action_key = str(action_idx)

        if action_key not in st.session_state.tier2_responses:
            st.session_state.tier2_responses[action_key] = {}
        if action_key not in st.session_state.tier2_same_as:
            st.session_state.tier2_same_as[action_key] = {}

        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
        st.markdown(f"### Action {action_idx + 1}")
        st.markdown(f"> {action_text}")

        # Technical domains section
        tech_domains = [
            (d, t) for d, t in all_domains if t == "nist"
        ]
        eth_domains = [
            (d, t) for d, t in all_domains if t == "pfce"
        ]

        if tech_domains:
            st.markdown(
                '<div class="section-header-tech">'
                "Technical Considerations (NIST CSF)</div>",
                unsafe_allow_html=True,
            )
            _render_domain_prompts(
                action_idx, action_key, tech_domains, actions, NIST_DOMAINS
            )

        if eth_domains:
            st.markdown(
                '<div class="section-header-eth">'
                "Ethical Considerations (PFCE)</div>",
                unsafe_allow_html=True,
            )
            _render_domain_prompts(
                action_idx, action_key, eth_domains, actions, PFCE_DOMAINS
            )


def _render_domain_prompts(action_idx, action_key, domains, all_actions,
                           domain_defs):
    """Render consolidated prompt with patterns for a set of domains for one action."""
    for domain_key, domain_type in domains:
        domain_info = domain_defs[domain_key]

        with st.expander(
            f"{domain_key}: {domain_info['description']}",
            expanded=True,
        ):
            # "Same as" option for second action onward
            if action_idx > 0:
                prior_actions = [
                    (i, text)
                    for i, text in all_actions
                    if i < action_idx
                ]
                if prior_actions:
                    same_as_options = ["Specify fresh"] + [
                        f"Same as Action {i + 1}" for i, _ in prior_actions
                    ]
                    same_key = f"same_as_{action_key}_{domain_key}_{action_idx}"

                    current_same = st.session_state.tier2_same_as.get(
                        action_key, {}
                    ).get(domain_key)
                    default_idx = 0
                    if current_same is not None:
                        for j, (pi, _) in enumerate(prior_actions):
                            if pi == current_same:
                                default_idx = j + 1
                                break

                    choice = st.selectbox(
                        f"Copy from prior action?",
                        same_as_options,
                        index=default_idx,
                        key=same_key,
                    )

                    if choice != "Specify fresh":
                        source_idx = prior_actions[
                            same_as_options.index(choice) - 1
                        ][0]
                        if action_key not in st.session_state.tier2_same_as:
                            st.session_state.tier2_same_as[action_key] = {}
                        st.session_state.tier2_same_as[action_key][
                            domain_key
                        ] = source_idx
                        st.info(
                            f"Using responses from Action {source_idx + 1} "
                            f"for {domain_key}."
                        )
                        continue
                    else:
                        if action_key in st.session_state.tier2_same_as:
                            st.session_state.tier2_same_as[action_key].pop(
                                domain_key, None
                            )

            # Initialize response storage for this domain
            if domain_key not in st.session_state.tier2_responses.get(
                action_key, {}
            ):
                st.session_state.tier2_responses[action_key][domain_key] = {}

            responses = st.session_state.tier2_responses[action_key][domain_key]

            # Display the consolidated Tier 2 prompt
            st.markdown(f"**{domain_info['tier2_prompt']}**")

            # Display guidance questions as non-interactive reference
            with st.expander("Guiding considerations", expanded=False):
                for g in domain_info["guidance"]:
                    st.markdown(f"- {g}")

            # Render pattern checkboxes
            uid = f"{action_key}_{domain_key}"
            selected_patterns = []

            for pat_idx, pattern_label in enumerate(domain_info["patterns"]):
                pat_uid = f"pat_{uid}_{pat_idx}"
                cb_val = st.session_state.get(pat_uid, False)

                is_checked = st.checkbox(
                    pattern_label,
                    value=cb_val,
                    key=pat_uid,
                )

                if is_checked:
                    selected_patterns.append(pattern_label)

            # "Other" free text — always visible
            other_uid = f"pat_other_{uid}"
            other_val = st.text_input(
                "Other",
                value=st.session_state.get(other_uid, ""),
                key=other_uid,
                placeholder="Describe any other consideration not listed above...",
            )
            if other_val.strip():
                selected_patterns.append(f"[Other] {other_val.strip()}")

            # N/A option
            na_uid = f"pat_na_{uid}"
            na_val = st.checkbox(
                "Not applicable to this action",
                value=st.session_state.get(na_uid, False),
                key=na_uid,
            )

            # Store as composite string for downstream consumption
            # Format: pipe-separated pattern labels, or "N/A"
            if na_val:
                responses["0"] = "N/A"
            elif selected_patterns:
                responses["0"] = " | ".join(selected_patterns)
            else:
                responses["0"] = ""


def _check_tier2_complete():
    """No mandatory completion required for Tier 2. User may proceed at any time."""
    return True


def render_stage4():
    """Two-tier consideration elicitation."""
    st.header("Stage 4: Consideration Elicitation")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Systematically elicit ethical and technical "
        "considerations using NIST CSF and PFCE as interpretive lenses."
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
        st.success("Ready to proceed to examination.")
        if st.button(
            "Proceed to Stage 5: Interaction Examination →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.current_stage = 5
            st.session_state.max_unlocked_stage = max(
                st.session_state.max_unlocked_stage, 5
            )
            st.rerun()
