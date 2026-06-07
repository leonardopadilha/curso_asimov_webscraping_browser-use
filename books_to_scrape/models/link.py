from pydantic import BaseModel, ConfigDict, Field

class Link(BaseModel):
    url: str = Field(description="Link para detalhes de um livro")
    model_config = ConfigDict(extra="forbid")

class LinkList(BaseModel):
    links: list[Link] = Field(description="Lista de links detalhes de livros")
    model_config = ConfigDict(extra="forbid")