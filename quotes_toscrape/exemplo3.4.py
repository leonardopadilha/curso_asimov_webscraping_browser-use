import asyncio
from browser_use import Agent, ChatOpenAI, Tools, ActionResult
from pydantic import BaseModel, Field

llm = ChatOpenAI(
    model="gpt-5-mini"
)

extract_llm = ChatOpenAI(
    model="gpt-5-nano"
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
Acesse https://quotes.toscrape.com/.

Extraia as 5 primeiras citações visíveis na página inicial, incluindo:
- texto da citação
- autor
- tags associadas

Retorne somente os dados extraídos, sem explicações, sem validações e sem comentários.
Considere a tarefa concluída após a extração.
"""

def save_final_result(final_result: QuoteList):
    with open("database.json", "w") as f:
        f.write(final_result.model_dump_json(indent=4, ensure_ascii=False))


async def run_agent():
    agent: Agent = Agent(
        task=task, 
        llm=llm, 
        page_extraction_llm=extract_llm,
        output_model_schema=QuoteList, 
        calculate_cost=True,
        flash_mode=True
    )

    history = await agent.run()

    quote_list: QuoteList | None = history.get_structured_output(output_model=QuoteList)

    if quote_list:
        save_final_result(quote_list)

    print("Número de STEPS: ", history.number_of_steps())
    print("Número de Actions: ", len(history.action_names()))
    print("Uso dos tokens e custo: ", history.usage)
    print("Duração total (segundos): ", history.total_duration_seconds())

async def main():
    await run_agent()

if __name__ == "__main__":
    asyncio.run(main())