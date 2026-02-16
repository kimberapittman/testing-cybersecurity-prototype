"""Stage 1: Decision-Point Specification."""

import streamlit as st


def render_stage1():
    """Establish the unit of analysis."""
    st.header("Stage 1: Decision-Point Specification")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Establish the unit of analysis — what decision "
        "must be made and who has authority."
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

    # Validation
    all_filled = all([
        st.session_state.decision_description.strip(),
        st.session_state.responsible_actor.strip(),
    ])

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    if not all_filled:
        st.info("Complete both fields to proceed to Stage 2.")
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
