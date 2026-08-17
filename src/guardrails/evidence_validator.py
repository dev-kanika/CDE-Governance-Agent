import os

from dotenv import load_dotenv
#from google import genai
from llm.groq_client import generate_structured
from pydantic import BaseModel


load_dotenv()

#client = genai.Client(
#    api_key=os.getenv("GEMINI_API_KEY")
#)

#MODEL = "gemini-3.5-flash"

class CandidateValidation(BaseModel):
    name: str
    supported: bool
    supported_claims: list[str]
    unsupported_claims: list[str]
    corrected_criteria: list[str]
    corrected_reason: str


class ValidationResults(BaseModel):
    validations: list[CandidateValidation]


def validate_candidates(candidates):

    candidate_text = "\n\n".join(
        f"""
CANDIDATE {i + 1}

Name:
{candidate.name}

Description:
{candidate.description}

Claimed Criticality:
{candidate.criticality}

Claimed Criteria:
{candidate.criteria_met}

Reason:
{candidate.reason}

Source:
{candidate.source}

Page:
{candidate.page}

Supporting Evidence:
{candidate.evidence}
"""
        for i, candidate in enumerate(candidates)
    )

    prompt = f"""
You are an evidence validator for a banking
data-governance system.

Your ONLY job is to check whether the claims made by
each candidate are directly supported by its provided
source evidence.

Do NOT use outside knowledge.

Do NOT decide whether anything is an officially
confirmed CDE.

VALIDATION RULES:

1. Check every candidate independently.

2. Check every claimed criterion independently.

3. A claim is supported only when the provided evidence
   directly supports it.

4. Do not treat assumptions or reasonable interpretations
   as direct evidence.

5. Keep supported claims.

6. Identify unsupported claims.

7. corrected_criteria must contain ONLY criteria directly
   supported by the evidence.

8. corrected_reason must use ONLY supported information.

9. Never invent evidence.

10. The candidate may remain valid even when some claims
    fail validation.

11. Criteria are independent. Evidence supporting one
    criterion does not automatically support another criterion.

12. Evidence supporting CALCULATION does not automatically
    support OUTPUT.

13. Evidence supporting IDENTIFICATION / LINKING does not
    automatically support OUTPUT.

14. Mark OUTPUT as supported ONLY when the provided evidence
    explicitly describes the data element as being required
    to produce, populate, generate, report, or determine a
    named business or regulatory output.

15. When the evidence does not directly support a criterion,
    mark that criterion as unsupported.

16. For IDENTIFICATION / LINKING, direct evidence that a field
    identifies an account, depositor, business object, or record
    is sufficient. The evidence does not also need to explicitly
    describe a file-to-file relationship.

17. "Confirmed CDE" is a human governance decision.

CANDIDATES TO VALIDATE:

{candidate_text}

Return one validation object for EVERY candidate.
"""

    #response = client.models.generate_content(
    #    model=MODEL,
    #    contents=prompt,
    #    config={
    #        "response_mime_type": "application/json",
    #        "response_schema": ValidationResults,
    #    },
    #)

    response_text = generate_structured(
        prompt,
        ValidationResults
    )

    return ValidationResults.model_validate_json(
        response_text
    )