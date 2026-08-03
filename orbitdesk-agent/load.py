import json
import os

documents = []


# Load Knowledge Base Documents

files = os.listdir("knowledge_base")

for file in files:
    if file.endswith(".md"):
        path = os.path.join("knowledge_base", file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        documents.append({
            "type": "knowledge_base",
            "filename": file,
            "source_id": file,
            "content": content
        })


# Load Resolved Cases

with open("resolved_cases.json", "r", encoding="utf-8") as f:
    resolved_cases = json.load(f)

for case in resolved_cases["cases"]:

    text = f"""
Case ID: {case['case_id']}

Title:
{case['title']}

Symptoms:
{" ".join(case.get("symptoms", []))}

Resolution:
{" ".join(case.get("resolution", []))}
"""

    documents.append({
        "type": "resolved_case",
        "filename": case["case_id"],
        "source_id": case["case_id"],
        "content": text
    })


print(f"Loaded {len(documents)} documents.")