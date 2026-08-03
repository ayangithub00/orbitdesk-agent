import sys
sys.path.append("..")

from state import AgentState
from model import generator


def generation_node(state: AgentState):
    print("[Generation]")

    question = state["question"]
    documents = state["documents"]

    retry_count = state.get("retry_count", 0)

    context = ""

    for doc in documents:
        context += f"Document: {doc['filename']}\n"
        context += f"{doc['content']}\n\n"

    retry_message = ""

    if retry_count > 0:
        retry_message = """
The previous answer was not verified.
Generate a better answer using ONLY the provided context.
"""

    prompt = f"""
You are an AI support assistant for OrbitDesk.

Answer ONLY using the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided documents."

{retry_message}

Context:
{context}

Question:
{question}

Answer:
"""

    response = generator(
        prompt,
        max_new_tokens=200,
        do_sample=False
    )

    answer = response[0]["generated_text"].replace(prompt, "").strip()

    retry_count += 1

    sources = []

    for doc in documents:
        sources.append({
            "source_id": doc["source_id"],
            "passage": doc["filename"]
        })

    confidence = round(min(1.0, 0.6 + 0.1 * len(documents)), 2)

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "requires_human": False,
        "reason": "Generated from retrieved OrbitDesk documentation.",
        "retry_count": retry_count
    }