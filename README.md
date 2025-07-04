# 🤖 Concursy Agente — Gerador de Questões com IA

Este projeto utiliza a biblioteca [CrewAI](https://github.com/crewAIInc/crewAI) para orquestrar agentes de inteligência artificial capazes de gerar questões de prova com base em um tema e nível de dificuldade definidos.

---

## 🚀 O que o projeto faz

- Recebe um tema (ex: Fotossíntese) e um nível de dificuldade (ex: fácil)
- Cria agentes com papéis específicos:
  - **Especialista** no tema
  - **Gerador de questão** com alternativas
  - **Revisor pedagógico**
- Gera uma questão com 4 alternativas e resposta correta

---

## 🧱 Tecnologias utilizadas

- Python 3.11+
- [CrewAI](https://github.com/joaomdmoura/crewai)
- [LangChain](https://www.langchain.com/)
- [OpenAI API](https://platform.openai.com/)

---

## 📦 Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/concursy-agente.git
cd concursy-agente
````

2. (Opcional) Crie um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuração da API

Crie um arquivo `.env` na raiz do projeto com a seguinte variável:

```env
OPENAI_API_KEY=sua-chave-aqui
```

---

## ▶️ Executando

```bash
python3 index.py
```

Você verá no terminal o passo a passo dos agentes e o resultado final da questão gerada.

---

## 🛠 Próximos passos (ideias)

* Criar interface web com Gradio ou Streamlit
* Salvar questões em planilhas ou em um banco de dados
* Escolher matérias, temas e níveis via formulário

---

Feito com 🍺.
