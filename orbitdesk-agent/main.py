from graph import app
import json

import json

with open("sample_questions.json", "r") as f:
    questions = json.load(f)

for q in questions["questions"]: 
    print(f"\n--- {q['question_id']} ---")
    question = q["question"]

    state = {
        "question": question,
        "retry_count": 0
    }

    result = app.invoke(state)

    final_output = {        
        "classification": result.get("classification"),
        "answer": result.get("answer"),
        "sources": result.get("sources", []),
        "confidence": result.get("confidence", 0.0),
        "requires_human": result.get("requires_human", False),
        "reason": result.get("reason", "")
    }

    print("\nFinal Response:")       
    print(json.dumps(final_output, indent=4))    
