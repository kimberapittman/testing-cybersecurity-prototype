"""Stage 6: Documentation — compile and export the analytic record."""

import io
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)
from domain_data import (
    NIST_DOMAINS,
    PFCE_DOMAINS,
)


def _get_actions():
    return [
        (i, action)
        for i, action in enumerate(st.session_state.actions)
        if action.strip()
    ]


def _get_response_text(action_idx, domain_key, domain_type):
    """Get consolidated response text for an action+domain pair."""
    action_key = str(action_idx)
    same_as = st.session_state.tier2_same_as.get(action_key, {}).get(domain_key)
    if same_as is not None:
        action_key = str(same_as)

    responses = st.session_state.tier2_responses.get(action_key, {}).get(
        domain_key, {}
    )

    # Under new structure, all patterns stored under key "0"
    composite = responses.get("0", "").strip()

    if composite == "N/A":
        return "  N/A"
    elif composite:
        patterns = [p.strip() for p in composite.split("|") if p.strip()]
        lines = [f"  - {p}" for p in patterns]
        return "\n".join(lines)
    else:
        return "  (No considerations selected)"


def _compile_record():
    """Compile the full analytic record as structured text."""
    sections = []

    # ── Stage 1: Decision Point ──
    sections.append("=" * 60)
    sections.append("DECISION-POINT SPECIFICATION")
    sections.append("=" * 60)
    sections.append(f"Decision: {st.session_state.decision_description}")
    sections.append(f"Responsible Actor: {st.session_state.responsible_actor}")

    # ── Stage 2: Constraints ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("CONSTRAINT DECLARATION")
    sections.append("=" * 60)
    constraints = st.session_state.constraints
    if constraints:
        for key, data in constraints.items():
            label = data.get("label", key)
            spec = data.get("specification", "").strip()
            sections.append(f"{label}: {spec if spec else '(No specification)'}")
    else:
        sections.append("(No constraints declared)")

    # ── Stage 3: Actions ──
    actions = _get_actions()
    sections.append("")
    sections.append("=" * 60)
    sections.append("DECLARED ACTIONS")
    sections.append("=" * 60)
    for action_idx, action_text in actions:
        sections.append(f"Action {action_idx + 1}: {action_text}")

    # ── Stage 4: Domain Activations ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("DOMAIN ACTIVATIONS (Tier 1)")
    sections.append("=" * 60)
    sections.append(
        f"NIST CSF Domains: {', '.join(st.session_state.selected_nist_domains)}"
    )
    sections.append(
        f"PFCE Domains: {', '.join(st.session_state.selected_pfce_domains)}"
    )

    # ── Stage 5: Consolidated Consideration Profiles ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("CONSOLIDATED CONSIDERATION PROFILES")
    sections.append("=" * 60)
    for action_idx, action_text in actions:
        sections.append(f"\nAction {action_idx + 1}: {action_text}")
        sections.append("-" * 40)

        sections.append("  Technical Considerations (NIST CSF):")
        for domain_key in st.session_state.selected_nist_domains:
            sections.append(f"    {domain_key}:")
            sections.append(
                _get_response_text(action_idx, domain_key, "nist")
            )
        if not st.session_state.selected_nist_domains:
            sections.append("    (No technical domains activated)")

        sections.append("  Ethical Considerations (PFCE):")
        for domain_key in st.session_state.selected_pfce_domains:
            sections.append(f"    {domain_key}:")
            sections.append(
                _get_response_text(action_idx, domain_key, "pfce")
            )
        if not st.session_state.selected_pfce_domains:
            sections.append("    (No ethical domains activated)")

    # ── Stage 5: Cross-Action Comparison ──
    if len(actions) >= 2:
        sections.append("")
        sections.append("=" * 60)
        sections.append("CROSS-ACTION COMPARISON")
        sections.append("=" * 60)

        if st.session_state.selected_nist_domains:
            sections.append("\n  Technical Considerations (NIST CSF):")
            for domain_key in st.session_state.selected_nist_domains:
                sections.append(f"\n    {domain_key}:")
                for action_idx, action_text in actions:
                    sections.append(f"      Action {action_idx + 1}:")
                    sections.append(
                        _get_response_text(action_idx, domain_key, "nist")
                    )

        if st.session_state.selected_pfce_domains:
            sections.append("\n  Ethical Considerations (PFCE):")
            for domain_key in st.session_state.selected_pfce_domains:
                sections.append(f"\n    {domain_key}:")
                for action_idx, action_text in actions:
                    sections.append(f"      Action {action_idx + 1}:")
                    sections.append(
                        _get_response_text(action_idx, domain_key, "pfce")
                    )

    return "\n".join(sections)


def _escape_xml(text: str) -> str:
    """Escape text for use in reportlab Paragraph XML."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _generate_pdf(record_text: str) -> bytes:
    """Generate a PDF from the compiled record text using reportlab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=16,
        spaceAfter=6,
        textColor=HexColor("#1a1a1a"),
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=4,
        textColor=HexColor("#1e40af"),
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        spaceAfter=3,
    )
    sub_style = ParagraphStyle(
        "CustomSub",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        textColor=HexColor("#666666"),
        spaceAfter=2,
    )

    story = []
    story.append(Paragraph("Cybersecurity Decision-Support Record", title_style))
    story.append(
        Paragraph(
            "Generated from session data &mdash; no persistent storage",
            sub_style,
        )
    )
    story.append(Spacer(1, 12))

    for line in record_text.split("\n"):
        if line.startswith("=" * 20):
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=1,
                    color=HexColor("#333333"),
                    spaceAfter=4,
                    spaceBefore=8,
                )
            )
        elif line.isupper() and len(line) > 5 and ":" not in line:
            story.append(Paragraph(_escape_xml(line), heading_style))
        elif line.startswith("-" * 10):
            story.append(
                HRFlowable(
                    width="90%",
                    thickness=0.5,
                    color=HexColor("#cccccc"),
                    spaceAfter=3,
                    spaceBefore=3,
                )
            )
        elif line.strip():
            story.append(Paragraph(_escape_xml(line), body_style))
        else:
            story.append(Spacer(1, 6))

    doc.build(story)
    return buffer.getvalue()


