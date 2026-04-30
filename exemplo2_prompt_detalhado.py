import asyncio
from browser_use import Agent, ChatOpenAI

llm = ChatOpenAI(
    model="gpt-5-mini"
)

task = """
Navegue para https://httpbin.org/forms/post e preencha o formulário de contato com:

1 - Para elementos HTML do tipo "input" preencha de acordo com o atributo "name" com o valor dado por "valor":

    * name: custname        valor: Aluno Asimov
    * name: custtel         valor: 555-123-456
    * name: custmail:       valor: aluno.asimov@example.com

2 - Para os elementos HTML do tipo "radio" com atributo "name" com valor "size" marque a opção cujo 
atributo "value" é "large".

3 - Para os elementos HTML do tipo "checkbox" e com o atributo "name" com valor "topping" marque os com "value": 
"bacon", "cheese" e "onion".

4 - Para o elemento HTML do tipo "input" cujo atributo "name" é "delivery" preencha com hora e minuto de agora, mas 
que respeitem os atributos min, max, step. Lembrando que o fuso horário usado deve ser "Brasilia Standard Time".

5 - Para o elemento HTML do tipo "textarea" cujo "name" é "comments", preencha com: 
"Esse é somente um teste do Browser-use".

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