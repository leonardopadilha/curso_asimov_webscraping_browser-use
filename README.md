# Browser Use - Exemplos

Este projeto contém exemplos simples de automação de navegador usando a biblioteca `browser-use` com um modelo da OpenAI.

Os scripts demonstram como criar um agente capaz de navegar pela web, realizar buscas e preencher formulários automaticamente a partir de uma instrução em linguagem natural.

## Arquivos do Projeto

- `exemplo1.py`: faz uma busca no Google para descobrir o valor atual do dólar em reais.
- `exemplo2.py`: acessa um formulário de exemplo no site `httpbin.org`, preenche os campos e envia a resposta.
- `exemplo2_prompt_detalhado.py`: versão mais detalhada do exemplo de preenchimento de formulário, usando atributos HTML como referência.
- `requirements.txt`: lista as dependências Python do projeto.
- `.gitignore`: ignora `.env` e `.venv`.

## Pré-requisitos

- Python instalado.
- Uma chave de API compatível com o modelo usado em `ChatOpenAI`.
- Navegadores e dependências necessárias para execução do `browser-use`.

## Instalação

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Configure sua chave de API em um arquivo `.env` ou como variável de ambiente:

```env
OPENAI_API_KEY=sua_chave_aqui
```

## Como Executar

Para rodar o exemplo de busca do dólar:

```powershell
python exemplo1.py
```

Para rodar o exemplo de preenchimento de formulário:

```powershell
python exemplo2.py
```

Para rodar a versão com prompt mais detalhado:

```powershell
python exemplo2_prompt_detalhado.py
```

## Observações

Os exemplos usam o modelo `gpt-5-mini`, definido diretamente nos arquivos Python:

```python
llm = ChatOpenAI(
    model="gpt-5-mini"
)
```

Caso queira usar outro modelo, altere o valor de `model` nos scripts.