def _render_compiled_record(record_text: str):
    """Display the compiled record for practitioner review."""
    actions = _get_actions()

    # Stage 1
    st.subheader("Decision-Point Specification")
    st.markdown(f"**Decision:** {st.session_state.decision_description}")
    st.markdown(f"**Responsible Actor:** {st.session_state.responsible_actor}")

    # Stage 2
    st.subheader("Constraint Declaration")
    constraints = st.session_state.constraints
    if constraints:
        for key, data in constraints.items():
            label = data.get("label", key)
            spec = data.get("specification", "").strip()
            if spec:
                st.markdown(f"**{label}:** {spec}")
    else:
        st.markdown("*(No constraints declared)*")

    # Stage 3
    st.subheader("Declared Actions")
    for action_idx, action_text in actions:
        st.markdown(f"**Action {action_idx + 1}:** {action_text}")

    # Stage 4 — Domain Activations
    st.subheader("Domain Activations")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="section-header-tech">NIST CSF Domains</div>',
            unsafe_allow_html=True,
        )
        for d in st.session_state.selected_nist_domains:
            st.markdown(f"- {d}")
    with col2:
        st.markdown(
            '<div class="section-header-eth">PFCE Domains</div>',
            unsafe_allow_html=True,
        )
        for d in st.session_state.selected_pfce_domains:
            st.markdown(f"- {d}")

    # Stage 5 — Consolidated Consideration Profiles
    st.subheader("Consolidated Consideration Profiles")
    for action_idx, action_text in actions:
        with st.expander(
            f"Action {action_idx + 1}: {action_text[:80]}...", expanded=True
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    '<div class="section-header-tech">Technical (NIST CSF)</div>',
                    unsafe_allow_html=True,
                )
                for domain_key in st.session_state.selected_nist_domains:
                    st.markdown(f"**{domain_key}:**")
                    text = _get_response_text(action_idx, domain_key, "nist")
                    st.markdown(text)
                if not st.session_state.selected_nist_domains:
                    st.markdown("*(No technical domains activated)*")
            with col2:
                st.markdown(
                    '<div class="section-header-eth">Ethical (PFCE)</div>',
                    unsafe_allow_html=True,
                )
                for domain_key in st.session_state.selected_pfce_domains:
                    st.markdown(f"**{domain_key}:**")
                    text = _get_response_text(action_idx, domain_key, "pfce")
                    st.markdown(text)
                if not st.session_state.selected_pfce_domains:
                    st.markdown("*(No ethical domains activated)*")

    # Cross-action comparison
    if len(actions) >= 2:
        st.subheader("Cross-Action Comparison")
        if st.session_state.selected_nist_domains:
            st.markdown(
                '<div class="section-header-tech">Technical (NIST CSF)</div>',
                unsafe_allow_html=True,
            )
            for domain_key in st.session_state.selected_nist_domains:
                st.markdown(f"**{domain_key}**")
                cols = st.columns(len(actions))
                for col, (action_idx, action_text) in zip(cols, actions):
                    with col:
                        st.markdown(f"*Action {action_idx + 1}*")
                        st.markdown(
                            _get_response_text(action_idx, domain_key, "nist")
                        )

        if st.session_state.selected_pfce_domains:
            st.markdown(
                '<div class="section-header-eth">Ethical (PFCE)</div>',
                unsafe_allow_html=True,
            )
            for domain_key in st.session_state.selected_pfce_domains:
                st.markdown(f"**{domain_key}**")
                cols = st.columns(len(actions))
                for col, (action_idx, action_text) in zip(cols, actions):
                    with col:
                        st.markdown(f"*Action {action_idx + 1}*")
                        st.markdown(
                            _get_response_text(action_idx, domain_key, "pfce")
                        )


def render_stage6():
    """Documentation stage — review and export."""
    st.header("Stage 6: Documentation")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Identify the responsible actor, review the "
        "complete analytic record, and export as PDF."
        "</div>",
        unsafe_allow_html=True,
    )

    # Responsible actor input
    st.subheader("Responsible Actor")
    st.session_state.responsible_actor = st.text_area(
        "Responsible actor",
        value=st.session_state.responsible_actor,
        placeholder="Who has authority to make this decision?",
        help="Identify the person or role with decision authority.",
        key="input_responsible_actor",
    )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    st.markdown("## Analytic Record")

    # Compile record
    record_text = _compile_record()

    # Display compiled record
    _render_compiled_record(record_text)

    # Export
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
    st.markdown("## Export")

    pdf_bytes = _generate_pdf(record_text)
    st.download_button(
        label="Download Complete Record as PDF",
        data=pdf_bytes,
        file_name="cybersecurity_decision_record.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True,
    )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
    if st.button(
        "Start New Analysis",
        use_container_width=True,
        help="This will clear all session data and start fresh.",
    ):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
