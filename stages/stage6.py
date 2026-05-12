"""Stage 6: Documentation — document observations, reasoning, and export."""

import io
from datetime import datetime
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
    PageBreak,
)
from domain_data import (
    NIST_DOMAINS,
    PFCE_DOMAINS,
)

PFCE_DISPLAY_ORDER = ["BENEFICENCE", "NON-MALEFICENCE", "AUTONOMY", "JUSTICE", "EXPLICABILITY"]
NIST_DISPLAY_ORDER = ["GOVERN", "IDENTIFY", "PROTECT", "DETECT", "RESPOND", "RECOVER"]


def _get_actions():
    return [
        (i, action)
        for i, action in enumerate(st.session_state.actions)
        if action.strip()
    ]


def _get_consideration_text(action_idx, domain_key):
    """Get consideration text for an action+domain pair. Returns None if N/A or empty."""
    action_key = str(action_idx)

    responses = st.session_state.tier2_responses.get(action_key, {}).get(
        domain_key, {}
    )
    data = responses.get("0", {})

    if isinstance(data, str):
        if not data.strip() or data.strip() == "N/A":
            return None
        patterns = [p.strip() for p in data.split("|") if p.strip()]
        return "\n".join(f"- {p}" for p in patterns)

    if data.get("na", False):
        return None

    text = data.get("text", "").strip()
    patterns = data.get("patterns", [])

    if not text and not patterns:
        return None

    parts = []
    if text:
        parts.append(text)
    if patterns:
        for p in patterns:
            parts.append(f"- {p}")

    return "\n".join(parts)


def _get_response_text_for_record(action_idx, domain_key):
    """Get consideration text formatted for the text-based compiled record."""
    action_key = str(action_idx)

    responses = st.session_state.tier2_responses.get(action_key, {}).get(
        domain_key, {}
    )
    data = responses.get("0", {})

    if isinstance(data, str):
        if data.strip() == "N/A":
            return "      N/A"
        elif data.strip():
            patterns = [p.strip() for p in data.split("|") if p.strip()]
            return "\n".join(f"      - {p}" for p in patterns)
        else:
            return "      (No considerations selected)"

    if data.get("na", False):
        return "      N/A"

    text = data.get("text", "").strip()
    patterns = data.get("patterns", [])

    if not text and not patterns:
        return "      (No considerations selected)"

    lines = []
    if text:
        for line in text.split("\n"):
            lines.append(f"      {line}")
    if patterns:
        for p in patterns:
            lines.append(f"      - {p}")

    return "\n".join(lines)


def _compile_record():
    """Compile the full documented record as structured text for PDF export."""
    sections = []

    # ── Decision Point ──
    sections.append("=" * 60)
    sections.append("DECISION-POINT SPECIFICATION")
    sections.append("=" * 60)
    sections.append(f"Decision: {st.session_state.decision_description}")
    actor = st.session_state.responsible_actor.strip()
    if actor:
        sections.append(f"Decision-maker: {actor}")

    # ── Constraints ──
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

    # ── Actions ──
    actions = _get_actions()
    sections.append("")
    sections.append("=" * 60)
    sections.append("DECLARED ACTIONS")
    sections.append("=" * 60)
    for action_idx, action_text in actions:
        sections.append(f"Action {action_idx + 1}: {action_text}")

    # ── Considerations by Action ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("CONSIDERATIONS BY ACTION")
    sections.append("=" * 60)
    for action_idx, action_text in actions:
        sections.append(f"\nAction {action_idx + 1}: {action_text}")
        sections.append("-" * 40)

        sections.append("  Ethical Considerations (PFCE):")
        has_pfce = False
        for domain_key in PFCE_DISPLAY_ORDER:
            if domain_key not in st.session_state.selected_pfce_domains:
                continue
            text = _get_consideration_text(action_idx, domain_key)
            if text is None:
                continue
            has_pfce = True
            sections.append(f"    {domain_key}:")
            sections.append(
                _get_response_text_for_record(action_idx, domain_key)
            )
        if not has_pfce:
            sections.append(
                "    No ethical considerations were identified for this action."
            )

        sections.append("  Technical Considerations (NIST CSF):")
        has_nist = False
        for domain_key in NIST_DISPLAY_ORDER:
            if domain_key not in st.session_state.selected_nist_domains:
                continue
            text = _get_consideration_text(action_idx, domain_key)
            if text is None:
                continue
            has_nist = True
            sections.append(f"    {domain_key}:")
            sections.append(
                _get_response_text_for_record(action_idx, domain_key)
            )
        if not has_nist:
            sections.append(
                "    No technical considerations were identified for this action."
            )

    # ── Observations ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("OBSERVATIONS")
    sections.append("=" * 60)
    obs = st.session_state.stage6_observations.strip()
    sections.append(obs if obs else "None documented")

    # ── Key Considerations ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("KEY CONSIDERATIONS")
    sections.append("=" * 60)
    key_cons = st.session_state.stage6_key_considerations.strip()
    sections.append(key_cons if key_cons else "None documented")

    # ── Decision Reasoning ──
    sections.append("")
    sections.append("=" * 60)
    sections.append("DECISION REASONING")
    sections.append("=" * 60)
    reasoning = st.session_state.stage6_reasoning.strip()
    sections.append(reasoning if reasoning else "None documented")

    return "\n".join(sections)


