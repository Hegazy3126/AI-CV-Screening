
import re

from education_extractor import (
    extract_education,
    extract_degree_level,
)


RELATED_FIELDS = {
    "computer science",
    "computer engineering",
    "information technology",
    "information systems",
    "business administration",
    "accounting",
}


def normalize_text(text):
    return re.sub(r"\s+", " ", str(text).lower()).strip()


def find_fields(text):
    """Return recognized study fields explicitly mentioned in text."""
    text = normalize_text(text)
    found = set()

    for field in RELATED_FIELDS:
        pattern = r"\b" + re.escape(field) + r"\b"

        if re.search(pattern, text):
            found.add(field)

    return found


def match_education(cv_text, job_description):
    cv_education = extract_education(cv_text)
    job_education = extract_education(job_description)

    cv_fields = find_fields(cv_text)
    job_fields = find_fields(job_description)

    cv_degree_list = extract_degree_level(cv_text)
    job_degree_list = extract_degree_level(job_description)

    cv_degree = cv_degree_list[0] if cv_degree_list else None
    required_degree = (
        job_degree_list[0] if job_degree_list else None
    )

    # No education requirement detected in the job description
    if not job_education:
        status = "NOT REQUIRED"

    # Education is missing from the CV
    elif not cv_education:
        status = "NOT AVAILABLE"

    # The CV mentions a recognized field, but it does not match
    # any of the explicitly listed required fields.
    elif job_fields and cv_fields and not (job_fields & cv_fields):
        status = "NOT MATCHED"

    # We cannot establish a field match from the available text
    elif not cv_fields or not job_fields:
        status = "NEEDS REVIEW"

    # A degree level is required, but it cannot be identified in CV
    elif required_degree and not cv_degree:
        status = "NEEDS REVIEW"

    # A bachelor's degree or higher is accepted for a bachelor-level
    # requirement by this simple rule-based matcher.
    elif required_degree == "BACHELOR":
        if cv_degree in {"BACHELOR", "MASTER", "PHD"}:
            status = "MATCHED"
        else:
            status = "NOT MATCHED"

    # Avoid assuming that different degree levels are equivalent
    elif required_degree and cv_degree != required_degree:
        status = "NEEDS REVIEW"

    # A recognized field and the required degree level were detected
    else:
        status = "MATCHED"

    return {
        "status": status,
        "cv_education": cv_education,
        "job_education": job_education,
        "cv_degree": cv_degree,
        "required_degree": required_degree,
    }


if __name__ == "__main__":
    job_description = """
    Education Requirements:
    Bachelor's degree in Business Administration,
    Computer Science, or a related field.
    """

    test_cases = [
        (
            "Matching education",
            """
            Education:
            Bachelor's degree in Business Administration.
            """,
        ),
        (
            "Different field",
            """
            Education:
            Bachelor's degree in Accounting.
            """,
        ),
        (
            "Education missing",
            """
            Work Experience:
            Sales Representative for 12 months.
            """,
        ),
        (
            "Field mentioned without degree",
            """
            Education:
            Studied Business Administration.
            """,
        ),
    ]

    for name, cv_text in test_cases:
        result = match_education(cv_text, job_description)

        print("\n" + "=" * 45)
        print(name)
        print("CV Education:", result["cv_education"])
        print("CV Degree:", result["cv_degree"])
        print("Required Degree:", result["required_degree"])
        print("Status:", result["status"])