"""
Cybersecurity Decision-Point Analysis Tool
Linear stage-based progression through six analytical stages.
"""

import textwrap
import streamlit as st
from stages.stage1 import render_stage1
from stages.stage2 import render_stage2
from stages.stage3 import render_stage3
from stages.stage4 import render_stage4
from stages.stage5 import render_stage5
from stages.stage6 import render_stage6
from styles import inject_custom_css


def _html_block(s: str) -> str:
    """Strip leading whitespace so indented HTML isn't treated as code."""
    return "\n".join(line.lstrip() for line in textwrap.dedent(s).splitlines())


def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "current_stage": 1,
        "max_unlocked_stage": 1,
        # Stage 1
        "decision_description": "",
        "responsible_actor": "",
        # Stage 2
        "constraints": {},
        # Stage 3
        "actions": [""],
        # Stage 4
        "selected_nist_domains": [],
        "selected_pfce_domains": [],
        # Stage 4 Tier 2
        "tier2_responses": {},
        "tier2_same_as": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_downstream(from_stage: int):
    """Clear all data from stages after from_stage."""
    if from_stage < 2:
        st.session_state.constraints = {}
    if from_stage < 3:
        st.session_state.actions = ["", ""]
    if from_stage < 4:
        st.session_state.selected_nist_domains = []
        st.session_state.selected_pfce_domains = []
        st.session_state.tier2_responses = {}
        st.session_state.tier2_same_as = {}


def navigate_to(stage: int):
    """Navigate to a stage, preserving all entered data."""
    st.session_state.current_stage = stage


def render_divider():
    """Render a blue gradient divider."""
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)


def _sidebar_divider():
    """Render a subtle gradient divider for the sidebar."""
    st.markdown(
        '<hr style="margin:1.25rem 0;border:none;height:1px;'
        "background:linear-gradient(90deg,"
        "rgba(255,255,255,0.00),"
        "rgba(255,255,255,0.35),"
        'rgba(255,255,255,0.00));">',
        unsafe_allow_html=True,
    )


def render_progress_bar():
    """Render glassy stage indicators for the six stages."""
    stage_names = [
        "Decision Point",
        "Constraints",
        "Actions",
        "Considerations",
        "Review",
        "Documentation",
    ]
    cols = st.columns(6)
    for i, (col, name) in enumerate(zip(cols, stage_names), 1):
        with col:
            if i == st.session_state.current_stage:
                css = "stage-indicator stage-current"
            elif i <= st.session_state.max_unlocked_stage:
                css = "stage-indicator stage-completed"
            else:
                css = "stage-indicator stage-locked"
            st.markdown(
                f'<div class="{css}">'
                f'<div class="stage-number">{i}</div>'
                f'<div class="stage-label">{name}</div></div>',
                unsafe_allow_html=True,
            )


def render_sidebar():
    """Render the sidebar with tool overview, about, and resources."""
    with st.sidebar:
        st.markdown(
            "<h3 style='font-weight:700;'>Tool Overview</h3>",
            unsafe_allow_html=True,
        )

        # About section
        st.markdown(
            _html_block(
                """
                <details class="sb-details">
                  <summary>About This Tool</summary>
                  <div class="sb-details-body">

                    <span class="sb-section">What It Does</span>
                    <div class="sb-section-body">
                      <div class="sb-p">
                        This tool provides a structured six-stage reasoning
                        process for cybersecurity decision analysis, combining
                        NIST CSF technical context with PFCE ethical analysis.
                      </div>
                    </div>

                    <span class="sb-section">How It Works</span>
                    <div class="sb-section-body">
                      <div class="sb-p">
                        Progress through six stages: define the decision point,
                        declare constraints, specify actions, elicit
                        considerations, examine interactions, and produce a
                        documented record.
                      </div>
                    </div>

                    <span class="sb-section">Data Handling</span>
                    <div class="sb-section-body">
                      <div class="sb-p">
                        No persistent storage. All data exists only for the
                        duration of this session. Use Stage 6 export to
                        preserve your analysis as PDF.
                      </div>
                    </div>

                  </div>
                </details>
                """
            ),
            unsafe_allow_html=True,
        )

        _sidebar_divider()

        # Resources section
        st.markdown(
            _html_block(
                """
                <details class="sb-details">
                  <summary>Resources</summary>
                  <div class="sb-details-body">

                    <div class="sb-p">
                      This tool draws on two established frameworks:
                    </div>

                    <div style="margin-left:1rem;margin-top:0.5rem;">

                      <div style="margin-bottom:0.75rem;">
                        <a href="https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf"
                           target="_blank"
                           style="font-weight:800;color:white;text-decoration:none;">
                          NIST Cybersecurity Framework (CSF) 2.0
                        </a><br>
                        <span style="font-size:0.9rem;opacity:0.85;">
                          National Institute of Standards and Technology (2024)
                        </span>
                      </div>

                      <div style="margin-bottom:0.75rem;">
                        <a href="https://doi.org/10.1016/j.cose.2021.102382"
                           target="_blank"
                           style="font-weight:800;color:white;text-decoration:none;">
                          Principlist Framework for Cybersecurity Ethics (PFCE)
                        </a><br>
                        <span style="font-size:0.9rem;opacity:0.85;">
                          Formosa, Paul; Michael Wilson; Deborah Richards (2021)
                        </span>
                      </div>

                    </div>

                  </div>
                </details>
                """
            ),
            unsafe_allow_html=True,
        )

        _sidebar_divider()


def render_navigation():
    """Render backward navigation buttons for unlocked stages."""
    if st.session_state.current_stage > 1:
        render_divider()
        st.markdown("**Navigate to a previous stage:**")
        cols = st.columns(st.session_state.current_stage - 1)
        stage_names = [
            "Stage 1: Decision Point",
            "Stage 2: Constraints",
            "Stage 3: Actions",
            "Stage 4: Considerations",
            "Stage 5: Review",
        ]
        for i, col in enumerate(cols):
            stage_num = i + 1
            with col:
                if st.button(
                    f"◀ {stage_names[i]}",
                    key=f"nav_back_{stage_num}",
                    use_container_width=True,
                ):
                    navigate_to(stage_num)
                    st.rerun()


def main():
    st.set_page_config(
        page_title="Cybersecurity Decision-Point Elicitation and Examination Tool",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_custom_css()
    init_session_state()

    # Sidebar
    render_sidebar()

    # Main header
    st.markdown(
        "<div style='text-align:center;'>"
        "<h1 style='color:#60a5fa;'>Cybersecurity Decision-Point Elicitation and Examination Tool</h1>"
        "</div>",
        unsafe_allow_html=True,
    )
    render_divider()

    render_progress_bar()
    render_divider()

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



if __name__ == "__main__":
    main()
