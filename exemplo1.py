import asyncio
from browser_use import Agent, ChatOpenAI

llm = ChatOpenAI(
    model="gpt-5-mini"
)

task = """
Faça uma busca utilizando Google e determine o valor do dólar hoje
em Reais do Brasil.
"""

async def main():
    agent = Agent(
        llm=llm,
        task=task
    )

    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())