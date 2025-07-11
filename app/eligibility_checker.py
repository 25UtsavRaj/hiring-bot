def evaluate_candidate_answers(answers: dict, jd_text: str) -> dict:
    """
    Compares candidate answers with hardcoded or inferred eligibility.
    """

    reasons = []

    # Simple rule-based eligibility
    if 'postgraduate' in answers:
        if answers['postgraduate'].lower() not in ['yes', 'y']:
            reasons.append("Postgraduate degree is required")

    if 'experience' in answers:
        try:
            experience = float(answers['experience'].replace("years", "").strip())
            if experience < 0.75:  # ~9 months
                reasons.append("Minimum 9 months of experience required")
        except:
            reasons.append("Invalid experience format")

    if 'bike' in answers:
        if answers['bike'].lower() not in ['yes', 'y']:
            reasons.append("Two-wheeler is mandatory for field role")

    if 'field_work' in answers:
        if answers['field_work'].lower() not in ['yes', 'y']:
            reasons.append("Field travel is mandatory")

    if 'travel' in answers:
        if answers['travel'].lower() not in ['yes', 'y']:
            reasons.append("Willingness to travel required")

    # Final Decision
    status = "Shortlisted" if len(reasons) == 0 else "Rejected"

    return {
        "status": status,
        "reason": " | ".join(reasons) if reasons else "Eligible"
    }
