from cde_extractor import retrieve_evidence, analyze_cdes
from guardrails.evidence_validator import validate_candidates


def run_agent(question):

    print("\n🔎 Retrieving evidence...")
    evidence = retrieve_evidence(
        question,
        n_results=5
    )

    print(f"Retrieved {len(evidence)} evidence chunks.")

    print("\n🧠 Analyzing candidates...")
    result = analyze_cdes(
        question,
        evidence
    )

    print(f"Found {len(result.candidates)} candidate(s).")

    print("\n🛡️ Validating candidates...")
    validations = validate_candidates(
        result.candidates
    )

    return result, validations


def display_results(validations):

    print("\n")
    print("=" * 60)
    print("CDE GOVERNANCE ANALYSIS")
    print("=" * 60)

    for validation in validations.validations:

        print("\n" + "-" * 60)

        print(f"Candidate: {validation.name}")

        if validation.supported:
            print("Status: SUPPORTED CANDIDATE")
        else:
            print("Status: REQUIRES REVIEW")

        print("\nSupported Criteria:")

        if validation.supported_claims:
            for criterion in validation.supported_claims:
                print(f"  ✓ {criterion}")
        else:
            print("  None")

        if validation.unsupported_claims:
            print("\nUnsupported Claims:")
            for criterion in validation.unsupported_claims:
                print(f"  ✗ {criterion}")

        print("\nCorrected Reason:")
        print(f"  {validation.corrected_reason}")

    print("\n" + "=" * 60)
    print("Note: Final CDE designation is a human governance decision.")
    print("=" * 60)


if __name__ == "__main__":

    print("=" * 60)
    print("CDE GOVERNANCE AGENT")
    print("=" * 60)

    question = input("\nEnter your governance question:\n> ").strip()

    if not question:
        print("\n❌ Please enter a question.")
        raise SystemExit(1)

    result, validations = run_agent(question)

    display_results(validations)