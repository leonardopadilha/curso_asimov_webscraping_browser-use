from pydantic import BaseModel, ConfigDict, Field

class Book(BaseModel):
    title: str = Field(description="Título do livro.")
    description: str = Field(description="Descrição do livro")
    upc: str = Field(description="Código Universal de Produto (Universal Product Code)")
    price_incl_tax: str = Field(description="Preço do livro, incluindo taxas")
    price_excl_tax: str = Field(description="Preço do livro, excluindo taxas")
    tax: str = Field(description="Taxas")
    availability: str = Field( description="Disponibilidade do livro (Ex: 'In stock')")
    number_of_reviews: int = Field(description="Número de 'reviews' do livro")

    model_config = ConfigDict(extra="forbid")