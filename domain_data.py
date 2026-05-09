"""
Domain definitions, prompts, and patterns for NIST CSF and PFCE frameworks.
"""

# ── PFCE Domains ──
# Listed FIRST — ethical before technical, always.

PFCE_DOMAINS = {
    "BENEFICENCE": {
        "prompt": (
            "Could this decision meaningfully improve safety, well-being, "
            "or other benefits for people?"
        ),
        "description": (
            "Human well-being and normal social functioning are supported "
            "rather than undermined."
        ),
        "tier2_prompt": (
            "What benefit does this action support, and what conditions "
            "or risks does realizing that benefit require?"
        ),
        "guidance": [
            "Who benefits from this action, and how?",
            "What conditions must hold for the benefit to be realized?",
            "Could pursuit of this benefit create risk or exposure for others?",
            "What benefit is foregone if this action is not taken?",
        ],
        "patterns": [
            "Reduces exposure to a known or active threat",
            "Preserves continuity of public services",
            "Protects personal data or sensitive information",
            "Benefit depends on conditions not yet confirmed",
            "Benefit to some creates risk or exposure for others",
            "Continued vulnerability to a known risk if not taken",
            "Loss of opportunity to contain or mitigate an active threat if not taken",
            "Missed opportunity to establish governance precedent if not taken",
            "Erosion of public trust or institutional credibility if not taken",
        ],
    },
    "NON-MALEFICENCE": {
        "prompt": (
            "Could this decision create harm, increase exposure to harm, or "
            "make conditions worse for people, even indirectly?"
        ),
        "description": (
            "Avoidable harm to people, institutions, or society is minimized."
        ),
        "tier2_prompt": (
            "What harm could this action create, increase, or enable?"
        ),
        "guidance": [
            "Who may be harmed by this action?",
            "Through what mechanism does this action produce or enable harm?",
            "How severe could this harm be, and is it reversible?",
            "Could this action cause harm that extends beyond the immediate decision context?",
        ],
        "patterns": [
            "Service disruption affecting residents",
            "Personal data exposure or compromise",
            "Public safety or emergency service disruption",
            "Harm to employees involved in response or affected operations",
            "Delayed response allowing harm to continue or spread",
            "Resource diversion from other critical functions",
            "Harm extending beyond the immediate decision context",
            "Disproportionate impact on populations with limited alternatives",
            "Erosion of public trust in municipal institutions",
        ],
    },
    "AUTONOMY": {
        "prompt": (
            "Could this decision affect people's ability to make informed "
            "choices, maintain control over their data or systems, or "
            "understand how risks apply to them?"
        ),
        "description": (
            "Affected parties retain meaningful agency and informed choice."
        ),
        "tier2_prompt": (
            "How does this action affect people's ability to make "
            "informed choices, control their data, or manage their "
            "own exposure?"
        ),
        "guidance": [
            "Who is affected by this action, and are they aware of its implications?",
            "Does this action reduce anyone's ability to make informed choices about matters affecting them?",
            "Is consent feasible, and if not, what justifies proceeding without it?",
            "Does this action create or extend information asymmetry between the municipality and affected parties?",
            "Does this action affect anyone's ownership of or control over their data or systems?",
        ],
        "patterns": [
            "Affected parties are unaware of the action or its implications",
            "Reduces ability of affected parties to make informed choices",
            "Creates or extends information asymmetry",
            "Consent is not feasible due to time constraints",
            "Consent is not feasible due to scale of affected population",
            "Consent is not feasible because affected parties cannot be identified",
            "Consent is not applicable — internal operational decision",
            "Affected parties retain meaningful choice and awareness",
            "Affects ownership or control of data belonging to individuals or organizations",
        ],
    },
    "JUSTICE": {
        "prompt": (
            "Could this decision raise concerns about fairness — whether in "
            "how its impacts are distributed, how the decision itself is made, "
            "or whose rights are affected?"
        ),
        "description": (
            "Burdens and benefits are distributed fairly, processes are "
            "legitimate, and rights are protected."
        ),
        "tier2_prompt": (
            "Could the burdens, benefits, or processes associated with "
            "this action raise fairness concerns?"
        ),
        "guidance": [
            "Are the burdens of this action distributed evenly across affected populations?",
            "Do any groups bear disproportionate risk or loss of access?",
            "Are there populations with fewer alternatives or resources to absorb the impact?",
            "Does this action reinforce or create inequity in who is protected and who is exposed?",
            "Was the process for making this decision fair and transparent to affected parties?",
            "Does this action affect anyone's rights — property, data, privacy, or access to services?",
            "Could this action discriminate against or disproportionately burden any group?",
            "Does this action affect who can access public services or systems?",
        ],
        "patterns": [
            "No disproportionate impact identified",
            "Lower-income populations face greater impact",
            "Populations with fewer digital alternatives are disproportionately affected",
            "Specific neighborhoods or communities bear concentrated impact",
            "Communities subject to monitoring or surveillance bear privacy burden others do not",
            "Some departments or services absorb more disruption than others",
            "Reinforces existing inequity in who is protected and who is exposed",
            "Decision-making process lacks transparency or stakeholder input",
            "No procedural mechanism exists to govern this type of action",
            "Privacy or property rights of affected parties may not be adequately protected",
            "Action may limit accessibility to services for some populations",
            "Could discriminate against or produce bias toward specific groups",
        ],
    },
    "EXPLICABILITY": {
        "prompt": (
            "Could this decision raise questions about who authorized it, "
            "why it was chosen, or how it would be explained to "
            "affected parties?"
        ),
        "description": (
            "Decisions and actions are explainable, traceable, and accountable."
        ),
        "tier2_prompt": (
            "How explainable, transparent, and accountable is this action?"
        ),
        "guidance": [
            "Could this action be explained to affected parties if questioned?",
            "Is the reasoning for this action documented in a form that supports review?",
            "Is it clear who authorized this action and under what authority?",
            "Are there aspects of this action that would be difficult to justify publicly?",
            "Are the policies and procedures governing this type of decision transparent and publicly accessible?",
            "Has the organization met its obligation to maintain the systems and practices needed to prevent this situation?",
        ],
        "patterns": [
            "Reasoning is clear and communicable",
            "Technical aspects may be difficult to explain to non-technical audiences",
            "Trade-offs may be difficult to justify in hindsight",
            "Explanation would require disclosing information not yet public",
            "Reasoning depends on uncertainty that may not be apparent after the fact",
            "Authorization and responsibility are clear",
            "Authorization or responsibility is unclear or undocumented",
            "Aspects of this action would be difficult to justify publicly",
            "Policies governing this type of decision are transparent and publicly documented",
            "Organization has met professional diligence obligations for system maintenance and security practices",
            "Decision involves automated systems whose operation may not be fully understood by decision-makers",
        ],
    },
}

