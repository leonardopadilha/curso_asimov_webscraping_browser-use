import asyncio
from browser_use import Agent, ChatOpenAI
from pydantic import BaseModel, Field

llm = ChatOpenAI(
    model="gpt-5-mini"
)

class Tag(BaseModel):
    text: str = Field(description="Texto de uma única tag.")

class Quote(BaseModel):
    text: str = Field(description="Texto da citação.")
    author: str = Field(description="Autor da citação.")
    tags: list[Tag] = Field(description="Lista de Tags.")

class QuoteList(BaseModel):
    quotes: list[Quote] = Field(description="Lista de citações.")

task = """
    Acesse https://quotes.toscrape.com/ e extraia as seguintes informações:
        - As 5 primeiras citações da página
        - O autor de cada citação
        - As tags associadas a cada citação
"""

async def run_agent() -> QuoteList | None:
    agent: Agent = Agent(task=task, llm=llm, output_model_schema=QuoteList, calculate_cost=True)
    history = await agent.run()

    print("Número de STEPS: ", history.number_of_steps())
    print("Número de Actions: ", len(history.action_names()))
    print("Uso dos tokens e custo: ", history.usage)
    print("Duração total (segundos): ", history.total_duration_seconds())

    return history.get_structured_output(output_model=QuoteList)


async def main():
    result = await run_agent()
    if result:
        for quote in result.quotes:
            print(f"Texto: {quote.text}")
            print(f"Autor: {quote.author}")
            print(f"TAGS: {quote.tags}")

if __name__ == "__main__":
    asyncio.run(main())