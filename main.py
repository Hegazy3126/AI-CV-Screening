
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from cv_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from experience_extractor import extract_experience
from education_matcher import match_education


# ==========================================
# 1. Settings
# ==========================================

CV_FOLDER = Path("test_cvs")
REQUIRED_EXPERIENCE_MONTHS = 12

WEIGHTS = {
    "skills": 0.50,
    "experience": 0.20,
    "semantic": 0.20,
    "education": 0.10,
}

print("Loading AI model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================
# 2. Job Description
# ==========================================

job_description = """
We are looking for a Sales Representative.

Requirements:
- Sales
- Customer Service
- Communication
- Negotiation
- Persuasion
- Customer Needs Analysis
- Objection Handling
- Closing Sales
- Target Achievement
- Product Presentation
- Teamwork
- Problem Solving

Education Requirements:
Bachelor's degree in Business Administration,
Computer Science, or a related field.

Minimum 1 year of experience.
"""

job_skills = extract_skills(job_description)

if not job_skills:
    raise ValueError("No job skills were found.")


# ==========================================
# 3. Find CV Files
# ==========================================

if not CV_FOLDER.exists():
    raise FileNotFoundError(
        f"CV folder not found: {CV_FOLDER.resolve()}"
    )

pdf_files = sorted(CV_FOLDER.glob("*.pdf"))

if not pdf_files:
    raise FileNotFoundError(
        f"No PDF files found in {CV_FOLDER.resolve()}"
    )

results = []


# ==========================================
# 4. Education Score Helper
# ==========================================

def get_education_score(status):
    """
    Returns None when education cannot be evaluated.
    This prevents missing information from being
    treated automatically as a pass or a failure.
    """

    status = str(status).strip().upper()

    if status == "MATCHED":
        return 100.0

    if status == "NOT MATCHED":
        return 0.0

    if status == "NEEDS REVIEW":
        return 50.0

    return None


# ==========================================
# 5. Analyze Each CV
# ==========================================

for pdf_path in pdf_files:

    print(f"\nAnalyzing: {pdf_path.name}")

    try:
        cv_text = extract_text_from_pdf(str(pdf_path))

        if not cv_text or not cv_text.strip():
            print("Skipped: PDF contains no extractable text.")
            continue

        # ----- Skills -----

        cv_skills = extract_skills(cv_text)

        matched_skills = [
            skill for skill in job_skills
            if skill in cv_skills
        ]

        missing_skills = [
            skill for skill in job_skills
            if skill not in cv_skills
        ]

        skills_score = (
            len(matched_skills) / len(job_skills)
        ) * 100

        # ----- Experience -----

        experience_months = extract_experience(cv_text)

        experience_score = min(
            experience_months
            / REQUIRED_EXPERIENCE_MONTHS * 100,
            100.0
        )

        # ----- Education -----

        education_result = match_education(
            cv_text,
            job_description
        )

        education_status = education_result.get(
            "status", "NEEDS REVIEW"
        )

        education_score = get_education_score(
            education_status
        )

        cv_education = education_result.get(
            "cv_education", []
        )

        # ----- Semantic Similarity -----

        embeddings = model.encode(
            [cv_text, job_description],
            normalize_embeddings=True
        )

        similarity = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        semantic_score = max(
            0.0,
            min(float(similarity) * 100, 100.0)
        )

        # ----- Final Score -----
        # If education is unavailable, exclude its weight
        # and normalize using the remaining weights.

        components = {
            "skills": skills_score,
            "experience": experience_score,
            "semantic": semantic_score,
        }

        if education_score is not None:
            components["education"] = education_score

        active_weight = sum(
            WEIGHTS[name] for name in components
        )

        final_score = sum(
            components[name] * WEIGHTS[name]
            for name in components
        ) / active_weight

        results.append({
            "filename": pdf_path.name,
            "matched": matched_skills,
            "missing": missing_skills,
            "experience": experience_months,
            "skills_score": skills_score,
            "experience_score": experience_score,
            "semantic_score": semantic_score,
            "education_score": education_score,
            "education_status": education_status,
            "education": cv_education,
            "final_score": final_score,
        })

    except Exception as error:
        print(f"Could not analyze {pdf_path.name}: {error}")


# ==========================================
# 6. Rank Candidates
# ==========================================

results.sort(
    key=lambda item: item["final_score"],
    reverse=True
)


# ==========================================
# 7. Display Report
# ==========================================

print("\n" + "=" * 55)
print("             AI CV SCREENING REPORT")
print("=" * 55)

if not results:
    print("No CVs could be analyzed.")

for rank, result in enumerate(results, start=1):

    print("\n" + "-" * 55)
    print(f"RANK #{rank}: {result['filename']}")
    print("-" * 55)

    print(f"Final Ranking Score: {result['final_score']:.2f}%")
    print(f"Skills Score: {result['skills_score']:.2f}%")
    print(f"Experience: {result['experience']} months")
    print(
        f"Experience Score: "
        f"{result['experience_score']:.2f}%"
    )
    print(
        f"Semantic Similarity: "
        f"{result['semantic_score']:.2f}%"
    )

    print("\nEDUCATION")
    print("Status:", result["education_status"])

    if result["education_score"] is None:
        print("Education Score: Not evaluated")
    else:
        print(
            f"Education Score: "
            f"{result['education_score']:.2f}%"
        )

    education = result["education"]

    if isinstance(education, (list, tuple, set)):
        education_text = ", ".join(map(str, education))
    else:
        education_text = str(education) if education else ""

    print("CV Education:", education_text or "Not available")

    print("\nMATCHED SKILLS")
    print(", ".join(result["matched"]) or "None")

    print("\nMISSING SKILLS")
    print(", ".join(result["missing"]) or "None")

print("\n" + "=" * 55)
print("IMPORTANT NOTES")
print("- Scores are experimental ranking scores, not")
print("  probabilities of being hired.")
print("- Education scores depend on the current rule-based")
print("  education matcher and may need manual review.")
print("- Candidates should not be rejected automatically")
print("  based only on these experimental scores.")
print("=" * 55)