
import re

from pathlib import Path


EDUCATION_KEYWORDS = [
    "computer science",
    "computer engineering",
    "information technology",
    "information systems",
    "business administration",
    "accounting",
    "engineering",
    "bachelor",
    "master",
    "phd",
    "doctorate",
    "mba",
    "university",
    "college",
    "diploma",
    "associate degree",
]

DEGREE_PATTERNS = {
    "PHD": r"\b(ph\.?\s*d|doctorate|doctoral)\b",
    "MASTER": r"\b(master'?s?|m\.?\s*sc\.?|mba)\b",
    "BACHELOR": r"\b(bachelor'?s?|b\.?\s*sc\.?)\b",
    "DIPLOMA": r"\b(diploma|associate degree)\b",
}


def extract_education(text):
    """Extract education-related keywords from text."""

    text = str(text).lower()
    found_education = []

    for keyword in EDUCATION_KEYWORDS:
        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, text):
            found_education.append(keyword)

    return found_education


def extract_degree_level(text):
    """Detect degree terms mentioned in text."""

    text = str(text).lower()
    found_degrees = []

    for degree, pattern in DEGREE_PATTERNS.items():
        if re.search(pattern, text):
            found_degrees.append(degree)

    return found_degrees


if __name__ == "__main__":

    # Test 1: Known example to verify the extractor
    sample_text = """
    Education:
    Bachelor's degree in Business Administration.
    """

    print("=" * 45)
    print("TEST 1: SAMPLE TEXT")
    print("=" * 45)
    print("Education:", extract_education(sample_text))
    print("Degree:", extract_degree_level(sample_text))

    # Test 2: Read the actual CV, if available
    pdf_path = Path("test_cvs/mohamed_cv.pdf.pdf")

    print("\n" + "=" * 45)
    print("TEST 2: ACTUAL CV")
    print("=" * 45)

    if pdf_path.exists():
        try:
            from cv_parser import extract_text_from_pdf

            cv_text = extract_text_from_pdf(str(pdf_path))

            print("PDF text length:", len(cv_text))
            print("Education:", extract_education(cv_text))
            print("Degree:", extract_degree_level(cv_text))

            if not extract_education(cv_text):
                print(
                    "No education keywords found in this CV. "
                    "This is expected if the CV has no education section."
                )

        except Exception as error:
            print("Could not read PDF:", error)
    else:
        print("CV file not found:", pdf_path)