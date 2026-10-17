from skill_extractor import extract_skills
from cv_parser import extract_text_from_pdf


# =========================
# 1. Read CV
# =========================

pdf_path = "test_cvs/mohamed_cv.pdf.pdf"

cv_text = extract_text_from_pdf(pdf_path)

cv_skills = extract_skills(cv_text)


# =========================
# 2. Job Description
# =========================

job_description = """
We are looking for a Sales Representative for a telecommunications company.

Requirements:
- Sales experience
- Customer service
- Communication skills
- Negotiation
- Persuasion
- Customer needs analysis
- Objection handling
- Closing sales
- Target achievement
- Product presentation
- Teamwork
- Problem solving
- English language
"""


job_skills = extract_skills(job_description)


# =========================
# 3. Compare Skills
# =========================

matched_skills = []

for skill in job_skills:
    if skill in cv_skills:
        matched_skills.append(skill)


missing_skills = []

for skill in job_skills:
    if skill not in cv_skills:
        missing_skills.append(skill)


# =========================
# 4. Calculate Match
# =========================

if len(job_skills) > 0:
    match_percentage = (
        len(matched_skills) / len(job_skills)
    ) * 100
else:
    match_percentage = 0


# =========================
# 5. Print Result
# =========================

print("===== SKILL MATCH RESULT =====")

print("\nMatched Skills:")

for skill in matched_skills:
    print("-", skill)


print("\nMissing Skills:")

for skill in missing_skills:
    print("-", skill)


print("\nTotal Required Skills:", len(job_skills))
print("Matched Skills:", len(matched_skills))
print("Missing Skills:", len(missing_skills))

print(
    "\nSkill Match Percentage:",
    round(match_percentage, 2),
    "%"
)