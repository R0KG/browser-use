from PyPDF2 import PdfReader
import logging

logger = logging.getLogger(__name__)

CV = "/home/r0/code/browser-use/CV.pdf"


def read_cv():
    pdf = PdfReader(CV)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    logger.info(f"Read cv with {len(text)} characters")
    return text


if __name__ == "__main__":
    print(read_cv())
