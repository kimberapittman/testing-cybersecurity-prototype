"""Stage 2: Constraint Declaration."""

import streamlit as st


CONSTRAINT_CATEGORIES = [
    ("institutional_constraints", "Institutional Constraints",
     "Organizational structures, reporting hierarchies, decision-making norms."),
    ("governance_constraints", "Governance Constraints",
     "Oversight requirements, approval processes, accountability structures."),
    ("legal_constraints", "Legal Constraints",
     "Statutory, regulatory, or contractual obligations."),
    ("temporal_constraints", "Temporal Constraints",
     "Deadlines, time pressures, scheduling dependencies."),
    ("resource_constraints", "Resource Constraints",
     "Budget, staffing, technical capacity, or infrastructure limits."),
]


def render_stage2():
    """Define the option space through constraint declaration."""
    st.header("Stage 2: Constraint Declaration")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Define the option space. Constraints are "
        "analytically prior to all subsequent stages — they determine what "
        "actions are feasible."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "Declare constraints across five categories. Empty categories are "
        "permitted if intentionally left blank."
    )

    for key, label, help_text in CONSTRAINT_CATEGORIES:
        st.session_state[key] = st.text_area(
            label,
            value=st.session_state[key],
            placeholder=f"Describe any {label.lower()} affecting this decision...",
            help=help_text,
            key=f"input_{key}",
        )

    # Check which categories have content
    filled_categories = []
    empty_categories = []
    for key, label, _ in CONSTRAINT_CATEGORIES:
        if st.session_state[key].strip():
            filled_categories.append(label)
        else:
            empty_categories.append(label)

    has_content = len(filled_categories) > 0

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    if not has_content:
        st.info(
            "At least one constraint category must have content to proceed."
        )
        return

    # If there are empty categories, require confirmation
    if empty_categories:
        st.markdown("**The following categories are empty:**")
        for cat in empty_categories:
            st.markdown(f"- {cat}")

        st.session_state.stage2_confirmed_blanks = st.checkbox(
            "I confirm these categories are intentionally left blank, "
            "not overlooked.",
            value=st.session_state.stage2_confirmed_blanks,
            key="input_stage2_confirmed_blanks",
        )

        if not st.session_state.stage2_confirmed_blanks:
            st.warning(
                "Please confirm that empty categories are intentional "
                "before proceeding."
            )
            return

    if st.button(
        "Proceed to Stage 3: Action-Set Declaration →",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.current_stage = 3
        st.session_state.max_unlocked_stage = max(
            st.session_state.max_unlocked_stage, 3
        )
        st.rerun()
