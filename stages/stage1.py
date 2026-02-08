"""Stage 1: Decision-Point Specification."""

import streamlit as st


def render_stage1():
    """Establish the unit of analysis."""
    st.header("Stage 1: Decision-Point Specification")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Establish the unit of analysis — what decision "
        "must be made, who has authority, and why deferral is not feasible."
        "</div>",
        unsafe_allow_html=True,
    )

    st.session_state.decision_description = st.text_area(
        "Decision point description",
        value=st.session_state.decision_description,
        placeholder="What decision must be made?",
        help="Describe the decision that must be made.",
        key="input_decision_description",
    )

    st.session_state.responsible_actor = st.text_area(
        "Responsible actor",
        value=st.session_state.responsible_actor,
        placeholder="Who has authority to make this decision?",
        help="Identify the person or role with decision authority.",
        key="input_responsible_actor",
    )

    st.session_state.scope_of_authority = st.text_area(
        "Scope of authority",
        value=st.session_state.scope_of_authority,
        placeholder="What does this actor have authority to do?",
        help="Define the boundaries of the decision-maker's authority.",
        key="input_scope_of_authority",
    )

    st.session_state.why_no_deferral = st.text_area(
        "Why deferral is not feasible",
        value=st.session_state.why_no_deferral,
        placeholder="What is the material consequence of inaction?",
        help="Explain why this decision cannot be deferred.",
        key="input_why_no_deferral",
    )

    # Validation
    all_filled = all([
        st.session_state.decision_description.strip(),
        st.session_state.responsible_actor.strip(),
        st.session_state.scope_of_authority.strip(),
        st.session_state.why_no_deferral.strip(),
    ])

    st.markdown("---")

    if not all_filled:
        st.info("Complete all four fields to proceed to Stage 2.")
    else:
        if st.button(
            "Proceed to Stage 2: Constraint Declaration →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.current_stage = 2
            st.session_state.max_unlocked_stage = max(
                st.session_state.max_unlocked_stage, 2
            )
            st.rerun()
