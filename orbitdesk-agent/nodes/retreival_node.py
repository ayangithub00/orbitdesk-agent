from retreival import search
import sys
sys.path.append("..")
from state import AgentState


def retrieval_node(state: AgentState):
    print("[Retrieval]")

    question = state["question"]

    try:
        documents = search(question)
    except Exception:
        documents = []

    return {
        "documents": documents
    }