# AI CV Screening System

An AI-powered recruitment tool that analyzes CVs and ranks candidates based on job requirements.

## Features

* Extract text from PDF CVs.
* Extract and match candidate skills against job requirements.
* Evaluate work experience.
* Analyze education using rule-based matching.
* Calculate semantic similarity between CVs and job descriptions.
* Rank candidates using a weighted scoring system.

## Technologies Used

* Python
* Sentence Transformers
* Scikit-learn
* PyMuPDF
* Regular Expressions (Regex)

## Project Structure

| File                      | Description                                  |
| ------------------------- | -------------------------------------------- |
| `main.py`                 | Main screening and ranking pipeline          |
| `cv_parser.py`            | Extracts text from PDF files                 |
| `skill_extractor.py`      | Extracts skills from CVs                     |
| `skill_matcher.py`        | Matches candidate skills to job requirements |
| `job_parser.py`           | Processes job requirements                   |
| `education_extractor.py`  | Extracts education information               |
| `education_matcher.py`    | Evaluates education matches                  |
| `experience_extractor.py` | Extracts work experience                     |
| `experience_matcher.py`   | Evaluates work experience                    |

## How It Works

The system analyzes CVs, matches skills and experience against job requirements, evaluates available education information, calculates semantic similarity, and produces a ranked candidate report.

## Installation

1. Install Python 3.11 or a compatible version.
2. Install the required dependencies.
3. Run the application using:

```bash
python main.py
```

The required dependencies should be documented in `requirements.txt`.

## Important Note

The ranking scores are experimental and do not represent the probability of being hired. Results should be reviewed by a human recruiter.

## Future Improvements

* Add a graphical user interface.
* Evaluate performance on a larger labeled dataset.
* Improve skill extraction and semantic matching.
* Measure Precision, Recall, and F1-score.

## Author

GitHub: [@Hegazy3126](https://github.com/Hegazy3126)
