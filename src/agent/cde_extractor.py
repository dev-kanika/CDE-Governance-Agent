import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import os
import chromadb

from dotenv import load_dotenv
#from google import genai
from llm.groq_client import generate_structured
from pydantic import BaseModel

load_dotenv()

#client = genai.Client(
#    api_key=os.getenv("GEMINI_API_KEY")
#)

#MODEL = "gemini-3.5-flash"


class CandidateCDE(BaseModel):
    name: str
    description: str
    criticality: str
    criteria_met: list[str]
    reason: str
    source: str
    page: int
    evidence: str


class CandidateCDEList(BaseModel):
    candidates: list[CandidateCDE]


def retrieve_evidence(question, n_results=5):

    chroma = chromadb.PersistentClient(
        path="data/chroma_db"
    )

    collection = chroma.get_collection(
        "fdic_documents"
    )

    results = collection.query(
        query_texts=[question],
        n_results=n_results,
        include=[
            "documents",
            "metadatas",
            "distances"
        ],
    )

    evidence = []

    for i, text in enumerate(results["documents"][0]):

        evidence.append({
            "text": text,
            "source": results["metadatas"][0][i]["source"],
            "page": results["metadatas"][0][i]["page"],
            "distance": results["distances"][0][i],
        })

    return evidence


def analyze_cdes(question, evidence):

    evidence_text = "\n\n".join(
        f"""
SOURCE: {item['source']}
PAGE: {item['page']}

EVIDENCE:
{item['text']}
"""
        for item in evidence
    )

    prompt = f"""
You are a banking data-governance analysis assistant.

Your task is to identify CANDIDATE Critical Data Elements
from the provided source evidence.

CRITICAL RULES:

1. Use ONLY the provided evidence.
2. Do not use outside knowledge.
3. Do not invent data elements.
4. Do NOT declare anything a confirmed CDE.
5. A data element must have documentary evidence supporting
   its critical role.
6. Being mentioned in a document is NOT enough.
7. Preserve the exact terminology used by the source.
8. Avoid duplicate concepts where one source term represents
   the same underlying data element.
9. If evidence is insufficient, do not force a classification.
10. IMPORTANT: Review ALL provided evidence for explicitly named
    data elements. If a field is explicitly defined in the evidence
    and directly satisfies at least one criterion, include it as a
    candidate. Do not omit a field simply because another candidate
    appears more important.
11. A candidate may satisfy multiple criteria. Evaluate each
    criterion independently.

Evaluate each candidate against these criteria:

1. OUTPUT
   Mark this criterion ONLY when the source evidence explicitly
   states that the data element is required to produce, populate,
   generate, report, or determine a named business or regulatory
   output.

   Do NOT infer OUTPUT merely because the element contributes
   to a calculation or determination.

2. CALCULATION
   Is the element required for a calculation or determination?

3. IDENTIFICATION / LINKING
   Is the element explicitly required to identify a business
   object, account, depositor, or record, or to connect/link
   related records?

   Identifying an account or record qualifies even if the
   evidence does not explicitly say that it links to another
   record.

4. OWNERSHIP / AGGREGATION
   Is the element required to determine ownership, capacity,
   or aggregation?

5. VALIDATION / RECONCILIATION
   Is the element required to validate or reconcile results?

CLASSIFICATION:

STRONG CANDIDATE:
Evidence clearly demonstrates one or more of the criteria.

POTENTIAL CANDIDATE:
The element appears relevant, but evidence is incomplete.

NOT ESTABLISHED:
The element is mentioned, but the evidence does not establish
criticality.

ABSTAIN:
There is insufficient evidence to make a determination.

IMPORTANT:
"Confirmed CDE" is a HUMAN GOVERNANCE DECISION.

The purpose of this step is candidate discovery, not final
approval. Prefer complete evidence-based candidate discovery
over aggressive filtering.

The AI must never output "confirmed CDE."

For every candidate provide:

- name
- description
- criticality
- criteria_met
- reason
- source
- page
- exact supporting evidence

USER QUESTION:

{question}

SOURCE EVIDENCE:

{evidence_text}
"""

    #response = client.models.generate_content(
    #    model=MODEL,
    #    contents=prompt,
    #    config={
    #        "response_mime_type": "application/json",
    #        "response_schema": CandidateCDEList,
    #    },
    #)

    response_text = generate_structured(
        prompt,
        CandidateCDEList
    )

    return CandidateCDEList.model_validate_json(
        response_text
    )