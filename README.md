# CDE Governance Agent

An AI-powered data governance assistant that identifies potential **Critical Data Elements (CDEs)** from regulatory and business documents, validates the evidence behind them, and presents the results for human governance review.

## What does it do?

**Upload a document → Find relevant evidence → Identify candidate CDEs → Validate the claims → Review → Export**

The system helps data-governance teams reduce manual work while keeping the final governance decision with a human reviewer.

## How it works

1. **Upload a document** — PDF or supported document.
2. **Extract evidence** — document content is processed and relevant sections are retrieved.
3. **Identify candidate CDEs** — the AI finds data elements supported by the source evidence.
4. **Evaluate criteria** — candidates are assessed against:
   - OUTPUT
   - CALCULATION
   - IDENTIFICATION / LINKING
   - OWNERSHIP / AGGREGATION
   - VALIDATION / RECONCILIATION
5. **Validate evidence** — a separate validation step checks whether the claimed criteria are actually supported by the evidence.
6. **Human review** — the reviewer can confirm, reject, or request further investigation.
7. **Export** — governance decisions can be captured in the governance register / CSV.

## Guardrails

- Uses only evidence supplied from the document.
- Does not intentionally invent data elements or supporting evidence.
- Separates candidate discovery from evidence validation.
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
- Groq (`openai/gpt-oss-120b`)
- ChromaDB
- Pydantic
- PyMuPDF
- Sentence Transformers
- Pandas

## Project Structure

```text
CDE-Governance-Agent/
├── src/
│   ├── agent/
│   ├── guardrails/
│   ├── ingestion/
│   ├── retrieval/
│   └── llm/
├── ui/
│   └── app.py
├── data/
│   ├── documents/
│   └── chroma_db/
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
```

Create a `.env` file containing:

```text
GROQ_API_KEY=your_api_key_here
```

Then run:

```bash
streamlit run ui/app.py
```

## Disclaimer

This is a decision-support prototype. AI-generated results should be reviewed by appropriate data-governance professionals before being used for formal regulatory, compliance, or business decisions.
