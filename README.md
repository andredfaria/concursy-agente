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
- **🆕 Suporte a múltiplos providers de LLM** (OpenAI, Anthropic, Google, Groq, Ollama, HuggingFace)

---

## 🧱 Tecnologias utilizadas

- Python 3.11+
- [CrewAI](https://github.com/joaomdmoura/crewai)
- [LangChain](https://www.langchain.com/)
- **Providers de LLM suportados:**
  - [OpenAI API](https://platform.openai.com/) (GPT-4, GPT-3.5)
  - [Anthropic Claude](https://console.anthropic.com/) (Claude 3)
  - [Google Gemini](https://makersuite.google.com/) (Gemini Pro/Flash)
  - [Groq](https://console.groq.com/) (Llama, Mixtral - rápido e gratuito)
  - [Ollama](https://ollama.ai/) (modelos locais)
  - [HuggingFace](https://huggingface.co/) (vários modelos)

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

### 🚀 Configuração Rápida (OpenAI)

Crie um arquivo `.env` na raiz do projeto com a seguinte variável:

```env
OPENAI_API_KEY=sua-chave-aqui
```

### 🎛️ Configuração Avançada (Múltiplos Providers)

1. **Copie o arquivo de exemplo:**
   ```bash
   cp config_example.env .env
   ```

2. **Configure as API keys dos providers desejados no arquivo `.env`:**
   ```env
   # Provider preferido (opcional)
   PREFERRED_LLM_PROVIDER=openai
   
   # OpenAI
   OPENAI_API_KEY=sua-chave-openai-aqui
   
   # Anthropic Claude (opcional)
   ANTHROPIC_API_KEY=sua-chave-anthropic-aqui
   
   # Google Gemini (opcional)
   GOOGLE_API_KEY=sua-chave-google-aqui
   
   # Groq (opcional - rápido e gratuito)
   GROQ_API_KEY=sua-chave-groq-aqui
   
   # Para modelos locais via Ollama
   OLLAMA_BASE_URL=http://localhost:11434
   ```

3. **Instale os providers desejados:**
   ```bash
   # Execute o configurador interativo
   python setup_providers.py
   
   # Ou instale manualmente:
   pip install langchain-anthropic    # Claude
   pip install langchain-google-genai # Gemini
   pip install langchain-groq         # Groq
   ```

### 🆓 Opções Gratuitas Recomendadas

- **Groq**: Rápido e com tier gratuito generoso
- **Ollama**: Modelos locais, sem API key necessária

---

## ▶️ Executando

```bash
python3 index.py
```

### 🎯 Como Funciona

1. **Na primeira execução**, o sistema mostra os providers disponíveis e permite escolher
2. **Providers configurados** via `PREFERRED_LLM_PROVIDER` são usados automaticamente
3. **Seleção interativa** aparece quando múltiplos providers estão disponíveis

**Exemplo de execução:**
```
🚀 Configurando modelo de LLM...
🤖 Providers de LLM Disponíveis:
--------------------------------------------------
1. OpenAI - ✅ Disponível
   📝 GPT-4, GPT-3.5 e outros modelos da OpenAI
   🔑 API Key (OPENAI_API_KEY): ✅ Configurada

2. Groq - ✅ Disponível
   📝 Modelos rápidos via Groq
   🔑 API Key (GROQ_API_KEY): ✅ Configurada

🎯 Escolha um provider (número):
> 2
✅ Usando: Groq
```

Você verá no terminal o passo a passo dos agentes e o resultado final da questão gerada.

## 🛠️ Utilitários

### Script de Configuração

Execute o configurador interativo para gerenciar providers:

```bash
python setup_providers.py
```

**Funcionalidades:**
- 📦 Instalar providers automaticamente
- 🧪 Testar configuração de API keys
- 📖 Ver informações detalhadas dos providers
- 📝 Criar arquivo `.env` básico

---

## 🛠 Próximos passos

### 🤖 Melhorias de IA
* ✅ **Múltiplos providers de LLM** (OpenAI, Anthropic, Google, Groq, Ollama)
* Sistema de fallback automático entre providers
* Configuração de modelos específicos por provider
* Análise de custo por provider

### 🎯 Funcionalidades
* Criar interface web com Gradio ou Streamlit
* Salvar questões em planilhas ou em um banco de dados
* Escolher matérias, temas e níveis via formulário
* Sistema de templates de prova personalizáveis

### 📚 Conteúdo
* Integração com RAG para carregar editais em PDF
* Banco de questões de provas anteriores
* Análise de padrões de questões por banca

---

Feito com 🍺.
