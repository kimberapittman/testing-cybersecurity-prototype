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

    st.markdown(
        "A decision point is a specific question facing a specific "
        "decision-maker at a specific moment. It should be narrow enough "
        "that you can identify concrete actions under consideration. "
        "For example: *'Whether to pay the ransomware demand or refuse "
        "payment and pursue system reconstruction.'* A decision point is "
        "NOT a broad goal or strategy such as *'How to improve our "
        "cybersecurity posture.'*"
    )

    st.session_state.decision_description = st.text_area(
        "Decision point description",
        value=st.session_state.decision_description,
        placeholder="What decision must be made?",
        help="Describe the decision that must be made.",
        key="input_decision_description",
    )

    st.session_state.responsible_actor = st.text_input(
        "Decision-maker name or role",
        value=st.session_state.responsible_actor,
        placeholder="Who is the decision-maker?",
        help="Identify the person or role with authority to make this decision.",
        key="input_responsible_actor",
    )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    if st.button(
        "Proceed to Stage 2: Decision Environment →",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.current_stage = 2
        st.session_state.max_unlocked_stage = max(
            st.session_state.max_unlocked_stage, 2
        )
        st.rerun()
