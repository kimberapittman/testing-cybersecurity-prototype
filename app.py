"""
Cybersecurity Decision-Support Prototype
Linear stage-based progression through six analytical stages.
"""

import streamlit as st
from stages.stage1 import render_stage1
from stages.stage2 import render_stage2
from stages.stage3 import render_stage3
from stages.stage4 import render_stage4
from stages.stage5 import render_stage5
from stages.stage6 import render_stage6
from styles import inject_custom_css


def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "current_stage": 1,
        "max_unlocked_stage": 1,
        # Stage 1
        "decision_description": "",
        "responsible_actor": "",
        "scope_of_authority": "",
        "why_no_deferral": "",
        # Stage 2
        "institutional_constraints": "",
        "governance_constraints": "",
        "legal_constraints": "",
        "temporal_constraints": "",
        "resource_constraints": "",
        "stage2_confirmed_blanks": False,
        # Stage 3
        "actions": ["", ""],
        # Stage 4
        "selected_nist_domains": [],
        "selected_pfce_domains": [],
        # Stage 4 Tier 2 — stored as nested dicts:
        # tier2_responses[action_idx][domain_key][prompt_idx] = response text
        "tier2_responses": {},
        # tier2_same_as[action_idx][domain_key] = source_action_idx or None
        "tier2_same_as": {},
        # Stage 5
        # interaction_matrix[action_idx][(tech_domain, eth_domain)] = {
        #   "relationship": str, "explanation": str,
        #   "foregone": str, "consequences": str
        # }
        "interaction_matrix": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_downstream(from_stage: int):
    """Clear all data from stages after from_stage."""
    if from_stage < 2:
        st.session_state.institutional_constraints = ""
        st.session_state.governance_constraints = ""
        st.session_state.legal_constraints = ""
        st.session_state.temporal_constraints = ""
        st.session_state.resource_constraints = ""
        st.session_state.stage2_confirmed_blanks = False
    if from_stage < 3:
        st.session_state.actions = ["", ""]
    if from_stage < 4:
        st.session_state.selected_nist_domains = []
        st.session_state.selected_pfce_domains = []
        st.session_state.tier2_responses = {}
        st.session_state.tier2_same_as = {}
    if from_stage < 5:
        st.session_state.interaction_matrix = {}


def navigate_to(stage: int):
    """Navigate to a stage, clearing downstream if going backward."""
    if stage < st.session_state.current_stage:
        clear_downstream(stage)
        st.session_state.max_unlocked_stage = stage
    st.session_state.current_stage = stage


def render_progress_bar():
    """Render a visual progress indicator for the six stages."""
    stage_names = [
        "Decision Point",
        "Constraints",
        "Actions",
        "Considerations",
        "Interactions",
        "Documentation",
    ]
    cols = st.columns(6)
    for i, (col, name) in enumerate(zip(cols, stage_names), 1):
        with col:
            if i == st.session_state.current_stage:
                st.markdown(
                    f'<div class="stage-indicator stage-current">'
                    f'<div class="stage-number">{i}</div>'
                    f'<div class="stage-label">{name}</div></div>',
                    unsafe_allow_html=True,
                )
            elif i <= st.session_state.max_unlocked_stage:
                st.markdown(
                    f'<div class="stage-indicator stage-completed">'
                    f'<div class="stage-number">{i}</div>'
                    f'<div class="stage-label">{name}</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="stage-indicator stage-locked">'
                    f'<div class="stage-number">{i}</div>'
                    f'<div class="stage-label">{name}</div></div>',
                    unsafe_allow_html=True,
                )


def render_navigation():
    """Render backward navigation buttons for unlocked stages."""
    if st.session_state.current_stage > 1:
        st.markdown("---")
        st.markdown("**Navigate to a previous stage:**")
        cols = st.columns(st.session_state.current_stage - 1)
        stage_names = [
            "Stage 1: Decision Point",
            "Stage 2: Constraints",
            "Stage 3: Actions",
            "Stage 4: Considerations",
            "Stage 5: Interactions",
        ]
        for i, col in enumerate(cols):
            stage_num = i + 1
            with col:
                if st.button(
                    f"← {stage_names[i]}",
                    key=f"nav_back_{stage_num}",
                    use_container_width=True,
                ):
                    st.warning(
                        f"Navigating back to Stage {stage_num} will clear all "
                        f"data from subsequent stages."
                    )
                    navigate_to(stage_num)
                    st.rerun()


def main():
    st.set_page_config(
        page_title="Cybersecurity Decision-Support Prototype",
        page_icon="🔒",
        layout="wide",
    )
    inject_custom_css()
    init_session_state()

    st.title("Cybersecurity Decision-Support Prototype")
    st.caption(
        "A structured approach to cybersecurity decision analysis using "
        "NIST CSF and PFCE frameworks."
    )

    render_progress_bar()
    st.markdown("---")

    stage = st.session_state.current_stage
    if stage == 1:
        render_stage1()
    elif stage == 2:
        render_stage2()
    elif stage == 3:
        render_stage3()
    elif stage == 4:
        render_stage4()
    elif stage == 5:
        render_stage5()
    elif stage == 6:
        render_stage6()

    render_navigation()

    # Session notice
    st.markdown("---")
    st.caption(
        "⚠ No persistent storage. All data exists only for the duration of "
        "this session. Use Stage 6 export to preserve your analysis."
    )


if __name__ == "__main__":
    main()
