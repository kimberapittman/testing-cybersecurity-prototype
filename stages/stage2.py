"""Stage 2: Constraint Declaration."""

import streamlit as st


CONSTRAINT_CATEGORIES = [
    (
        "authority",
        "Authority",
        "Does the decision-maker have unilateral authority to act, or does "
        "this action require approval, cooperation, or authorization from "
        "other parties (e.g., council, department heads, elected officials)?",
    ),
    (
        "technical_architecture",
        "Technical Architecture",
        "Does the current system architecture limit what actions can be "
        "performed? Are there technical dependencies, shared infrastructure, "
        "or system configurations that prevent certain modifications?",
    ),
    (
        "personnel_expertise",
        "Available Resources — staffing, funding, and expertise",
        "Are the staffing, funding, and expertise required to execute the actions "
        "under consideration available at the time of this decision?",
    ),
    (
        "budget_procurement",
        "Budget and Procurement Authority",
        "Does the decision-maker have access to funds or authority to commit "
        "resources needed to execute the actions under consideration?",
    ),
    (
        "legal_regulatory",
        "Legal and Regulatory Requirements",
        "Are there legal obligations, regulatory requirements, or "
        "contractual terms that require or prohibit specific actions "
        "(e.g., data retention laws, public records requirements, "
        "vendor agreements)?",
    ),
    (
        "time",
        "Time",
        "Does the decision context impose time constraints that limit "
        "which actions can be initiated, completed, or deliberated "
        "within the available window?",
    ),
    (
        "vendor_contractual",
        "Vendor and Contractual Dependencies",
        "Does execution of any action depend on a vendor or third party "
        "whose cooperation, authorization, or technical support is required?",
    ),
]


def render_stage2():
    """Define the option space through constraint declaration."""
    st.header("Stage 2: Decision Environment")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Establish the decision environment. Constraints are "
        "analytically prior to all subsequent stages — they inform what "
        "actions are feasible."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "Select only the constraints that apply to your specific decision "
        "context — not all will be relevant to every decision. "
        "The constraints you declare here define which actions are "
        "feasible in Stage 3."
    )

    # Initialize constraint state if needed
    if "constraints" not in st.session_state:
        st.session_state.constraints = {}

    for key, label, prompt in CONSTRAINT_CATEGORIES:
        selected = st.checkbox(
            f"**{label}** :gray[ — {prompt}]",
            value=key in st.session_state.constraints,
            key=f"chk_{key}",
        )

        if selected:
            spec = st.text_area(
                f"Describe how this constraint applies to your decision",
                value=st.session_state.constraints.get(key, {}).get(
                    "specification", ""
                ),
                placeholder=f"Describe how {label.lower()} constrains this decision...",
                key=f"spec_{key}",
                label_visibility="collapsed",
            )
            st.session_state.constraints[key] = {
                "label": label,
                "specification": spec,
            }
        else:
            # Remove if unchecked
            st.session_state.constraints.pop(key, None)

    # "Other" — selectable like the rest
    other_selected = st.checkbox(
        "**Other** :gray[ — Are there additional constraints not listed above "
        "that shape what actions are feasible at this decision point?]",
        value="other" in st.session_state.constraints,
        key="chk_other",
    )

    if other_selected:
        other_text = st.text_area(
            "Other constraints",
            value=st.session_state.constraints.get("other", {}).get(
                "specification", ""
            ),
            placeholder="Describe any additional constraints...",
            key="spec_other",
            label_visibility="collapsed",
        )
        st.session_state.constraints["other"] = {
            "label": "Other",
            "specification": other_text,
        }
    else:
        st.session_state.constraints.pop("other", None)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    if st.button(
        "Proceed to Stage 3: Declared Actions →",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.current_stage = 3
        st.session_state.max_unlocked_stage = max(
            st.session_state.max_unlocked_stage, 3
        )
        st.rerun()
