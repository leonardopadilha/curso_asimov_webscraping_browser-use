import asyncio
from browser_use import Agent, ChatOpenAI

llm = ChatOpenAI(
    model="gpt-5-mini"
)

task = """
Navegue para https://httpbin.org/forms/post e preencha o formulário de contato com:

- Customer name: Aluno Asimov
- Telephone: 555-123-456
- Pizza Size: "Large"
- Pizza Toppings:  "Bacon", "Onion"
- Preferred delivery time: 15:00
- Delivery instructions: "Seja rápido!"

Em seguida, envie o formulário e me diga qual resposta você recebeu.
"""

async def main():
    agent = Agent(
        llm=llm,
        task=task
    )

    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())