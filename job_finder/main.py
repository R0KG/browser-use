import platform
import asyncio
from pathlib import Path
from browser_use.browser.browser import Browser, BrowserConfig
from pydantic import SecretStr
from job_finder.actions import controller
from job_finder.models import Job
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


async def main():
    ground_task = (
        "You are a professional job finder. "
        "1. Read my cv with read_cv"
        "find job according to my cv and save them to a file"
        "search at linkedin and karriere.at:"
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
