"""Stage 4: Consideration Elicitation (Two-Tier)."""

import streamlit as st
from domain_data import NIST_DOMAINS, PFCE_DOMAINS


def _render_domain_card(domain_key: str, prompt: str, description: str,
                        selected: bool, card_key: str) -> bool:
    """Render a selectable domain card. Returns the new selected state."""
    css_class = "domain-card-selected" if selected else "domain-card"
    checkmark = '<span class="checkmark">✓</span>' if selected else ""

    st.markdown(
        f'<div class="{css_class}">'
        f'{checkmark}'
        f'<div class="domain-card-title">{domain_key}</div>'
        f'<div class="domain-card-desc">{prompt}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )
    return st.checkbox(
        f"Select {domain_key}",
        value=selected,
        key=card_key,
        label_visibility="collapsed",
    )


def _render_tier1():
    """Tier 1: Domain Identification — select applicable domains."""
    st.subheader("Tier 1: Domain Identification")
    st.markdown(
        "Select all domains that apply to this decision point. "
        "You must select at least one technical (NIST CSF) domain and "
        "at least one ethical (PFCE) domain."
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

    has_nist = len(st.session_state.selected_nist_domains) > 0
    has_pfce = len(st.session_state.selected_pfce_domains) > 0

    if not has_nist:
        st.warning("Select at least one NIST CSF technical domain.")
    if not has_pfce:
        st.warning("Select at least one PFCE ethical domain.")

    return has_nist and has_pfce


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
        "For each declared action, respond to the specification prompts "
        "for each activated domain. Respond with one to two sentences, "
        'or mark "Not applicable to this action."'
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

        st.markdown("---")
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
    """Render prompts for a set of domains for one action."""
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
                        # Extract source action index
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

            # Render individual prompts
            if domain_key not in st.session_state.tier2_responses.get(
                action_key, {}
            ):
                st.session_state.tier2_responses[action_key][domain_key] = {}

            responses = st.session_state.tier2_responses[action_key][domain_key]

            for p_idx, prompt_text in enumerate(domain_info["prompts"]):
                prompt_key = str(p_idx)
                current_val = responses.get(prompt_key, "")

                col1, col2 = st.columns([5, 1])
                with col1:
                    response = st.text_area(
                        prompt_text,
                        value=current_val,
                        placeholder="One to two sentences...",
                        key=f"t2_{action_key}_{domain_key}_{p_idx}",
                        height=80,
                    )
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    na_key = f"na_{action_key}_{domain_key}_{p_idx}"
                    is_na = current_val == "N/A"
                    if st.checkbox(
                        "N/A",
                        value=is_na,
                        key=na_key,
                        help="Mark as not applicable to this action",
                    ):
                        response = "N/A"

                st.session_state.tier2_responses[action_key][domain_key][
                    prompt_key
                ] = response


def _check_tier2_complete():
    """Check if all activated domains for all actions have responses."""
    actions = _get_actions()
    all_nist = st.session_state.selected_nist_domains
    all_pfce = st.session_state.selected_pfce_domains

    for action_idx, _ in actions:
        action_key = str(action_idx)
        all_domains_for_action = all_nist + all_pfce

        for domain_key in all_domains_for_action:
            # Check if "same as" is set
            same_as = st.session_state.tier2_same_as.get(
                action_key, {}
            ).get(domain_key)
            if same_as is not None:
                continue

            # Check if domain is in NIST or PFCE
            if domain_key in NIST_DOMAINS:
                prompts = NIST_DOMAINS[domain_key]["prompts"]
            else:
                prompts = PFCE_DOMAINS[domain_key]["prompts"]

            responses = st.session_state.tier2_responses.get(
                action_key, {}
            ).get(domain_key, {})

            for p_idx in range(len(prompts)):
                val = responses.get(str(p_idx), "").strip()
                if not val:
                    return False
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

    st.markdown("---")
    _render_tier2()

    st.markdown("---")

    tier2_complete = _check_tier2_complete()

    if not tier2_complete:
        st.info(
            "Complete all specification prompts (or mark N/A) for every "
            "activated domain and every action to proceed."
        )
    else:
        st.success("All considerations specified.")
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
