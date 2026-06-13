from utils.llm_config import LLMConfig
from browser_use import ChatOpenAI
from models.link import Link
from logging import Logger
import asyncio
from typing import Any
from browser_use import AgentHistoryList
from models.book import Book
from browser_use import Browser
from database.database import save_book, save_book_parsed
from browser_use import Agent
from tools.tools import basic_extraction_tools
from models.usage import Usage
from pydantic import ValidationError
from database.database import save_usage


CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

book_task = """
Agora você está numa página com as informações sobre um único livro.

* Extraia os dados de um único livro na página atual.
* Só gere saída com as informações sobre livro.

Dados do livro a serem extraídos:
    - title
    - description
    - upc
    - price_incl_tax
    - price_excl_tax
    - tax
    - availability
    - number_of_reviews
"""

llm_config = LLMConfig(
    llm=ChatOpenAI(model="o3"),
    page_extraction_llm=ChatOpenAI(model="gpt-5-mini"),
    fallback_llm=ChatOpenAI(model="gpt-5"),
    judge_llm=ChatOpenAI(model="gpt-5"),
    flash_mode=True,
    use_vision=True,
    max_failures=2,
)

async def extract_book_info(
    browser: Browser,
    logger: Logger
) -> tuple[Book | None, AgentHistoryList[Any]]:
    agent: Agent = Agent(
        task = book_task,
        browser = browser,

        # config do LLM
        llm = llm_config.llm,
        page_extraction_llm = llm_config.page_extraction_llm,
        fallback_llm = llm_config.fallback_llm,
        judge_llm = llm_config.judge_llm,
        flash_mode = llm_config.flash_mode,
        use_vision = llm_config.use_vision,
        max_failures = llm_config.max_failures,

        # tools
        tools = basic_extraction_tools,
        output_model_schema = Book,
        calculate_cost = True
    )

    history = await agent.run()

    if history.usage:
        save_usage(Usage(task_name="extract_book_info", summary=history.usage))

    if not history.is_successful():
        logger.error("extract_book_info: modelo não teve sucesso.")
        return None, history
    
    try:
        output = history.get_structured_output(output_model=Book)
        logger.info(f"extract_book_info: STRUCTURED_OUTPUT \n\n{output}\n")
        return output, history
    except ValidationError as error:
        logger.error(f"extract_book_info: ERRO DE VALIDAÇÃO \n\n{error}\n")
        return None, history

async def parse_book(link: Link, logger: Logger) -> bool:
    browser = Browser(
        channel="chrome",
        headless=True,
        keep_alive=False,
        executable_path=CHROME_PATH,
        minimum_wait_page_load_time=2,
    )

    await browser.start()
    logger.info(f"parse_book: navegando para {link.url}")

    await browser.navigate_to(url=link.url)
    await asyncio.sleep(3)

    if not await browser.get_current_page_title():
        logger.error(f"parse_book: página do livro demorou muito para carregar\n\n{link.url}\n\n")
        return False

    book, history = await extract_book_info(browser=browser, logger=logger)
    await browser.stop()

    steps = history.number_of_steps()

    if not book:
        logger.error(f"parse_book: falha na extração de livro (steps {steps}) em: {link.url}")
        return False

    save_book(book=book)
    save_book_parsed(link=link)

    logger.info(f"parse_book: livro {book.title} salvo (steps {steps}) de : {link.url} ")
    return True

    



