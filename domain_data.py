"""
Domain definitions, prompts, and decomposed specification prompts
for NIST CSF and PFCE frameworks.
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
        "prompts": [
            "Does this action require bypassing or exceeding normal authorization?",
            "Is this action consistent with established policy and governance expectations?",
            "Is the decision-maker's authority sufficient for this action?",
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
        "prompts": [
            "Does this action reduce the ability to understand the scope or nature of the risk?",
            "Does this action affect awareness of what other systems or assets may be exposed?",
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
        "prompts": [
            "Does this action strengthen or weaken existing safeguards?",
            "Does this action create new exposure while addressing current risk?",
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
        "prompts": [
            "Does this action reduce access to monitoring, logs, or telemetry?",
            "Does this action affect the ability to identify whether the threat has spread?",
        ],
    },
    "RESPOND": {
        "prompt": (
            "Are you taking action in response to a confirmed cybersecurity incident?"
        ),
        "description": (
            "Cybersecurity incidents are managed to limit harm."
        ),
        "prompts": [
            "Does this action delay or constrain the ability to contain the incident?",
            "Does this action affect coordination with other responders or stakeholders?",
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
        "prompts": [
            "Does this action extend the time or effort required to restore operations?",
            "Does this action affect the order or priority of what gets restored?",
        ],
    },
}

# ── PFCE Domains ──

PFCE_DOMAINS = {
    "NON-MALEFICENCE": {
        "prompt": (
            "This decision could create harm, increase exposure to harm, or "
            "make conditions worse for people, even indirectly."
        ),
        "description": (
            "Avoidable harm to people, institutions, or society is minimized."
        ),
        "prompts": [
            "Who may be harmed by this action?",
            "Through what mechanism does this action produce or enable harm?",
            "How severe could this harm be, and is it reversible?",
            "Could this action cause harm that extends beyond the immediate decision context?",
        ],
    },
    "BENEFICENCE": {
        "prompt": (
            "This decision could meaningfully improve safety, well-being, or "
            "other benefits for people, but only if certain risks are accepted."
        ),
        "description": (
            "Human well-being and normal social functioning are supported "
            "rather than undermined."
        ),
        "prompts": [
            "Who benefits from this action, and how?",
            "What conditions must hold for the benefit to be realized?",
            "Could pursuit of this benefit create risk or exposure for others?",
            "What benefit is foregone if this action is not taken?",
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
        "prompts": [
            "Who is affected by this action, and are they aware of its implications?",
            "Does this action reduce anyone's ability to make informed choices about matters affecting them?",
            "Is consent feasible, and if not, what justifies proceeding without it?",
            "Does this action create or extend information asymmetry between the municipality and affected parties?",
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
        "prompts": [
            "Are the burdens of this action distributed evenly across affected populations?",
            "Do any groups bear disproportionate risk or loss of access?",
            "Are there populations with fewer alternatives or resources to absorb the impact?",
            "Does this action reinforce or create inequity in who is protected and who is exposed?",
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
        "prompts": [
            "Could this action be explained to affected parties if questioned?",
            "Is the reasoning for this action documented in a form that supports review?",
            "Is it clear who authorized this action and under what authority?",
            "Are there aspects of this action that would be difficult to justify publicly?",
        ],
    },
}

# ── Response Patterns for Selected Tier 2 Prompts ──
# Maps (domain_key, prompt_text) -> list of selectable pattern strings.
# Only the prompts listed here get pattern-based UI; all others keep plain text.

RESPONSE_PATTERNS = {
    ("NON-MALEFICENCE", "Who may be harmed by this action?"): [
        "Residents who depend on affected municipal services",
        "Residents whose personal data may be exposed or compromised",
        "Employees involved in response or affected operations",
        "Third-party organizations relying on municipal systems or data",
        "Vulnerable populations with limited access to alternatives",
    ],
    ("NON-MALEFICENCE", "Through what mechanism does this action produce or enable harm?"): [
        "Loss of access to services or systems",
        "Exposure of personal or sensitive data",
        "Disruption to public safety or emergency services",
        "Delayed response allowing harm to continue or spread",
        "Resource diversion from other critical functions",
        "Erosion of public trust in municipal institutions",
    ],
    ("AUTONOMY", "Is consent feasible, and if not, what justifies proceeding without it?"): [
        "Consent is feasible and can be obtained before action",
        "Consent is not feasible due to time constraints",
        "Consent is not feasible because affected parties cannot be identified",
        "Consent is not feasible due to scale of affected population",
        "Consent is not applicable — this is an internal operational decision without direct external impact requiring consent",
    ],
    ("JUSTICE", "Do any groups bear disproportionate risk or loss of access?"): [
        "No disproportionate impact identified",
        "Lower-income populations face greater impact",
        "Populations with fewer digital alternatives are disproportionately affected",
        "Specific neighborhoods or communities bear concentrated impact",
        "Communities subject to monitoring or surveillance bear privacy burden others do not",
    ],
    ("GOVERN", "Is this action consistent with established policy and governance expectations?"): [
        "Consistent with existing policy",
        "No policy exists for this type of action",
        "Policy exists but was designed for a different purpose and may not apply",
        "Action conflicts with or deviates from established policy",
        "Policy exists but does not clearly address this situation",
    ],
    ("PROTECT", "Does this action create new exposure while addressing current risk?"): [
        "No new exposure created",
        "Creates temporary exposure during implementation",
        "Addresses one risk but opens a different vulnerability",
        "Removes a safeguard that was protecting against a different threat",
        "Uncertain whether new exposure is created",
    ],
    ("RESPOND", "Does this action affect coordination with other responders or stakeholders?"): [
        "Coordination with other parties is maintained",
        "Action disrupts communication channels needed for coordination",
        "Action requires notification of parties not yet informed",
        "Action requires coordination with external agencies not yet engaged",
        "External coordination was already limited before this action",
    ],
    ("RECOVER", "Does this action extend the time or effort required to restore operations?"): [
        "Action supports faster or easier restoration",
        "Action extends recovery timeline",
        "Action may compromise backup integrity or availability",
        "Recovery impact depends on conditions not yet known",
        "Action has no meaningful effect on recovery timeline",
    ],
    ("BENEFICENCE", "What benefit is foregone if this action is not taken?"): [
        "Continued vulnerability to a known risk",
        "Loss of opportunity to contain or mitigate an active threat",
        "Delayed improvement to security posture",
        "Missed opportunity to establish governance precedent or oversight structure",
        "Erosion of public trust or institutional credibility",
    ],
    ("EXPLICABILITY", "Could this action be explained to affected parties if questioned?"): [
        "Yes — reasoning is clear and communicable",
        "Partially — technical aspects may be difficult to explain to non-technical audiences",
        "The action could be explained but the trade-offs may be difficult to justify in hindsight",
        "Explanation would require disclosing information not yet public",
        "The reasoning depends on conditions of uncertainty that may not be apparent after the fact",
    ],
}

RELATIONSHIP_TYPES = [
    "",
    "Alignment",
    "Tension",
    "Conflict",
    "Independence",
    "Not applicable",
]

RELATIONSHIP_COLORS = {
    "Alignment": "rel-alignment",
    "Tension": "rel-tension",
    "Conflict": "rel-conflict",
    "Independence": "rel-independence",
    "Not applicable": "rel-na",
}

RELATIONSHIP_DESCRIPTIONS = {
    "Alignment": "Considerations reinforce the same course of action",
    "Tension": "Considerations pull in different directions but remain partially satisfiable",
    "Conflict": "Considerations are directly incompatible; satisfying one forecloses the other",
    "Independence": "Both relevant but do not meaningfully interact",
    "Not applicable": "No meaningful relationship to examine",
}
