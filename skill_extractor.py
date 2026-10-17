import re


SKILLS = [
    "sales",
    "customer service",
    "communication",
    "negotiation",
    "persuasion",
    "customer needs analysis",
    "objection handling",
    "closing sales",
    "target achievement",
    "product presentation",
    "teamwork",
    "problem solving",
    "time management",
    "working under pressure",
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "pandas",
    "excel",
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found_skills.append(skill)

    return found_skills


if __name__ == "__main__":
    from cv_parser import extract_text_from_pdf

    pdf_path = "test_cvs/mohamed_cv.pdf.pdf"

    cv_text = extract_text_from_pdf(pdf_path)

    skills = extract_skills(cv_text)

    print("===== EXTRACTED SKILLS =====")

    for skill in skills:
        print("-", skill)