# ── NIST CSF Domains ──

NIST_DOMAINS = {
    "GOVERN": {
        "prompt": (
            "Does this decision involve establishing, reviewing, or overseeing "
            "cybersecurity risk management strategy, policies, governance "
            "expectations, or third-party dependencies?"
        ),
        "description": (
            "Cybersecurity decisions are legitimate, directed, and accountable."
        ),
        "tier2_prompt": (
            "What governance, authorization, policy, or oversight "
            "considerations does this action raise?"
        ),
        "guidance": [
            "Does this action require bypassing or exceeding normal authorization?",
            "Is this action consistent with established policy and governance expectations?",
            "Is the decision-maker's authority sufficient for this action?",
            "Does this action align with the organization's mission priorities and stakeholder expectations?",
            "Does this action involve third-party vendors, service providers, or supply chain dependencies that introduce additional risk?",
            "Is there a formal oversight mechanism to monitor how this type of decision is implemented?",
        ],
        "patterns": [
            "Consistent with existing policy",
            "No policy exists for this type of action",
            "Policy exists but does not clearly address this situation",
            "Action conflicts with or deviates from established policy",
            "Requires authorization the decision-maker does not hold",
            "Requires bypassing normal authorization due to urgency",
            "Governance expectations are unclear or undefined for this situation",
            "Involves third-party or vendor dependencies not fully assessed",
            "Stakeholder expectations regarding this type of decision are unknown or unclear",
            "No formal oversight mechanism exists to monitor how this type of decision is implemented",
        ],
    },
    "IDENTIFY": {
        "prompt": (
            "Does this decision involve understanding current cybersecurity "
            "risks, such as identifying assets, systems, vulnerabilities, "
            "or risk exposure?"
        ),
        "description": (
            "The organization has situational awareness of its cybersecurity risks."
        ),
        "tier2_prompt": (
            "How does this action affect understanding of the current "
            "risk landscape?"
        ),
        "guidance": [
            "Does this action reduce the ability to understand the scope or nature of the risk?",
            "Does this action affect awareness of what other systems or assets may be exposed?",
        ],
        "patterns": [
            "Improves visibility into scope or nature of the risk",
            "Reduces visibility into scope or nature of the risk",
            "Affects awareness of which systems or assets may be exposed",
            "Risk landscape is unclear and this action does not resolve that uncertainty",
            "Action proceeds despite incomplete asset or system inventory",
            "No meaningful effect on risk understanding",
        ],
    },
    "PROTECT": {
        "prompt": (
            "Does this decision involve applying or managing safeguards "
            "to reduce or manage cybersecurity risk?"
        ),
        "description": (
            "Cybersecurity risks are mitigated to prevent incidents or limit exposure."
        ),
        "tier2_prompt": (
            "How does this action affect existing safeguards or "
            "create new exposure?"
        ),
        "guidance": [
            "Does this action strengthen or weaken existing safeguards?",
            "Does this action create new exposure while addressing current risk?",
        ],
        "patterns": [
            "Strengthens or reinforces existing safeguards",
            "Weakens or removes an existing safeguard",
            "No new exposure created",
            "Creates temporary exposure during implementation",
            "Addresses one risk but opens a different vulnerability",
            "Removes a safeguard that was protecting against a different threat",
            "Uncertain whether new exposure is created",
        ],
    },
    "DETECT": {
        "prompt": (
            "Does this decision involve capabilities for monitoring, "
            "detecting, or analyzing cybersecurity-relevant activity "
            "or events?"
        ),
        "description": (
            "Cybersecurity events are identified and characterized in time to act."
        ),
        "tier2_prompt": (
            "How does this action affect the ability to detect, "
            "monitor, or analyze cybersecurity-relevant activity?"
        ),
        "guidance": [
            "Does this action reduce access to monitoring, logs, or telemetry?",
            "Does this action affect the ability to identify whether the threat has spread?",
            "Does this action affect ongoing monitoring or detection capabilities beyond the immediate situation?",
        ],
        "patterns": [
            "Preserves or improves monitoring and detection capability",
            "Reduces access to monitoring, logs, or telemetry",
            "Limits ability to determine whether the threat has spread",
            "Detection capability was already limited before this action",
            "Creates a monitoring gap during implementation",
            "Affects ongoing detection capabilities beyond the immediate situation",
            "No meaningful effect on detection capability",
        ],
    },
    "RESPOND": {
        "prompt": (
            "Does this decision involve how the organization acts on "
            "detected cybersecurity events or manages incident-related "
            "processes?"
        ),
        "description": (
            "Cybersecurity incidents are managed to limit harm."
        ),
        "tier2_prompt": (
            "How does this action affect incident containment, "
            "coordination, or response processes?"
        ),
        "guidance": [
            "Does this action delay or constrain the ability to contain the incident?",
            "Does this action affect coordination with other responders or stakeholders?",
            "Does this action affect how the organization communicates about the incident to affected parties?",
        ],
        "patterns": [
            "Supports containment of the incident",
            "Delays or constrains the ability to contain the incident",
            "Coordination with other parties is maintained",
            "Disrupts communication channels needed for coordination",
            "Requires notification of parties not yet informed",
            "Requires coordination with external agencies not yet engaged",
            "External coordination was already limited before this action",
            "Affects how the organization communicates about the incident to affected parties",
        ],
    },
    "RECOVER": {
        "prompt": (
            "Does this decision involve restoring systems, data, or "
            "operations affected by a cybersecurity incident, or "
            "communicating recovery status to stakeholders?"
        ),
        "description": (
            "Operational capacity is restored and recovery is communicated "
            "after a cybersecurity incident."
        ),
        "tier2_prompt": (
            "How does this action affect the ability to restore "
            "operations and communicate recovery progress?"
        ),
        "guidance": [
            "Does this action extend the time or effort required to restore operations?",
            "Does this action affect the order or priority of what gets restored?",
            "Does this action affect how recovery progress is communicated to stakeholders, employees, or the public?",
        ],
        "patterns": [
            "Supports faster or easier restoration",
            "Extends recovery timeline",
            "May compromise backup integrity or availability",
            "Affects the order or priority of what gets restored",
            "Recovery impact depends on conditions not yet known",
            "No meaningful effect on recovery timeline",
            "Recovery communication to affected parties is planned and resourced",
            "No communication plan exists for updating stakeholders during recovery",
        ],
    },
}
