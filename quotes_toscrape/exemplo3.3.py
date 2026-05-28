import asyncio
from browser_use import Agent, ChatOpenAI, Tools, ActionResult
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
    1 - Acesse https://quotes.toscrape.com/ e extraia as seguintes informações:
        - As 5 primeiras citações da página
        - O autor de cada citação
        - As tags associadas a cada citação
    2 - Use a ferramenta 'save_final_result' para salvar o resultado final em arquivo.
"""

tools: Tools = Tools()

@tools.action(description="Salva o resultado final na forma de arquivo.", param_model=QuoteList)
def save_final_result(final_result: QuoteList)->ActionResult:

    if not final_result:
        return ActionResult(
            extracted_content="A tarefa falhou: final_result não tem citações.",
            is_done=False,
            success=False,
        )

    if not len(final_result.quotes) == 5:
        return ActionResult(
            extracted_content="A tarefa falhou: final_result deve ter exatamente 5 citações.",
            is_done=False,
            success=False,
        )

    with open("database.json", "w") as f:
        f.write(final_result.model_dump_json(indent=4, ensure_ascii=False))
        return ActionResult(
            extracted_content="A tarefa foi concluída com sucesso.",
            is_done=True,
            success=True,
        )


async def run_agent():
    agent: Agent = Agent(
        task=task, 
        llm=llm, 
        output_model_schema=QuoteList, 
        calculate_cost=True,
        tools=tools
    )

    history = await agent.run()

    print("Número de STEPS: ", history.number_of_steps())
    print("Número de Actions: ", len(history.action_names()))
    print("Uso dos tokens e custo: ", history.usage)
    print("Duração total (segundos): ", history.total_duration_seconds())

async def main():
    await run_agent()

if __name__ == "__main__":
    asyncio.run(main())