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
    Table,
    TableStyle,
    KeepTogether,
)


# ────────────────────────────────────────────────────────────────────
# CONSTANTS
# ────────────────────────────────────────────────────────────────────

PFCE_DISPLAY_ORDER = [
    "BENEFICENCE", "NON-MALEFICENCE", "AUTONOMY", "JUSTICE", "EXPLICABILITY",
]
NIST_DISPLAY_ORDER = [
    "GOVERN", "IDENTIFY", "PROTECT", "DETECT", "RESPOND", "RECOVER",
]

# Title-case names for display in the PDF.
DOMAIN_DISPLAY_NAMES = {
    "BENEFICENCE": "Beneficence",
    "NON-MALEFICENCE": "Non-Maleficence",
    "AUTONOMY": "Autonomy",
    "JUSTICE": "Justice",
    "EXPLICABILITY": "Explicability",
    "GOVERN": "Govern",
    "IDENTIFY": "Identify",
    "PROTECT": "Protect",
    "DETECT": "Detect",
    "RESPOND": "Respond",
    "RECOVER": "Recover",
}


# ────────────────────────────────────────────────────────────────────
# HELPERS
# ────────────────────────────────────────────────────────────────────

def _get_actions():
    """Return a list of (index, text) tuples for non-empty actions."""
    return [
        (i, action)
        for i, action in enumerate(st.session_state.actions)
        if action.strip()
    ]


def _get_consideration_text(action_idx, domain_key):
    """Get consideration text for the in-app expander.

    Returns a single string with text and bullets merged, or None if the
    domain was marked N/A or has no content. Used by _render_record_summary.
    """
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


def _get_consideration_parts(action_idx, domain_key):
    """Get consideration text and patterns separately for the PDF.

    Returns a (text, patterns) tuple. Returns (None, None) if the domain
    was marked N/A or has no content. Used by the PDF builder so that text
    and bullets can be rendered with different paragraph styles.
    """
    action_key = str(action_idx)

    responses = st.session_state.tier2_responses.get(action_key, {}).get(
        domain_key, {}
    )
    data = responses.get("0", {})

    if isinstance(data, str):
        # Legacy string shape — treat as patterns
        if not data.strip() or data.strip() == "N/A":
            return None, None
        patterns = [p.strip() for p in data.split("|") if p.strip()]
        return "", patterns

    if data.get("na", False):
        return None, None

    text = data.get("text", "").strip()
    patterns = data.get("patterns", [])

    if not text and not patterns:
        return None, None

    return text, patterns