def _escape_xml(text: str) -> str:
    """Escape text for use in reportlab Paragraph XML."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _build_decision_brief_story(styles_dict, date_str: str) -> list:
    """Build the Decision Brief flowables — appears as the lead page of the PDF."""
    brief = []

    brief.append(Paragraph("Decision Brief", styles_dict["brief_title"]))
    brief.append(
        Paragraph(
            f"Documented record generated {_escape_xml(date_str)}",
            styles_dict["brief_sub"],
        )
    )
    brief.append(Spacer(1, 14))

    brief.append(Paragraph("Decision Point", styles_dict["brief_heading"]))
    decision = st.session_state.decision_description.strip() or "(not specified)"
    brief.append(Paragraph(_escape_xml(decision), styles_dict["brief_body"]))
    brief.append(Spacer(1, 10))

    actor = st.session_state.responsible_actor.strip()
    if actor:
        brief.append(Paragraph("Decision-Maker", styles_dict["brief_heading"]))
        brief.append(Paragraph(_escape_xml(actor), styles_dict["brief_body"]))
        brief.append(Spacer(1, 10))

    brief.append(Paragraph("Key Considerations", styles_dict["brief_heading"]))
    key_cons = st.session_state.stage6_key_considerations.strip()
    if key_cons:
        for para in key_cons.split("\n"):
            if para.strip():
                brief.append(
                    Paragraph(_escape_xml(para), styles_dict["brief_body"])
                )
    else:
        brief.append(
            Paragraph("<i>Not documented.</i>", styles_dict["brief_body_muted"])
        )
    brief.append(Spacer(1, 10))

    brief.append(Paragraph("Decision Reasoning", styles_dict["brief_heading"]))
    reasoning = st.session_state.stage6_reasoning.strip()
    if reasoning:
        for para in reasoning.split("\n"):
            if para.strip():
                brief.append(
                    Paragraph(_escape_xml(para), styles_dict["brief_body"])
                )
    else:
        brief.append(
            Paragraph("<i>Not documented.</i>", styles_dict["brief_body_muted"])
        )
    brief.append(Spacer(1, 10))

    brief.append(Paragraph("Observations", styles_dict["brief_heading"]))
    obs = st.session_state.stage6_observations.strip()
    if obs:
        for para in obs.split("\n"):
            if para.strip():
                brief.append(
                    Paragraph(_escape_xml(para), styles_dict["brief_body"])
                )
    else:
        brief.append(
            Paragraph("<i>Not documented.</i>", styles_dict["brief_body_muted"])
        )
    brief.append(Spacer(1, 14))

    brief.append(
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=HexColor("#999999"),
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    brief.append(
        Paragraph(
            "The complete six-stage analytic record follows on the next page. "
            "The record documents the decision point, constraints declared, "
            "actions considered, and the full set of ethical and technical "
            "considerations elicited at each stage.",
            styles_dict["brief_pointer"],
        )
    )

    brief.append(PageBreak())
    return brief


def _generate_pdf(record_text: str) -> bytes:
    """Generate a PDF with a Decision Brief lead page followed by the analytic record."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    base_styles = getSampleStyleSheet()

    # Decision Brief styles
    brief_styles = {
        "brief_title": ParagraphStyle(
            "BriefTitle",
            parent=base_styles["Title"],
            fontSize=20,
            spaceAfter=2,
            textColor=HexColor("#1a1a1a"),
        ),
        "brief_sub": ParagraphStyle(
            "BriefSub",
            parent=base_styles["Normal"],
            fontSize=9,
            leading=11,
            textColor=HexColor("#666666"),
            spaceAfter=4,
        ),
        "brief_heading": ParagraphStyle(
            "BriefHeading",
            parent=base_styles["Heading2"],
            fontSize=12,
            spaceBefore=6,
            spaceAfter=4,
            textColor=HexColor("#1e40af"),
        ),
        "brief_body": ParagraphStyle(
            "BriefBody",
            parent=base_styles["Normal"],
            fontSize=10,
            leading=13,
            spaceAfter=4,
        ),
        "brief_body_muted": ParagraphStyle(
            "BriefBodyMuted",
            parent=base_styles["Normal"],
            fontSize=10,
            leading=13,
            textColor=HexColor("#888888"),
            spaceAfter=4,
        ),
        "brief_pointer": ParagraphStyle(
            "BriefPointer",
            parent=base_styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=HexColor("#555555"),
            spaceAfter=2,
        ),
    }

    # Analytic record styles
    record_title_style = ParagraphStyle(
        "CustomTitle",
        parent=base_styles["Title"],
        fontSize=16,
        spaceAfter=6,
        textColor=HexColor("#1a1a1a"),
    )
    record_heading_style = ParagraphStyle(
        "CustomHeading",
        parent=base_styles["Heading2"],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=4,
        textColor=HexColor("#1e40af"),
    )
    record_body_style = ParagraphStyle(
        "CustomBody",
        parent=base_styles["Normal"],
        fontSize=9,
        leading=12,
        spaceAfter=3,
    )
    record_sub_style = ParagraphStyle(
        "CustomSub",
        parent=base_styles["Normal"],
        fontSize=8,
        leading=10,
        textColor=HexColor("#666666"),
        spaceAfter=2,
    )

    date_str = datetime.now().strftime("%B %d, %Y")

    story = []

    # 1. Decision Brief (lead page)
    story.extend(_build_decision_brief_story(brief_styles, date_str))

    # 2. Analytic Record (following pages)
    story.append(Paragraph("Analytic Record", record_title_style))
    story.append(
        Paragraph(
            "Complete six-stage record of the elicitation and integration "
            "sequence.",
            record_sub_style,
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
            story.append(Paragraph(_escape_xml(line), record_heading_style))
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
            story.append(Paragraph(_escape_xml(line), record_body_style))
        else:
            story.append(Spacer(1, 6))

    doc.build(story)
    return buffer.getvalue()


def _render_record_summary():
    """Render the collapsible read-only record summary."""
    actions = _get_actions()

    # Decision Point
    st.subheader("Decision Point")
    st.markdown(f"{st.session_state.decision_description}")
    actor = st.session_state.responsible_actor.strip()
    if actor:
        st.markdown(f"**Decision-maker:** {actor}")

    # Constraints
    st.subheader("Constraints")
    constraints = st.session_state.constraints
    if constraints:
        for key, data in constraints.items():
            label = data.get("label", key)
            spec = data.get("specification", "").strip()
            if spec:
                st.markdown(f"**{label}:** {spec}")
            else:
                st.markdown(f"**{label}**")
    else:
        st.markdown("*(No constraints declared)*")

    # Declared Actions
    st.subheader("Declared Actions")
    for action_idx, action_text in actions:
        st.markdown(f"{action_idx + 1}. {action_text}")

    # Considerations by action
    st.subheader("Considerations by Action")
    for action_idx, action_text in actions:
        st.markdown(f"**Action {action_idx + 1}: {action_text}**")

        col_eth, col_tech = st.columns(2)

        with col_eth:
            st.markdown(
                '<div class="section-header-eth">'
                "Ethical Considerations (PFCE)</div>",
                unsafe_allow_html=True,
            )
            has_pfce = False
            for domain_key in PFCE_DISPLAY_ORDER:
                if domain_key not in st.session_state.selected_pfce_domains:
                    continue
                text = _get_consideration_text(action_idx, domain_key)
                if text is None:
                    continue
                has_pfce = True
                st.markdown(f"**{domain_key}**")
                st.markdown(text)
            if not has_pfce:
                st.markdown(
                    "No ethical considerations were identified for this action."
                )

        with col_tech:
            st.markdown(
                '<div class="section-header-tech">'
                "Technical Considerations (NIST CSF)</div>",
                unsafe_allow_html=True,
            )
            has_nist = False
            for domain_key in NIST_DISPLAY_ORDER:
                if domain_key not in st.session_state.selected_nist_domains:
                    continue
                text = _get_consideration_text(action_idx, domain_key)
                if text is None:
                    continue
                has_nist = True
                st.markdown(f"**{domain_key}**")
                st.markdown(text)
            if not has_nist:
                st.markdown(
                    "No technical considerations were identified for this action."
                )

        st.divider()

    # Observations
    st.subheader("Observations")
    obs = st.session_state.stage6_observations.strip()
    st.markdown(obs if obs else "*None documented*")

    # Key Considerations
    st.subheader("Key Considerations")
    key_cons = st.session_state.stage6_key_considerations.strip()
    st.markdown(key_cons if key_cons else "*None documented*")

    # Decision Reasoning
    st.subheader("Decision Reasoning")
    reasoning = st.session_state.stage6_reasoning.strip()
    st.markdown(reasoning if reasoning else "*None documented*")


def render_stage6():
    """Documentation stage — observations, reasoning, review, and export."""
    st.header("Stage 6: Documentation")
    st.markdown(
        '<div class="stage-purpose">'
        "<strong>Purpose:</strong> Document your observations from the "
        "consideration review and your reasoning below."
        "</div>",
        unsafe_allow_html=True,
    )

    # Text Area 1: Observations
    st.session_state.stage6_observations = st.text_area(
        "Having reviewed your ethical and technical considerations together, "
        "describe any observations about how these considerations relate to "
        "each other or to your decision.",
        value=st.session_state.stage6_observations,
        height=180,
        help=(
            "For example, did you notice any tensions between ethical and "
            "technical considerations? Did considerations under different "
            "domains reinforce each other? Were there surprises?"
        ),
        key="input_stage6_observations",
    )

    # Text Area 2: Key Considerations
    st.session_state.stage6_key_considerations = st.text_area(
        "Of the considerations you reviewed, which two or three "
        "weighed most heavily in your thinking?",
        value=st.session_state.stage6_key_considerations,
        height=150,
        help=(
            "You are not ranking all considerations. Identify only "
            "those that felt most significant to your decision and "
            "briefly explain why."
        ),
        key="input_stage6_key_considerations",
    )

    # Text Area 3: Decision Reasoning
    st.session_state.stage6_reasoning = st.text_area(
        "Based on your review of all considerations, document your reasoning "
        "for the action you are recommending or selecting.",
        value=st.session_state.stage6_reasoning,
        height=180,
        help=(
            "Record what considerations weighed most heavily and what "
            "tradeoffs you are accepting."
        ),
        key="input_stage6_reasoning",
    )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # Collapsible record summary
    with st.expander("Review Complete Record Before Export", expanded=False):
        _render_record_summary()

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # Export
    record_text = _compile_record()
    pdf_bytes = _generate_pdf(record_text)
    st.download_button(
        label="Export Documented Record",
        data=pdf_bytes,
        file_name="documented_record.pdf",
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
