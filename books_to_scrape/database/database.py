import os
from tinydb import TinyDB
from config import DATABASE_FILE
from contextlib import contextmanager
from models.link import Link
from models.book import Book
from models.usage import Usage
from tinydb import Query

@contextmanager
def db_session():
    db = TinyDB(
        DATABASE_FILE,
        ensure_ascii=False,
        indent=4,
        sort_keys=True,
        separators=(',', ': ')
    )

    try:
        yield db
    finally:
        db.close()

def create_tables() -> None:
    if not os.path.exists(DATABASE_FILE):
        with db_session() as db:
            db.table("CATALOG_PARSED_LINK", persist_empty=True) # Links do catalogo que já foram visitados
            db.table("CATALOG_FAILED_LINK", persist_empty=True) # Links do catálogo que falharam
            db.table("USAGE", persist_empty=True) # Resumo dos gastos
            db.table("BOOK", persist_empty=True) # dados de livros extraídos
            db.table("BOOK_LINK", persist_empty=True) # links de livros
            db.table("BOOK_PARSED_LINK", persist_empty=True) # links de livros que já foram extraídos
            db.table("BOOK_FAILED_LINK", persist_empty=True) # links de livros que falharam

def save_catalog_parsed(link: Link):
    with db_session() as db:
        table = db.table("CATALOG_PARSED_LINK")
        table.insert(link.model_dump())

def save_catalog_failed(link: Link):
    with db_session() as db:
        table = db.table("CATALOG_FAILED_LINK")
        table.insert(link.model_dump())

def save_book(book: Book) -> None:
    with db_session() as db:
        table = db.table("BOOK")
        table.insert(book.model_dump())

def save_book_link(link: Link) -> None:
    with db_session() as db:
        table = db.table("BOOK_LINK")
        table.insert(link.model_dump())

def get_book_links() -> list[Link]:
    with db_session() as db:
        table = db.table("BOOK_LINK")
        return [Link(**doc) for doc in table.all()]

def save_book_parsed(link: Link) -> None:
    with db_session() as db:
        table = db.table("BOOK_PARSED_LINK")
        table.insert(link.model_dump())

def save_book_failed(link: Link) -> None:
    with db_session() as db:
        table = db.table("BOOK_FAILED_LINK")
        table.insert(link.model_dump())

def save_usage(usage: Usage) -> None:
    with db_session() as db:
        table = db.table("USAGE")
        table.insert(usage.model_dump())

def is_book_saved(link: Link) -> bool:
    with db_session() as db:
        table = db.table("BOOK_PARSED_LINK")
        query = Query()
        return bool(table.search(query.url == link.url))

def is_catalog_parsed(link: Link) -> bool:
    with db_session() as db:
        table = db.table("CATALOG_PARSED_LINK")
        query = Query()
        return bool(table.search(query.url == link.url))
