"""Stage 3: Action-Set Declaration."""

import streamlit as st


def render_stage3():
    """Declare feasible actions within declared constraints."""
    st.header("Stage 3: Action-Set Declaration")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Declare feasible actions within the "
        "constraints established in Stage 2. Each action is an independent "
        "operational commitment, not implementation detail."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "Each action should describe an operational commitment — what you "
        "would actually do — rather than implementation steps."
    )

    actions = st.session_state.actions

    # Render existing action fields
    updated_actions = []
    for i in range(len(actions)):
        col1, col2 = st.columns([20, 1])
        with col1:
            val = st.text_area(
                f"Action {i + 1}",
                value=actions[i],
                placeholder=f"Describe action {i + 1} at the operational commitment level...",
                key=f"input_action_{i}",
            )
            updated_actions.append(val)
        with col2:
            if len(actions) > 1:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✕", key=f"remove_action_{i}", help="Remove this action"):
                    actions.pop(i)
                    st.session_state.actions = actions
                    st.rerun()

    st.session_state.actions = updated_actions

    # Add more actions button
    if st.button("+ Add Another Action", key="add_action"):
        st.session_state.actions.append("")
        st.rerun()

    filled_actions = [a for a in st.session_state.actions if a.strip()]

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    if not filled_actions:
        st.info("Declare at least one action to proceed to Stage 4.")
    else:
        st.success(f"{len(filled_actions)} action(s) declared.")
        if st.button(
            "Proceed to Stage 4: Consideration Elicitation →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.current_stage = 4
            st.session_state.max_unlocked_stage = max(
                st.session_state.max_unlocked_stage, 4
            )
            st.rerun()
