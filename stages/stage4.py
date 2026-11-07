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

            # 4. Pattern checkboxes — inside collapsed expander. A selected
            # pattern is a recognition aid, not a consideration: it carries a
            # brief specification of how it applies to this action.
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
                        spec_uid = f"patspec_{uid}_{pat_idx}"
                        pattern_spec = st.text_input(
                            f"How does '{pattern_label}' apply to this action?",
                            value=st.session_state.get(spec_uid, ""),
                            key=spec_uid,
                            placeholder="Briefly describe how this applies to this action...",
                            label_visibility="collapsed",
                        )
                        selected_patterns.append({
                            "label": pattern_label,
                            "specification": pattern_spec.strip(),
                        })

            # 5. N/A checkbox
            na_uid = f"pat_na_{uid}"
            na_val = st.checkbox(
                "Not applicable to this action",
                value=st.session_state.get(na_uid, False),
                key=na_uid,
            )
            if na_val:
                st.info(
                    "This domain was selected as relevant at Tier 1. "
                    "Marking it N/A will exclude it from this action's "
                    "considerations."
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


def pattern_label(pattern):
    """A pattern is a dict; sessions begun before this change may hold a string."""
    if isinstance(pattern, dict):
        return pattern.get("label", "")
    return str(pattern)


def pattern_is_specified(pattern):
    """True if this selected pattern says how it applies to the action."""
    if isinstance(pattern, dict):
        return bool(pattern.get("specification", "").strip())
    return True


def _activated_domains():
    """Return every domain activated at Tier 1, ethical before technical."""
    return (
        list(st.session_state.selected_pfce_domains)
        + list(st.session_state.selected_nist_domains)
    )


def _is_dispositioned(action_key, domain_key):
    """True if this action+domain carries content or an explicit N/A mark.

    Content is not required — a domain may legitimately not apply to a given
    action — but the determination must be recorded rather than left silent.
    """
    data = (
        st.session_state.tier2_responses
        .get(action_key, {})
        .get(domain_key, {})
        .get("0", {})
    )

    if isinstance(data, str):
        return bool(data.strip())

    return bool(
        data.get("na", False)
        or data.get("text", "").strip()
        or data.get("patterns", [])
    )


def _find_undispositioned():
    """Return (action number, domain key) pairs still awaiting a disposition."""
    domains = _activated_domains()
    return [
        (action_idx + 1, domain_key)
        for action_idx, _ in _get_actions()
        for domain_key in domains
        if not _is_dispositioned(str(action_idx), domain_key)
    ]


def _find_unspecified_patterns():
    """Return (action number, domain key, label) for patterns lacking a spec."""
    domains = _activated_domains()
    found = []
    for action_idx, _ in _get_actions():
        for domain_key in domains:
            data = (
                st.session_state.tier2_responses
                .get(str(action_idx), {})
                .get(domain_key, {})
                .get("0", {})
            )
            if not isinstance(data, dict):
                continue
            for pattern in data.get("patterns", []):
                if not pattern_is_specified(pattern):
                    found.append(
                        (action_idx + 1, domain_key, pattern_label(pattern))
                    )
    return found


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

    _render_tier1()

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    if not _activated_domains():
        st.info(
            "Select at least one domain above to proceed. Domains not "
            "selected here are recorded as not implicated by this "
            "decision point."
        )
        return

    _render_tier2()

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    undispositioned = _find_undispositioned()
    unspecified = _find_unspecified_patterns()

    if undispositioned:
        st.info(
            f"{len(undispositioned)} domain(s) await a disposition. For each "
            "action, describe the considerations that apply, select a common "
            "consideration, or mark the domain not applicable."
        )
        for action_num, domain_key in undispositioned[:10]:
            st.markdown(f"- Action {action_num} — {domain_key}")
        if len(undispositioned) > 10:
            st.markdown(f"- …and {len(undispositioned) - 10} more")
    elif unspecified:
        st.info(
            f"{len(unspecified)} selected consideration(s) need a brief "
            "specification of how they apply to the action. A selection "
            "without a specification records that something applies without "
            "recording what."
        )
        for action_num, domain_key, label in unspecified[:10]:
            st.markdown(f"- Action {action_num} — {domain_key}: {label}")
        if len(unspecified) > 10:
            st.markdown(f"- …and {len(unspecified) - 10} more")
    else:
        st.success("Ready to proceed to integration.")
        if st.button(
            "Proceed to Stage 5: Integration →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.current_stage = 5
            st.session_state.max_unlocked_stage = max(
                st.session_state.max_unlocked_stage, 5
            )
            st.rerun()
