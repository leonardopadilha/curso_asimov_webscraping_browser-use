import asyncio
from config import BASE_URL
from browser_use import Browser
from database.database import create_table
from logs.books_logger import books_logger

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

async def main():
    logger = books_logger()

    browser = Browser(
        channel="chrome",
        headless=False,
        keep_alive=False,
        executable_path=CHROME_PATH,
        minimum_wait_page_load_time=2
    )

    await browser.start()
    await browser.navigate_to(url=BASE_URL)

    logger.info(f"main: carregando a página principal de {BASE_URL}")

    create_table()

if __name__ == "__main__":
    asyncio.run(main())
