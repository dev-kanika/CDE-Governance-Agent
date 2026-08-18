# CDE Governance Agent

**Live App:** https://cde-governance-agent.streamlit.app/

An AI-powered data governance assistant that identifies potential **Critical Data Elements (CDEs)** from regulatory and business documents, validates the evidence behind them, and presents the results for human governance review.

## What Does It Do?

**Upload a document → Find relevant evidence → Identify candidate CDEs → Validate the claims → Review → Export**

The system helps data governance teams discover and assess potential CDEs while keeping the final governance decision with a human reviewer.

## How It Works

1. **Upload a document** — PDF or DOCX.
2. **Extract content** — the document is processed into usable sections.
3. **Retrieve evidence** — relevant evidence is retrieved using semantic search and ChromaDB.
4. **Identify candidate CDEs** — the AI analyzes the evidence and identifies potential CDEs.
5. **Evaluate criteria** — candidates are assessed against OUTPUT, CALCULATION, IDENTIFICATION / LINKING, OWNERSHIP / AGGREGATION and VALIDATION / RECONCILIATION.
6. **Validate evidence** — a separate validation layer checks whether claimed criteria are supported by the evidence.
7. **Governance review** — a human reviewer examines the candidate, evidence and validation.
8. **Export** — governance information can be exported as a CSV register.

## Guardrails

- Uses only evidence supplied from the source document.
- Avoids inventing data elements or supporting evidence.
- Separates candidate discovery from evidence validation.
- Flags unsupported claims for review.
- The AI does **not** make the final CDE designation.
- Final governance decisions remain with a human reviewer.

## Architecture

```text
Document Upload
      ↓
Document Reader
      ↓
Evidence Retrieval + ChromaDB
      ↓
CDE Extraction + Groq LLM
      ↓
Evidence Validation
      ↓
Human Governance Review
      ↓
Governance Register / CSV
```

## Technology

- Python
- Streamlit
- Groq — `openai/gpt-oss-120b`
- ChromaDB
- Pydantic
- PyMuPDF
- python-docx
- Sentence Transformers
- Pandas

## Project Structure

```text
CDE-GOVERNANCE-AGENT/
├── src/
│   ├── agent/
│   ├── guardrails/
│   ├── ingestion/
│   ├── retrieval/
│   └── llm/
├── ui/
│   └── app.py
├── data/
├── requirements.txt
├── .gitignore
└── README.md
```

## Key Principle

> **AI identifies. Evidence validates. Humans govern.**

## Running Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run ui/app.py
```

Create a `.env` file containing:

```text
GROQ_API_KEY=your_api_key_here
```

## Project Outcome

This project demonstrates an end-to-end AI-assisted data governance workflow, including document ingestion, semantic evidence retrieval, LLM-based CDE discovery, evidence validation, human governance review and deployment as a working Streamlit application.

## Disclaimer

This is a decision-support prototype. AI-generated results should be reviewed by appropriate data-governance professionals before being used for formal regulatory, compliance or business decisions.
