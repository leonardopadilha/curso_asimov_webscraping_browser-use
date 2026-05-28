import asyncio
from browser_use import Agent, ChatOpenAI

llm = ChatOpenAI(
    model="gpt-5-mini"
)

task = """
    Acesse https://quotes.toscrape.com/ e extraia as seguintes informações:
        - As 5 primeiras citações da página
        - O autor de cada citação
        - As tags associadas a cada citação
    
    Apresente as informações em um formato claro e estruturado, como:

    Quote 1: "[texto da citação]" - Author: [nome do autor] - Tags: [tag1, tag2, ...]
    Quote 2: "[texto da citação]" - Author: [nome do autor] - Tags: [tag1, tag2, ...]
    etc.
"""

async def main():
    agent: Agent = Agent(task=task, llm=llm, calculate_cost=True)
    history = await agent.run()

    print("Número de STEPS: ", history.number_of_steps())
    print("Número de Actions: ", len(history.action_names()))
    print("Uso dos tokens e custo: ", history.usage)
    print("Duração total (segundos): ", history.total_duration_seconds())

if __name__ == "__main__":
    asyncio.run(main())