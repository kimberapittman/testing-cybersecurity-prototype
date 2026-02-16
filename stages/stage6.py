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
    RELATIONSHIP_COLORS,
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

    domain_defs = NIST_DOMAINS if domain_type == "nist" else PFCE_DOMAINS
    responses = st.session_state.tier2_responses.get(action_key, {}).get(
        domain_key, {}
    )
    prompts = domain_defs[domain_key]["prompts"]

    lines = []
    for p_idx, prompt_text in enumerate(prompts):
        val = responses.get(str(p_idx), "").strip()
        if val:
            lines.append(f"  - {prompt_text}\n    {val}")
    return "\n".join(lines) if lines else "  (No response)"


def _compile_record():
    """Compile the full analytic record as structured text."""
    sections = []

    # ── Stage 1: Decision Point ──
    sections.append("=" * 60)
    sections.append("DECISION-POINT SPECIFICATION")
    sections.append("=" * 60)
    sections.append(f"Decision: {st.session_state.decision_description}")
    sections.append(f"Responsible Actor: {st.session_state.responsible_actor}")
    sections.append(f"Scope of Authority: {st.session_state.scope_of_authority}")
    sections.append(f"Why Deferral Not Feasible: {st.session_state.why_no_deferral}")

    # ── Stage 2: Constraints ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("CONSTRAINT DECLARATION")
    sections.append("=" * 60)
    constraint_fields = [
        ("Institutional", st.session_state.institutional_constraints),
        ("Governance", st.session_state.governance_constraints),
        ("Legal", st.session_state.legal_constraints),
        ("Temporal", st.session_state.temporal_constraints),
        ("Resource", st.session_state.resource_constraints),
    ]
    for label, val in constraint_fields:
        sections.append(f"{label}: {val if val.strip() else '(None declared)'}")

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

    # ── Stage 4: Technical Considerations ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("ELICITED TECHNICAL CONSIDERATIONS BY ACTION")
    sections.append("=" * 60)
    for action_idx, action_text in actions:
        sections.append(f"\nAction {action_idx + 1}: {action_text}")
        sections.append("-" * 40)
        for domain_key in st.session_state.selected_nist_domains:
            same_as = st.session_state.tier2_same_as.get(
                str(action_idx), {}
            ).get(domain_key)
            if same_as is not None:
                sections.append(
                    f"  {domain_key}: Same as Action {same_as + 1}"
                )
            else:
                sections.append(f"  {domain_key}:")
                sections.append(
                    _get_response_text(action_idx, domain_key, "nist")
                )

    # ── Stage 4: Ethical Considerations ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("ELICITED ETHICAL CONSIDERATIONS BY ACTION")
    sections.append("=" * 60)
    for action_idx, action_text in actions:
        sections.append(f"\nAction {action_idx + 1}: {action_text}")
        sections.append("-" * 40)
        for domain_key in st.session_state.selected_pfce_domains:
            same_as = st.session_state.tier2_same_as.get(
                str(action_idx), {}
            ).get(domain_key)
            if same_as is not None:
                sections.append(
                    f"  {domain_key}: Same as Action {same_as + 1}"
                )
            else:
                sections.append(f"  {domain_key}:")
                sections.append(
                    _get_response_text(action_idx, domain_key, "pfce")
                )

    # ── Stage 5: Interaction Examination ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("INTERACTION EXAMINATION RESULTS BY ACTION")
    sections.append("=" * 60)
    for action_idx, action_text in actions:
        action_key = str(action_idx)
        matrix = st.session_state.interaction_matrix.get(action_key, {})
        sections.append(f"\nAction {action_idx + 1}: {action_text}")
        sections.append("-" * 40)

        for tech_domain in st.session_state.selected_nist_domains:
            for eth_domain in st.session_state.selected_pfce_domains:
                cell_key = f"{tech_domain}|{eth_domain}"
                cell = matrix.get(cell_key, {})
                rel = cell.get("relationship", "Not specified")
                sections.append(f"  {tech_domain} x {eth_domain}: {rel}")

                if cell.get("explanation", "").strip():
                    sections.append(
                        f"    Explanation: {cell['explanation']}"
                    )
                if rel in ("Tension", "Conflict"):
                    sections.append(
                        f"    Foregone: {cell.get('foregone', '')}"
                    )
                    sections.append(
                        f"    Consequences: {cell.get('consequences', '')}"
                    )

    # ── Stage 5: Cross-Action Comparison ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("CROSS-ACTION COMPARISON SUMMARY")
    sections.append("=" * 60)
    all_domains = (
        [(d, "nist") for d in st.session_state.selected_nist_domains]
        + [(d, "pfce") for d in st.session_state.selected_pfce_domains]
    )
    for domain_key, domain_type in all_domains:
        framework = "NIST CSF" if domain_type == "nist" else "PFCE"
        sections.append(f"\n{domain_key} ({framework}):")
        for action_idx, action_text in actions:
            sections.append(f"  Action {action_idx + 1}:")
            sections.append(
                _get_response_text(action_idx, domain_key, domain_type)
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
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Decision:** {st.session_state.decision_description}")
        st.markdown(f"**Responsible Actor:** {st.session_state.responsible_actor}")
    with col2:
        st.markdown(f"**Scope of Authority:** {st.session_state.scope_of_authority}")
        st.markdown(f"**Why Deferral Not Feasible:** {st.session_state.why_no_deferral}")

    # Stage 2
    st.subheader("Constraint Declaration")
    constraint_fields = [
        ("Institutional", st.session_state.institutional_constraints),
        ("Governance", st.session_state.governance_constraints),
        ("Legal", st.session_state.legal_constraints),
        ("Temporal", st.session_state.temporal_constraints),
        ("Resource", st.session_state.resource_constraints),
    ]
    for label, val in constraint_fields:
        if val.strip():
            st.markdown(f"**{label}:** {val}")
        else:
            st.markdown(f"**{label}:** *(None declared)*")

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

    # Stage 4 — Considerations by action
    st.subheader("Elicited Considerations by Action")
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
                    same_as = st.session_state.tier2_same_as.get(
                        str(action_idx), {}
                    ).get(domain_key)
                    if same_as is not None:
                        st.markdown(
                            f"**{domain_key}:** *Same as Action {same_as + 1}*"
                        )
                    else:
                        st.markdown(f"**{domain_key}:**")
                        text = _get_response_text(action_idx, domain_key, "nist")
                        st.markdown(text)
            with col2:
                st.markdown(
                    '<div class="section-header-eth">Ethical (PFCE)</div>',
                    unsafe_allow_html=True,
                )
                for domain_key in st.session_state.selected_pfce_domains:
                    same_as = st.session_state.tier2_same_as.get(
                        str(action_idx), {}
                    ).get(domain_key)
                    if same_as is not None:
                        st.markdown(
                            f"**{domain_key}:** *Same as Action {same_as + 1}*"
                        )
                    else:
                        st.markdown(f"**{domain_key}:**")
                        text = _get_response_text(action_idx, domain_key, "pfce")
                        st.markdown(text)

    # Stage 5 — Interaction Results
    st.subheader("Interaction Examination Results")
    for action_idx, action_text in actions:
        action_key = str(action_idx)
        matrix = st.session_state.interaction_matrix.get(action_key, {})
        with st.expander(
            f"Action {action_idx + 1}: {action_text[:80]}...", expanded=True
        ):
            for tech_domain in st.session_state.selected_nist_domains:
                for eth_domain in st.session_state.selected_pfce_domains:
                    cell_key = f"{tech_domain}|{eth_domain}"
                    cell = matrix.get(cell_key, {})
                    rel = cell.get("relationship", "Not specified")

                    css_class = RELATIONSHIP_COLORS.get(rel, "rel-na")

                    content = f"<strong>{tech_domain} x {eth_domain}:</strong> {rel}"
                    if cell.get("explanation", "").strip():
                        content += f"<br><em>Explanation:</em> {cell['explanation']}"
                    if rel in ("Tension", "Conflict"):
                        content += (
                            f"<br><em>Foregone:</em> {cell.get('foregone', '')}"
                        )
                        content += (
                            f"<br><em>Consequences:</em> "
                            f"{cell.get('consequences', '')}"
                        )

                    st.markdown(
                        f'<div class="{css_class}">{content}</div>',
                        unsafe_allow_html=True,
                    )

    # Cross-action comparison
    st.subheader("Cross-Action Comparison Summary")
    all_domains = (
        [(d, "nist") for d in st.session_state.selected_nist_domains]
        + [(d, "pfce") for d in st.session_state.selected_pfce_domains]
    )
    for domain_key, domain_type in all_domains:
        framework = "NIST CSF" if domain_type == "nist" else "PFCE"
        header_class = (
            "section-header-tech" if domain_type == "nist" else "section-header-eth"
        )
        st.markdown(
            f'<div class="{header_class}">{domain_key} ({framework})</div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(len(actions))
        for col, (action_idx, action_text) in zip(cols, actions):
            with col:
                st.markdown(f"**Action {action_idx + 1}**")
                text = _get_response_text(action_idx, domain_key, domain_type)
                st.markdown(text)


def render_stage6():
    """Documentation stage — review and export."""
    st.header("Stage 6: Documentation")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Review the complete analytic record and "
        "export as PDF. No new input is required at this stage."
        "</div>",
        unsafe_allow_html=True,
    )

    st.warning(
        "This is a review-only stage. The record below was compiled from "
        "all prior stages. Export as PDF to preserve your analysis."
    )

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
