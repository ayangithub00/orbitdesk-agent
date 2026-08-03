from langgraph.graph import StateGraph, END

from state import AgentState
from nodes.triage import triage_node
from nodes.retreival_node import retrieval_node
from nodes.generation import generation_node
from nodes.verification import verification_node

graph = StateGraph(AgentState)

graph.add_node("triage", triage_node)
graph.add_node("retrieval", retrieval_node)
graph.add_node("generation", generation_node)
graph.add_node("verification", verification_node)

graph.set_entry_point("triage")


def route_after_triage(state: AgentState):
    classification = state["classification"]

    if classification == "answerable":
        return "retrieval"

    elif classification == "requires_clarification":
        return END

    elif classification == "requires_escalation":
        return END

    elif classification == "out_of_scope":
        return END

    return END


def route_after_verification(state: AgentState):
    if state["verified"]:
        return END

    if state["retry_count"] < 2:
        return "generation"

    return END


graph.add_conditional_edges(
    "triage",
    route_after_triage
)

graph.add_edge("retrieval", "generation")
graph.add_edge("generation", "verification")

graph.add_conditional_edges(
    "verification",
    route_after_verification
)

app = graph.compile()