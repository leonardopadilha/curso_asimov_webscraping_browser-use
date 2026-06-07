import asyncio
from logging import Logger
from browser_use import Browser
from models.link import Link, LinkList
from urllib.parse import urljoin
from database.database import *

async def extract_catalog_links(browser: Browser, logger: Logger) -> LinkList | None:
    page = await browser.get_current_page()
    if not page:
        logger.error(f"extract_catalog_links: Page é None")
        return None

    url = await page.get_url()

    while True:
        ready_state = await page.evaluate('() => document.readyState')
        if ready_state == "complete":
            logger.info(f"extract_catalog_links: página de catálogo carregada completamente: {url}")
            break
        logger.info(f"extract_catalog_links: esperando página de catálogo carregar completamente: {url}")
        await asyncio.sleep(1)

    books_elements = await page.get_elements_by_css_selector("article.product_pod h3 a")

    links: list[Link] = []

    for el in books_elements:
        href = await el.get_attribute("href")
        if not href:
            continue

        full_url = urljoin(url, href)
        links.append(Link(url=full_url))

    return LinkList(links=links)

async def parse_catalog(link: Link, logger: Logger, browser: Browser) -> LinkList | None:
    data = await extract_catalog_links(browser=browser, logger=logger)

    if not data:
        logger.error(f"parse_catalog: falha na extração de links em {link.url}")
        save_catalog_failed(link=link)
        return None

    logger.info(f"parse_catalog: total de {len(data.links)} links extraídos de {link.url}")

    save_catalog_parsed(link=link)
    return data