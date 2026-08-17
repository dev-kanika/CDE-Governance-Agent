questions = [
    # Should retrieve strong evidence
    {
        "question": "What is the primary key for the depositor data record?",
        "expected": "relevant",
    },
    {
        "question": "What field is used to identify a deposit account?",
        "expected": "relevant",
    },
    {
        "question": "What information does the Account File contain?",
        "expected": "relevant",
    },
    {
        "question": "What are the ownership right and capacity categories?",
        "expected": "relevant",
    },

    # Additional questions
    {
        "question": "What field identifies the ownership right and capacity of an account?",
        "expected": "relevant",
    },
    {
        "question": "What field contains the insured amount?",
        "expected": "relevant",
    },
    {
        "question": "What field contains the uninsured amount?",
        "expected": "relevant",
    },
    {
        "question": "How is the Customer File linked to the Account File?",
        "expected": "relevant",
    },
    {
        "question": "What information is contained in the Account Participant File?",
        "expected": "relevant",
    },
    {
        "question": "What data is used to identify account participants?",
        "expected": "relevant",
    },

    # Should NOT have strong evidence
    {
        "question": "What is the depositor's favorite color?",
        "expected": "irrelevant",
    },
    {
        "question": "What brand of coffee does the bank CEO drink?",
        "expected": "irrelevant",
    },
    {
        "question": "What is the weather in Toronto today?",
        "expected": "irrelevant",
    },
]