def _escape_xml(text):
    """Escape text for use in reportlab Paragraph XML."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# ────────────────────────────────────────────────────────────────────
# PDF: STYLES AND DECORATION
# ────────────────────────────────────────────────────────────────────

def _build_styles():
    """Build all paragraph styles used in the PDF."""
    base = getSampleStyleSheet()
    return {
        "doc_title": ParagraphStyle(
            "DocTitle", parent=base["Title"],
            fontSize=22, leading=26, spaceAfter=2,
            textColor=HexColor("#0f172a"),
        ),
        "doc_subtitle": ParagraphStyle(
            "DocSubtitle", parent=base["Normal"],
            fontSize=11, leading=14, textColor=HexColor("#475569"),
            spaceAfter=4,
        ),
        "section_h": ParagraphStyle(
            "SectionH", parent=base["Heading2"],
            fontSize=14, leading=18, spaceBefore=18, spaceAfter=8,
            textColor=HexColor("#1e40af"),
        ),
        "subsection_h": ParagraphStyle(
            "SubsectionH", parent=base["Heading3"],
            fontSize=12, leading=15, spaceBefore=10, spaceAfter=4,
            textColor=HexColor("#1e40af"),
            fontName="Helvetica-Bold",
        ),
        "action_h": ParagraphStyle(
            "ActionH", parent=base["Heading3"],
            fontSize=12, leading=15, spaceBefore=12, spaceAfter=4,
            textColor=HexColor("#0f172a"),
            fontName="Helvetica-Bold",
        ),
        "lens_h": ParagraphStyle(
            "LensH", parent=base["Heading4"],
            fontSize=11, leading=14, spaceBefore=0, spaceAfter=0,
            textColor=HexColor("#1e40af"),
            fontName="Helvetica-Bold",
            alignment=0,
        ),
        "domain_h": ParagraphStyle(
            "DomainH", parent=base["Normal"],
            fontSize=10, leading=13, spaceBefore=8, spaceAfter=2,
            textColor=HexColor("#0f172a"),
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"],
            fontSize=10, leading=14, spaceAfter=6,
        ),
        "body_muted": ParagraphStyle(
            "BodyMuted", parent=base["Normal"],
            fontSize=10, leading=14, textColor=HexColor("#94a3b8"),
            spaceAfter=6,
        ),
        "body_indented": ParagraphStyle(
            "BodyIndented", parent=base["Normal"],
            fontSize=10, leading=13, leftIndent=10, spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"],
            fontSize=10, leading=13, leftIndent=20, bulletIndent=10,
            spaceAfter=3,
        ),
        "framework_note": ParagraphStyle(
            "FrameworkNote", parent=base["Normal"],
            fontSize=9, leading=12, textColor=HexColor("#475569"),
            spaceAfter=4, leftIndent=10, rightIndent=10,
        ),
        "pointer": ParagraphStyle(
            "Pointer", parent=base["Normal"],
            fontSize=9, leading=12, textColor=HexColor("#64748b"),
            spaceAfter=2,
        ),
    }


def _draw_page_decoration(canvas, doc):
    """Draw the page number in the footer of every page."""
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#94a3b8"))
    canvas.drawCentredString(letter[0] / 2, 0.4 * inch, f"Page {doc.page}")
    canvas.restoreState()


def _section_divider():
    """A light horizontal rule placed above each numbered section heading."""
    return HRFlowable(
        width="100%", thickness=0.5, color=HexColor("#cbd5e1"),
        spaceBefore=18, spaceAfter=2,
    )


# ────────────────────────────────────────────────────────────────────
# PDF: SECTION BUILDERS
# ────────────────────────────────────────────────────────────────────

def _build_constraint_table(styles):
    """Build the constraint table for Section 2."""
    constraints = st.session_state.constraints
    if not constraints:
        return Paragraph(
            "<i>No constraints declared.</i>",
            styles["body_muted"],
        )

    data = [["Constraint Category", "Specification"]]
    for key, info in constraints.items():
        label = info.get("label", key)
        spec = info.get("specification", "").strip() or "(no specification provided)"
        data.append([
            Paragraph(f"<b>{_escape_xml(label)}</b>", styles["body"]),
            Paragraph(_escape_xml(spec), styles["body"]),
        ])

    table = Table(
        data,
        colWidths=[2.0 * inch, 4.3 * inch],
        repeatRows=1,
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1e40af")),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
            [HexColor("#ffffff"), HexColor("#f8fafc")]),
    ]))
    return table


def _build_action_block(action_idx, action_text, styles):
    """Build an action description block with a subtle highlighted background."""
    table = Table(
        [[Paragraph(
            f"<b>Action {action_idx + 1}.</b> {_escape_xml(action_text)}",
            styles["body"]
        )]],
        colWidths=[6.3 * inch],
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f1f5f9")),
        ("LINELEFT", (0, 0), (0, -1), 3, HexColor("#1e40af")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return table


def _build_domain_block(action_idx, framework, styles):
    """Build a list of flowables for one framework's domains for one action.

    Returns an empty list if no activated domains have content.
    """
    if framework == "pfce":
        order = PFCE_DISPLAY_ORDER
        selected = st.session_state.selected_pfce_domains
    else:
        order = NIST_DISPLAY_ORDER
        selected = st.session_state.selected_nist_domains

    items = []
    for domain_key in order:
        if domain_key not in selected:
            continue
        text, patterns = _get_consideration_parts(action_idx, domain_key)
        if text is None and patterns is None:
            continue

        items.append(Paragraph(
            DOMAIN_DISPLAY_NAMES.get(domain_key, domain_key.title()),
            styles["domain_h"]
        ))
        if text:
            items.append(Paragraph(
                _escape_xml(text), styles["body_indented"]
            ))
        if patterns:
            for p in patterns:
                items.append(Paragraph(
                    _escape_xml(p),
                    styles["bullet"],
                    bulletText="•",
                ))
    return items


def _build_action_considerations_table(action_idx, styles):
    """Build the 2-column considerations table for one action.

    Ethical (PFCE) on the left, technical (NIST CSF) on the right. Mirrors
    the Stage 5 prototype layout. Column header row identifies the lens;
    the content row holds the elicited considerations.
    """
    pfce_content = _build_domain_block(action_idx, "pfce", styles)
    nist_content = _build_domain_block(action_idx, "nist", styles)

    if not pfce_content:
        pfce_content = [Paragraph(
            "<i>No ethical considerations identified for this action.</i>",
            styles["body_muted"]
        )]
    if not nist_content:
        nist_content = [Paragraph(
            "<i>No technical considerations identified for this action.</i>",
            styles["body_muted"]
        )]

    data = [
        [
            Paragraph("Ethical Considerations (PFCE)", styles["lens_h"]),
            Paragraph("Technical Considerations (NIST CSF)", styles["lens_h"]),
        ],
        [pfce_content, nist_content],
    ]

    table = Table(
        data,
        colWidths=[3.15 * inch, 3.15 * inch],
        repeatRows=1,
    )
    table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#eff6ff")),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("LEFTPADDING", (0, 0), (-1, 0), 12),
        ("RIGHTPADDING", (0, 0), (-1, 0), 12),
        ("LINEBELOW", (0, 0), (-1, 0), 1, HexColor("#1e40af")),
        # Content row
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 1), (-1, 1), 10),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 10),
        ("LEFTPADDING", (0, 1), (-1, 1), 12),
        ("RIGHTPADDING", (0, 1), (-1, 1), 12),
        # Outer box and column divider
        ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ("LINEAFTER", (0, 0), (0, -1), 0.5, HexColor("#cbd5e1")),
    ]))
    return table


# ────────────────────────────────────────────────────────────────────
# PDF: BRIEF (page 1)
# ────────────────────────────────────────────────────────────────────

def _build_brief(styles, date_str):
    """Build the Decision Brief flowables (lead page of the PDF)."""
    items = []

    # Document header
    items.append(Paragraph("Documented Record", styles["doc_title"]))
    items.append(Paragraph(
        "Ethical and Technical Consideration Analysis for a Municipal Cybersecurity Decision",
        styles["doc_subtitle"]
    ))
    items.append(HRFlowable(
        width="100%", thickness=1.5, color=HexColor("#1e40af"),
        spaceBefore=4, spaceAfter=16,
    ))

    # Decision Brief heading
    items.append(Paragraph("Decision Brief", styles["section_h"]))
    items.append(Paragraph(
        f"Record generated {date_str}",
        styles["body_muted"]
    ))
    items.append(Spacer(1, 6))

    # Decision Point
    items.append(Paragraph("Decision Point", styles["subsection_h"]))
    decision = st.session_state.decision_description.strip() or "(not specified)"
    items.append(Paragraph(_escape_xml(decision), styles["body"]))

    # Decision-Maker (only if provided)
    actor = st.session_state.responsible_actor.strip()
    if actor:
        items.append(Paragraph("Decision-Maker", styles["subsection_h"]))
        items.append(Paragraph(_escape_xml(actor), styles["body"]))

    # Key Considerations
    items.append(Paragraph("Key Considerations", styles["subsection_h"]))
    key_cons = st.session_state.stage6_key_considerations.strip()
    if key_cons:
        for para in key_cons.split("\n"):
            if para.strip():
                items.append(Paragraph(
                    _escape_xml(para), styles["body"]
                ))
    else:
        items.append(Paragraph(
            "<i>Not documented.</i>", styles["body_muted"]
        ))

    # Decision Reasoning
    items.append(Paragraph("Decision Reasoning", styles["subsection_h"]))
    reasoning = st.session_state.stage6_reasoning.strip()
    if reasoning:
        for para in reasoning.split("\n"):
            if para.strip():
                items.append(Paragraph(
                    _escape_xml(para), styles["body"]
                ))
    else:
        items.append(Paragraph(
            "<i>Not documented.</i>", styles["body_muted"]
        ))

    # Observations
    items.append(Paragraph("Observations", styles["subsection_h"]))
    obs = st.session_state.stage6_observations.strip()
    if obs:
        for para in obs.split("\n"):
            if para.strip():
                items.append(Paragraph(
                    _escape_xml(para), styles["body"]
                ))
    else:
        items.append(Paragraph(
            "<i>Not documented.</i>", styles["body_muted"]
        ))

    # Pointer
    items.append(Spacer(1, 16))
    items.append(HRFlowable(
        width="100%", thickness=0.5, color=HexColor("#cbd5e1"),
        spaceBefore=4, spaceAfter=8,
    ))
    items.append(Paragraph(
        "The complete analytic record follows. It documents the decision "
        "point, the constraints shaping the decision environment, the "
        "actions considered, and the ethical and technical considerations "
        "elicited for each action.",
        styles["pointer"]
    ))

    return items


# ────────────────────────────────────────────────────────────────────
# PDF: RECORD (pages 2+)
# ────────────────────────────────────────────────────────────────────

def _build_record(styles):
    """Build the Analytic Record flowables (pages 2 onward)."""
    items = []

    # Title
    items.append(Paragraph("Analytic Record", styles["doc_title"]))
    items.append(Paragraph(
        "Six-stage record of the elicitation and integration sequence.",
        styles["doc_subtitle"]
    ))
    items.append(HRFlowable(
        width="100%", thickness=1.5, color=HexColor("#1e40af"),
        spaceBefore=4, spaceAfter=14,
    ))

    # Framework primer — explains PFCE and NIST CSF for the lay reader
    primer_table = Table(
        [[Paragraph(
            "<b>About this record.</b> This record was produced using a "
            "structured framework that applies two interpretive lenses to a "
            "cybersecurity decision: the <b>Principlist Framework for "
            "Cybersecurity Ethics (PFCE)</b>, which identifies ethical "
            "considerations across five principles (beneficence, "
            "non-maleficence, autonomy, justice, and explicability), and the "
            "<b>NIST Cybersecurity Framework 2.0</b>, which organizes "
            "technical considerations across six functions (govern, identify, "
            "protect, detect, respond, and recover). The two lenses are "
            "applied separately and presented together, making visible both "
            "the ethical and technical dimensions of the decision.",
            styles["framework_note"]
        )]],
        colWidths=[6.3 * inch],
    )
    primer_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#eff6ff")),
        ("LINELEFT", (0, 0), (0, -1), 3, HexColor("#1e40af")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    items.append(primer_table)

    # ── Section 1: Decision Point ──
    items.append(_section_divider())
    items.append(Paragraph("1. Decision Point", styles["section_h"]))
    decision = st.session_state.decision_description.strip() or "(not specified)"
    items.append(Paragraph(_escape_xml(decision), styles["body"]))
    actor = st.session_state.responsible_actor.strip()
    if actor:
        items.append(Paragraph(
            f"<b>Decision-Maker:</b> {_escape_xml(actor)}",
            styles["body"]
        ))

    # ── Section 2: Decision Environment ──
    items.append(_section_divider())
    items.append(Paragraph("2. Decision Environment", styles["section_h"]))
    items.append(Paragraph(
        "The following constraints define the decision environment within "
        "which feasible actions were identified.",
        styles["body"]
    ))
    items.append(Spacer(1, 4))
    items.append(_build_constraint_table(styles))

    # ── Section 3: Actions Considered ──
    actions = _get_actions()
    items.append(_section_divider())
    items.append(Paragraph("3. Actions Considered", styles["section_h"]))
    items.append(Paragraph(
        "The following actions were declared as feasible options at this "
        "decision point.",
        styles["body"]
    ))
    items.append(Spacer(1, 4))
    for action_idx, action_text in actions:
        items.append(_build_action_block(action_idx, action_text, styles))
        items.append(Spacer(1, 6))

    # ── Section 4: Considerations Analyzed ──
    items.append(_section_divider())
    items.append(Paragraph("4. Considerations Analyzed", styles["section_h"]))
    items.append(Paragraph(
        "For each declared action, the framework elicited considerations "
        "across the ethical principles (PFCE) and technical functions "
        "(NIST CSF) activated for this decision. The two lenses are "
        "presented side by side, making visible the integrated landscape "
        "for each action.",
        styles["body"]
    ))

    for action_idx, action_text in actions:
        # Wrap heading + table in KeepTogether so the action heading stays
        # with its table when content fits on a page. If a table is too
        # tall, reportlab will split it on its own.
        action_block = [
            Spacer(1, 10),
            Paragraph(
                f"Action {action_idx + 1}: {_escape_xml(action_text)}",
                styles["action_h"]
            ),
            Spacer(1, 4),
            _build_action_considerations_table(action_idx, styles),
        ]
        items.append(KeepTogether(action_block))

    # ── Section 5: Documentation ──
    items.append(_section_divider())
    items.append(Paragraph("5. Documentation", styles["section_h"]))

    items.append(Paragraph("Observations", styles["subsection_h"]))
    obs = st.session_state.stage6_observations.strip()
    if obs:
        for para in obs.split("\n"):
            if para.strip():
                items.append(Paragraph(
                    _escape_xml(para), styles["body"]
                ))
    else:
        items.append(Paragraph(
            "<i>Not documented.</i>", styles["body_muted"]
        ))

    items.append(Paragraph("Key Considerations", styles["subsection_h"]))
    key_cons = st.session_state.stage6_key_considerations.strip()
    if key_cons:
        for para in key_cons.split("\n"):
            if para.strip():
                items.append(Paragraph(
                    _escape_xml(para), styles["body"]
                ))
    else:
        items.append(Paragraph(
            "<i>Not documented.</i>", styles["body_muted"]
        ))

    items.append(Paragraph("Decision Reasoning", styles["subsection_h"]))
    reasoning = st.session_state.stage6_reasoning.strip()
    if reasoning:
        for para in reasoning.split("\n"):
            if para.strip():
                items.append(Paragraph(
                    _escape_xml(para), styles["body"]
                ))
    else:
        items.append(Paragraph(
            "<i>Not documented.</i>", styles["body_muted"]
        ))

    return items


# ────────────────────────────────────────────────────────────────────
# PDF: ENTRY POINT
# ────────────────────────────────────────────────────────────────────

def _generate_pdf() -> bytes:
    """Generate the Documented Record PDF.

    Layout:
        Page 1: Decision Brief (one-page executive summary)
        Page 2+: Analytic Record (five numbered sections with side-by-side
                 considerations tables per action)
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = _build_styles()
    date_str = datetime.now().strftime("%B %d, %Y")

    story = []
    story.extend(_build_brief(styles, date_str))
    story.append(PageBreak())
    story.extend(_build_record(styles))

    doc.build(
        story,
        onFirstPage=_draw_page_decoration,
        onLaterPages=_draw_page_decoration,
    )
    return buffer.getvalue()


# ────────────────────────────────────────────────────────────────────
# IN-APP RECORD SUMMARY (collapsible)
# ────────────────────────────────────────────────────────────────────

def _render_record_summary():
    """Render the collapsible read-only record summary (in-app, not PDF)."""
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


# ────────────────────────────────────────────────────────────────────
# STAGE 6 ENTRY POINT
# ────────────────────────────────────────────────────────────────────

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
    pdf_bytes = _generate_pdf()
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
        