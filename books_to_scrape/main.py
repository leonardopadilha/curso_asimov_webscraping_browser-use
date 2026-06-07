import asyncio
from config import BASE_URL
from models.link import Link
from browser_use import Browser
from database.database import create_table
from logs.books_logger import books_logger
from tasks.extract_catalog import parse_catalog
from actions.go_next import got_next_page

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

    max_catalog_extraction = 3
    total_catalog_extraction = 0
    total_pages = 0

    while max_catalog_extraction > 0:
        url = await browser.get_current_page_url()
        link = Link(url=url)

        logger.info(f"main próximo link do catálogo para verificar: {url}")
        data = await parse_catalog(link=link, logger=logger, browser=browser)
        if data:
            max_catalog_extraction -= 1
            total_catalog_extraction += len(data.links)
            total_pages += 1
            logger.info(f"main: páginas de catálogo processadas até agora: {total_pages}")

        if not await got_next_page(browser=browser):
            break

    logger.info(f"main: total de links extraídos: {total_catalog_extraction}")

    await browser.stop()

if __name__ == "__main__":
    asyncio.run(main())
