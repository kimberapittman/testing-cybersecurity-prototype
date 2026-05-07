"""
Domain definitions, prompts, and patterns for NIST CSF and PFCE frameworks.
"""

# ── NIST CSF Domains ──

NIST_DOMAINS = {
    "GOVERN": {
        "prompt": (
            "Are you establishing, reviewing, or overseeing cybersecurity "
            "risk management strategy, policies, or governance expectations?"
        ),
        "description": (
            "Cybersecurity decisions are legitimate, directed, and accountable."
        ),
        "tier2_prompt": (
            "What governance, authorization, or policy considerations "
            "does this action raise?"
        ),
        "guidance": [
            "Does this action require bypassing or exceeding normal authorization?",
            "Is this action consistent with established policy and governance expectations?",
            "Is the decision-maker's authority sufficient for this action?",
        ],
        "patterns": [
            "Consistent with existing policy",
            "No policy exists for this type of action",
            "Policy exists but does not clearly address this situation",
            "Action conflicts with or deviates from established policy",
            "Requires authorization the decision-maker does not hold",
            "Requires bypassing normal authorization due to urgency",
            "Governance expectations are unclear or undefined for this situation",
        ],
    },
    "IDENTIFY": {
        "prompt": (
            "Are you working to understand current cybersecurity risks, such as "
            "identifying assets, systems, vulnerabilities, or risk exposure?"
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
            "Are you applying or managing safeguards to reduce or manage "
            "cybersecurity risk?"
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
            "Are you monitoring for, identifying, or analyzing potential "
            "cybersecurity attacks or compromises?"
        ),
        "description": (
            "Cybersecurity events are identified and characterized in time to act."
        ),
        "tier2_prompt": (
            "How does this action affect the ability to detect or "
            "monitor threats?"
        ),
        "guidance": [
            "Does this action reduce access to monitoring, logs, or telemetry?",
            "Does this action affect the ability to identify whether the threat has spread?",
        ],
        "patterns": [
            "Preserves or improves monitoring and detection capability",
            "Reduces access to monitoring, logs, or telemetry",
            "Limits ability to determine whether the threat has spread",
            "Detection capability was already limited before this action",
            "Creates a monitoring gap during implementation",
            "No meaningful effect on detection capability",
        ],
    },
    "RESPOND": {
        "prompt": (
            "Are you taking action in response to a confirmed cybersecurity incident?"
        ),
        "description": (
            "Cybersecurity incidents are managed to limit harm."
        ),
        "tier2_prompt": (
            "How does this action affect incident containment "
            "or coordination?"
        ),
        "guidance": [
            "Does this action delay or constrain the ability to contain the incident?",
            "Does this action affect coordination with other responders or stakeholders?",
        ],
        "patterns": [
            "Supports containment of the incident",
            "Delays or constrains the ability to contain the incident",
            "Coordination with other parties is maintained",
            "Disrupts communication channels needed for coordination",
            "Requires notification of parties not yet informed",
            "Requires coordination with external agencies not yet engaged",
            "External coordination was already limited before this action",
        ],
    },
    "RECOVER": {
        "prompt": (
            "Are you restoring systems, data, or operations affected by a "
            "cybersecurity incident?"
        ),
        "description": (
            "Operational capacity is restored after a cybersecurity incident."
        ),
        "tier2_prompt": (
            "How does this action affect the ability to restore "
            "operations?"
        ),
        "guidance": [
            "Does this action extend the time or effort required to restore operations?",
            "Does this action affect the order or priority of what gets restored?",
        ],
        "patterns": [
            "Supports faster or easier restoration",
            "Extends recovery timeline",
            "May compromise backup integrity or availability",
            "Affects the order or priority of what gets restored",
            "Recovery impact depends on conditions not yet known",
            "No meaningful effect on recovery timeline",
        ],
    },
}

# ── PFCE Domains ──

PFCE_DOMAINS = {
    "BENEFICENCE": {
        "prompt": (
            "This decision could meaningfully improve safety, well-being, or "
            "other benefits for people, but only if certain risks are accepted."
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
            "This decision could create harm, increase exposure to harm, or "
            "make conditions worse for people, even indirectly."
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
            "This decision could affect people's ability to make informed "
            "choices, understand how risks apply to them, or exercise control "
            "over their exposure to consequences."
        ),
        "description": (
            "Affected parties retain meaningful agency and informed choice."
        ),
        "tier2_prompt": (
            "How does this action affect people's ability to make "
            "informed choices or control their exposure?"
        ),
        "guidance": [
            "Who is affected by this action, and are they aware of its implications?",
            "Does this action reduce anyone's ability to make informed choices about matters affecting them?",
            "Is consent feasible, and if not, what justifies proceeding without it?",
            "Does this action create or extend information asymmetry between the municipality and affected parties?",
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
        ],
    },
    "JUSTICE": {
        "prompt": (
            "The risks, burdens, or impacts of this decision could be "
            "distributed unevenly across people, groups, or communities."
        ),
        "description": (
            "Burdens and benefits are not unfairly or disproportionately distributed."
        ),
        "tier2_prompt": (
            "Could the burdens or benefits of this action fall unevenly "
            "on different groups?"
        ),
        "guidance": [
            "Are the burdens of this action distributed evenly across affected populations?",
            "Do any groups bear disproportionate risk or loss of access?",
            "Are there populations with fewer alternatives or resources to absorb the impact?",
            "Does this action reinforce or create inequity in who is protected and who is exposed?",
        ],
        "patterns": [
            "No disproportionate impact identified",
            "Lower-income populations face greater impact",
            "Populations with fewer digital alternatives are disproportionately affected",
            "Specific neighborhoods or communities bear concentrated impact",
            "Communities subject to monitoring or surveillance bear privacy burden others do not",
            "Some departments or services absorb more disruption than others",
            "Reinforces existing inequity in who is protected and who is exposed",
        ],
    },
    "EXPLICABILITY": {
        "prompt": (
            "This decision could be difficult to explain or assign "
            "responsibility for if questioned later."
        ),
        "description": (
            "Decisions and actions are explainable, traceable, and accountable."
        ),
        "tier2_prompt": (
            "How explainable and accountable is this action "
            "if questioned?"
        ),
        "guidance": [
            "Could this action be explained to affected parties if questioned?",
            "Is the reasoning for this action documented in a form that supports review?",
            "Is it clear who authorized this action and under what authority?",
            "Are there aspects of this action that would be difficult to justify publicly?",
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
        ],
    },
}
