import re


def extract_experience(text):

    text = text.lower()

    # Get only the Work Experience section
    if "work experience" in text:
        text = text.split("work experience", 1)[1]

    # Stop before the next major section
    sections = [
        "key skills",
        "career objective",
        "languages",
        "personal skills"
    ]

    for section in sections:
        if section in text:
            text = text.split(section, 1)[0]

    total_months = 0

    # Find months
    month_matches = re.findall(
        r'(\d+)\s*months?',
        text
    )

    for months in month_matches:
        total_months += int(months)

    # Find years
    year_matches = re.findall(
        r'(\d+(?:\.\d+)?)\s*years?',
        text
    )

    for years in year_matches:
        total_months += float(years) * 12

    return total_months


if __name__ == "__main__":

    from cv_parser import extract_text_from_pdf

    pdf_path = "test_cvs/mohamed_cv.pdf.pdf"

    cv_text = extract_text_from_pdf(pdf_path)

    experience_months = extract_experience(cv_text)

    experience_years = experience_months / 12

    print("===== EXPERIENCE EXTRACTION =====")

    print(
        "Experience:",
        round(experience_years, 2),
        "years"
    )

    print(
        "Experience:",
        round(experience_months, 2),
        "months"
    )