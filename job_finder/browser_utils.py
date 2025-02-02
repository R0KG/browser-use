import asyncio
import logging

logger = logging.getLogger(__name__)

async def safe_click(element, retries = 3, delay = 1):
    for attempt in range(retries):
        try:
            if await element.is_visible():
                await element.click()
                return True
            else:
                logger.debug(f"Element not visible. Attempt {attempt+1} of {retries}.")
        except Exception as e:
            logger.debug(f"Error on click attempt {attempt+1}: {e}")
        await asyncio.sleep(delay)
    logger.error("Failed to click the element after several attempts.")
    return False


async def safe_upload_file(file, file_path, retries = 3, delay = 1):
    for attempt in range(retries):
        try:
            await file.set_input_files(file_path)
            logger.info(f"File uploaded successfully on attempt {attempt+1}")
            return True
        except Exception as e:
            logger.debug(f"Error on upload attempt {attempt+1}: {e}")
        await asyncio.sleep(delay)
    logger.error("Failed to upload the file after several attempts.")
    return False
