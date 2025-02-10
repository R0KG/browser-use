import csv
from pathlib import Path
from PyPDF2 import PdfReader
import logging
from browser_use import ActionResult, Controller
from job_finder.models import Job
from browser_use.browser.context import BrowserContext

logger = logging.getLogger(__name__)
controller = Controller()

CV = Path.cwd() / "CV.pdf"

if not CV.exists():
    raise FileNotFoundError(f"CV file not found at {CV}")


@controller.action(
    "Save jobs to file - with a score how well it fits to my profile", param_model=Job
)
def save_jobs(job: Job):
    with open("jobs.csv", "a", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([job.title, job.company, job.link, job.salary, job.location])
    return ActionResult(extracted_content="Saved job to file")


@controller.action("Read jobs from file")
def read_jobs():
    with open("jobs.csv", "r") as f:
        return f.read()


@controller.action("Read CV")
def read_cv():
    pdf = PdfReader(CV)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    logger.info(f"Read cv with {len(text)} characters")
    return ActionResult(extracted_content=text, include_in_memory=True)


@controller.action(
    "Upload cv to element - call this function to upload if element is not found, try with different index of the same upload element",
    requires_browser=True,
)
async def upload_cv(index: int, browser: BrowserContext):
    path = str(CV.absolute())
    dom_el = await browser.get_dom_element_by_index(index)
    if dom_el is None:
        return ActionResult(error=f"No element found at index {index}")
    file_upload_dom_el = dom_el.get_file_upload_element()
    if file_upload_dom_el is None:
        logger.info(f"No file upload element found at index {index}")
        return ActionResult(error=f"No file upload element found at index {index}")
    file_upload_el = await browser.get_locate_element(file_upload_dom_el)
    if file_upload_el is None:
        logger.info(f"No file upload element found at index {index}")
        return ActionResult(error=f"No file upload element found at index {index}")
    try:
        await file_upload_el.set_input_files(path)
        msg = f"Successfully uploaded file to index {index}"
        logger.info(msg)
        return ActionResult(extracted_content=msg)
    except Exception as e:
        logger.debug(f"Error in set_input_files: {str(e)}")
        return ActionResult(error=f"Failed to upload file to index {index}")


@controller.action("Save user email and job email to file")
def save_user_email(user_email: str, job_email: str):
    with open("user_email.txt", "w") as f:
        writer = csv.writer(f)
        writer.writerow([user_email, job_email])
    return ActionResult(extracted_content="Saved user email and job email to file")
