import platform
import asyncio
from pathlib import Path
from browser_use.browser.browser import Browser, BrowserConfig
from pydantic import SecretStr
from browser_use import ActionResult, Agent, Controller
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


controller = Controller()


async def main():
    ground_task = (
        "You are a professional job finder and application assistant. Follow these steps precisely:\n"
        "1. Initial Setup:\n"
        "   - FIRST ACTION: Call the read_cv() function to read my CV\n"
        "   - Store the returned CV content in memory for form filling\n"
        "2. Search Jobs on These Platforms (in order):\n"
        "   a) karriere.at (Fast application)\n"
        "   b) LinkedIn (Fast application)\n"
        "   c) jobs.ams.at/public/emps (Austrian website)\n"
        "   d) stepstone.at (as guest, slower platform)\n"
        "3. For Each Job Posting:\n"
        "   - Extract and evaluate job details\n"
        "   - Save promising positions using save_jobs function\n"
        "   - Check application method:\n"
        "     * If direct form: Fill and submit application\n"
        "     * If email application: Stop and report with format:\n"
        "       - User email: [extracted]\n"
        "       - Apply to email: [company_email]\n"
        "       - Application file needed: [yes/no]\n"
        "       - Save user email and job email to file\n"
        "4. Keep Track:\n"
        "   - Maintain count of jobs processed in memory\n"
        "   - Record which platforms were searched\n"
        "   - Note any failed attempts or errors\n"
        "5. Important Rules:\n"
        "   - Always verify if links are working before processing\n"
        "   - Check for both application methods (form/email) on each posting\n"
        "   - Do not submit duplicate applications\n"
        "   - Save all relevant job details before applying\n"
    )
    tasks = [
        ground_task + "\n" + "Google",
    ]

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")

    if platform.system() == "Windows":
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    elif platform.system() == "Darwin":  # macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    else:  # Linux or others
        chrome_path = "/usr/bin/google-chrome"

    browser = Browser(
        config=BrowserConfig(
            chrome_instance_path=chrome_path,
            disable_security=True,
        )
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp", api_key=SecretStr(api_key)
    )

    agents = []
    # Create an agent for each task
    for task in tasks:
        from browser_use import Agent  # Import Agent here if not imported already

        agent = Agent(task=task, llm=llm, controller=controller, browser=browser)
        agents.append(agent)
        await asyncio.gather(*[agent.run() for agent in agents])


if __name__ == "__main__":
    asyncio.run(main())
