from skill_extractor import extract_skills


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


skills = extract_skills(job_description)

print("===== REQUIRED JOB SKILLS =====")

for skill in skills:
    print("-", skill)