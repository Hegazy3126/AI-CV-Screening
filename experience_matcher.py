from experience_extractor import extract_experience


# =========================
# CV
# =========================

cv_text = """
Sales Representative
Work Experience

Sales Representative — TOWN TEAM
6 Months | Fashion & Clothing Retail
"""


# =========================
# Job Description
# =========================

job_description = """
We are looking for a Sales Representative.

Requirements:
- Minimum 1 year of sales experience
- Customer service experience
- Communication skills
"""


# =========================
# Extract CV Experience
# =========================

cv_experience_months = extract_experience(cv_text)


# =========================
# Extract Required Experience
# =========================

import re

match = re.search(
    r'(?:minimum|required|at least)\s+(\d+(?:\.\d+)?)\s*(years?|months?)',
    job_description.lower()
)

if match:

    required_value = float(match.group(1))
    required_unit = match.group(2)

    if "year" in required_unit:
        required_experience_months = required_value * 12
    else:
        required_experience_months = required_value

else:
    required_experience_months = 0


# =========================
# Calculate Match
# =========================

if required_experience_months > 0:

    experience_match = (
        cv_experience_months /
        required_experience_months
    ) * 100

    experience_match = min(experience_match, 100)

else:
    experience_match = 100


# =========================
# Result
# =========================

print("===== EXPERIENCE MATCH =====")

print(
    "CV Experience:",
    cv_experience_months,
    "months"
)

print(
    "Required Experience:",
    required_experience_months,
    "months"
)

print(
    "Experience Match:",
    round(experience_match, 2),
    "%"
)