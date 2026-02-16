"""Stage 1: Decision-Point Specification."""

import streamlit as st


def render_stage1():
    """Establish the unit of analysis."""
    st.header("Stage 1: Decision-Point Specification")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Establish the unit of analysis — what decision "
        "must be made."
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

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

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
