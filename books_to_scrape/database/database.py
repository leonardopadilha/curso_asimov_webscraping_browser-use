import os
from tinydb import TinyDB
from config import DATABASE_FILE
from contextlib import contextmanager
from models.link import Link

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

def create_table() -> None:
    if not os.path.exists(DATABASE_FILE):
        with db_session() as db:
            db.table("CATALOG_PARSED_LINK", persist_empty=True) # Links do catalogo que já foram visitados
            db.table("CATALOG_FAILED_LINK", persist_empty=True) # Links do catálogo que falharam

def save_catalog_parsed(link: Link):
    with db_session() as db:
        table = db.table("CATALOG_PARSED_LINK")
        table.insert(link.model_dump())

def save_catalog_failed(link: Link):
    with db_session() as db:
        table = db.table("CATALOG_FAILED_LINK")
        table.insert(link.model_dump())