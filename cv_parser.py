
import pymupdf


def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)

    try:
        text = ""

        for page in doc:
            text += page.get_text()

        return text

    finally:
        doc.close()


if __name__ == "__main__":
    pdf_path = "test_cvs/mohamed_cv.pdf.pdf"

    cv_text = extract_text_from_pdf(pdf_path)

    print("===== CV TEXT =====")
    print(cv_text)