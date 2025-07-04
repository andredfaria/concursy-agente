from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Verificar se a chave da OpenAI está configurada
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("❌ OPENAI_API_KEY não encontrada! Crie um arquivo .env com sua chave da OpenAI")

# Configurar o modelo LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",  # Modelo mais econômico e eficiente
    temperature=0.7,      # Criatividade moderada
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Configurações da questão
prova = "CPA-2O"
tema = "Mercado Financeiro"
nivel = "Dificil"
area = "Finanças"

# Especialista em Conteúdo
especialista = Agent(
    role="Especialista em Conteúdo Educacional",
    goal=f"Identificar e estruturar os conceitos fundamentais sobre '{tema}' adequados ao nível {nivel}",
    backstory=f"""Você é um professor experiente com doutorado na área de '{area}'. 
    Tem mais de 20 anos de experiência em concurso da area de '{area}' e é especialista em adaptar conteúdos 
    complexos para diferentes níveis de aprendizado.""",
    verbose=True,
    llm=llm
)

# Gerador de Questões
gerador = Agent(
    role="Criador de Questões de Múltipla Escolha",
    goal="Criar uma questão de múltipla escolha clara, objetiva e pedagogicamente adequada baseada no edital do {prova}",
    backstory="""Você é um especialista em avaliação educacional com formação em Pedagogia. 
    Tem experiência em criar questões para vestibulares e concursos. 
    Conhece as melhores práticas para formulação de questões de múltipla escolha.""",
    verbose=True,
    llm=llm
)

# Revisor Pedagógico
revisor = Agent(
    role="Revisor Pedagógico",
    goal="Garantir a qualidade, clareza e adequação pedagógica da questão finalizada baseada no edital do {prova}",
    backstory="""Você é um pedagogo com especialização em avaliação educacional. 
    Tem experiência em revisar materiais editais de concursos. 
    Seu trabalho é garantir que a questão esteja perfeita antes da aplicação.""",
    verbose=True,
    llm=llm
)

# Tarefas Estruturadas
tarefa_especialista = Task(
    description=f"""
    Analise o tema '{tema}' e identifique os 5 pontos principais que devem ser abordados 
    em uma questão de nível {nivel}. 
    
    Forneça:
    1. Lista dos conceitos fundamentais
    2. Aspectos mais importantes para avaliação
    3. Possíveis conexões com outros temas
    4. Sugestões de enfoque adequado ao nível
    
    Seja específico e educacionalmente relevante.
    """,
    agent=especialista,
    expected_output="Lista estruturada com os pontos principais e orientações pedagógicas"
)

tarefa_gerador = Task(
    description="""
    Com base na análise do especialista, crie uma questão de múltipla escolha seguindo este formato:
    
    QUESTÃO: [Enunciado claro e objetivo]
    
    A) [Alternativa 1]
    B) [Alternativa 2] 
    C) [Alternativa 3]
    D) [Alternativa 4]
    
    RESPOSTA CORRETA: [Letra e justificativa]
    
    Requisitos:
    - Questão clara e sem ambiguidades
    - 4 alternativas plausíveis
    - Apenas uma resposta correta
    - Distratores bem elaborados
    - Linguagem adequada ao nível
    """,
    agent=gerador,
    expected_output="Questão de múltipla escolha completa com 4 alternativas e resposta correta identificada"
)

# Equipe de Criação de Questões
equipe = Crew(
    agents=[especialista, gerador],
    tasks=[tarefa_especialista, tarefa_gerador],
    verbose=True,
    process="sequential"  # Processamento sequencial para dependências
)

# Execução
if __name__ == "__main__":
    print("🎯 Iniciando geração de questão...")
    print(f"📚 Tema: {tema}")
    print(f"📚 Prova: {prova}")
    print(f"📚 Area: {area}")
    print(f"📊 Nível: {nivel}")
    print("-" * 50)
    
    try:
        resultado = equipe.kickoff()
        print("\n" + "="*60)
        print("✅ QUESTÃO FINALIZADA")
        print("="*60)
        print(resultado)
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        print("Verifique se a chave da OpenAI está correta e se há créditos disponíveis.")
