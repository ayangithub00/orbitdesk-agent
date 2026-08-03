import sys
sys.path.append("..")

from state import AgentState


def triage_node(state: AgentState):
    print("[Triage]")

    question = state["question"].lower()

    out_of_scope_keywords = [
        "refund",
        "subscription",
        "payment",
        "billing",
        "legal",
        "lawyer",
        "medical"
    ]

    escalation_keywords = [
        "escalate",
        "administrator",
        "human",
        "support team"
    ]

    clarification_keywords = [
        "not working",
        "doesn't work",
        "broken",
        "issue",
        "problem",
    ]

    if any(word in question for word in out_of_scope_keywords):
        classification = "out_of_scope"

    elif any(word in question for word in escalation_keywords):
        classification = "requires_escalation"

    elif any(word in question for word in clarification_keywords):
        classification = "requires_clarification"

    else:
        classification = "answerable"

    return {
        "classification": classification
    }