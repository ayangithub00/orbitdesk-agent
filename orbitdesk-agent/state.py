from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    question: str
    classification: str
    documents: List[dict]
    answer: str
    sources: List[dict]
    confidence: float
    requires_human: bool
    reason: str
    retry_count: int
    verified: bool
    clarification_question: Optional[str]