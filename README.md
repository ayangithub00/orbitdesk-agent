# OrbitDesk Support Agent

A local-first AI support agent built with LangGraph that answers support questions using a fictional product knowledge base.

## Overview

This project implements a multi-node agent workflow that:
- Classifies incoming questions (answerable, clarification, escalation, out of scope)
- Retrieves relevant documents using FAISS vector search
- Generates answers using a local Hugging Face model
- Verifies answers before returning them

## Models Used

| Model | Purpose | Library |
|-------|---------|---------|
| `all-MiniLM-L6-v2` | Document embeddings and semantic search | sentence-transformers |
| `Qwen/Qwen2.5-1.5B-Instruct` | Answer generation | transformers |

Both models run completely locally. No internet connection is required after initial model download.

## Hardware Used

- CPU: Apple M2
- RAM: 8GB
- GPU: None (CPU only)
- Model load time: ~30 seconds
- Average response latency: ~10-15 seconds per question

## Project Structure

```
orbitdesk-agent/
├── knowledge_base/          # Product documentation (10 markdown files)
├── nodes/
│   ├── triage.py           # Classifies incoming questions
│   ├── retreival_node.py   # Retrieves relevant documents
│   ├── generation.py       # Generates answers using local LLM
│   └── verification.py     # Verifies answer quality
├── graph.py                # LangGraph workflow definition
├── state.py                # Shared agent state
├── load.py                 # Loads knowledge base and resolved cases
├── retreival.py            # FAISS index and search function
├── model.py                # Local LLM setup
├── main.py                 # Entry point
├── resolved_cases.json     # Historical support cases
├── sample_questions.json   # Test questions
├── output_schema.json      # Response schema
└── requirements.txt
```

## Setup Instructions

**1. Clone the repository:**
```bash
git clone <github.com/ayangithub00/orbitdesk-agent>
cd orbitdesk-agent
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the agent:**
```bash
python main.py
```

Models will be downloaded automatically on first run (~1-2 GB).

## Graph Workflow

```
[START] → [Triage]
              ↓
    ┌─────────────────────────────┐
    ↓           ↓          ↓     ↓
[Retrieval] [Clarification] [Escalation] [Out of Scope]
    ↓              ↓              ↓           ↓
[Generation]      END            END         END
    ↓
[Verification]
    ↓              ↓
   END      [Generation] (retry, max 2)
    ↓
   END
```

## Sample Output

```json
{
    "classification": "answerable",
    "answer": "No, you do not have permission to create an API credential as a Viewer...",
    "sources": [
        {
            "source_id": "05_api_credentials.md",
            "passage": "05_api_credentials.md"
        }
    ],
    "confidence": 0.9,
    "requires_human": false,
    "reason": "Verification passed."
}
```

## Design Trade-offs

- **Keyword-based triage** instead of LLM-based — faster but less accurate for edge cases
- **Small local model (1.5B)** instead of larger model — runs on CPU but answer quality is limited

## Known Limitations

- Triage uses keyword matching — complex questions may be misclassified
- Small local model may give incomplete answers for complex questions
- Confidence score is heuristic-based, not model-based

## What I Would Improve With More Time

- LLM-based triage for better classification accuracy
- Better confidence scoring using model logits
- Add more test cases with automated routing verification

## AI Assistance Disclosure

Claude (Anthropic) was used as a coding assistant for guidance and debugging during development. All code was written and understood by the author.
