import sys
sys.path.append("..")

from state import AgentState


def verification_node(state: AgentState):
    print("[Verification]")

    documents = state.get("documents", [])
    answer = state.get("answer", "")
    sources = state.get("sources", [])

    verified = True
    reason = "Verification passed."

    
    # Check 1: Answer exists
    
    if not answer.strip():
        verified = False
        reason = "Answer is empty."

   
    # Check 2: Sources exist
   
    elif len(sources) == 0:
        verified = False
        reason = "No source references."

    
    # Check 3: Documents retrieved
   
    elif len(documents) == 0:
        verified = False
        reason = "No supporting documents retrieved."


    print("Verification:", verified)

    return {
        "verified": verified,
        "reason": reason
    }