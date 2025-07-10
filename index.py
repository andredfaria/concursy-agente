from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv
from llm_config import LLMFactory, LLMProvider

# Carregar variáveis do arquivo .env
load_dotenv()

def select_llm_provider():
    """
    Permite ao usuário selecionar o provider de LLM a ser usado
    
    Returns:
        tuple: (provider_name, llm_instance)
    """
    factory = LLMFactory()
    available_providers = factory.list_available_providers()
    provider_info = factory.get_provider_info()
    
    print("🤖 Providers de LLM Disponíveis:")
    print("-" * 50)
    
    available_list = []
    for i, (provider, is_available) in enumerate(available_providers.items(), 1):
        status = "✅ Disponível" if is_available else "❌ Não instalado"
        info = provider_info[provider]
        
        print(f"{i}. {info['name']} - {status}")
        print(f"   📝 {info['description']}")
        
        if is_available:
            available_list.append(provider)
            if info['requires_api_key']:
                env_var = info['env_var']
                api_key_set = "✅ Configurada" if os.getenv(env_var.split()[0]) else "❌ Não configurada"
                print(f"   🔑 API Key ({env_var}): {api_key_set}")
        else:
            print(f"   📦 Instalar: {info['install_command']}")
        print()
    
    # Se apenas OpenAI estiver disponível, usar automaticamente
    if len(available_list) == 1 and LLMProvider.OPENAI in available_list:
        print(f"🎯 Usando automaticamente: {provider_info[LLMProvider.OPENAI]['name']}")
        return LLMProvider.OPENAI, factory.create_llm(LLMProvider.OPENAI)
    
    # Se nenhum provider estiver disponível
    if not available_list:
        raise RuntimeError("❌ Nenhum provider de LLM está disponível! "
                         "Instale pelo menos um dos providers listados acima.")
    
    # Permitir seleção manual
    while True:
        try:
            print("🎯 Escolha um provider (número):")
            choice = input("> ").strip()
            
            if choice.isdigit():
                choice_idx = int(choice) - 1
                all_providers = list(available_providers.keys())
                
                if 0 <= choice_idx < len(all_providers):
                    selected_provider = all_providers[choice_idx]
                    
                    if selected_provider in available_list:
                        print(f"✅ Usando: {provider_info[selected_provider]['name']}")
                        return selected_provider, factory.create_llm(selected_provider)
                    else:
                        print("❌ Este provider não está disponível. Instale as dependências primeiro.")
                else:
                    print("❌ Opção inválida. Tente novamente.")
            else:
                print("❌ Digite um número válido.")
        except KeyboardInterrupt:
            print("\n👋 Operação cancelada.")
            exit(0)
        except Exception as e:
            print(f"❌ Erro: {e}")

def get_llm_from_config():
    """
    Obtém o LLM baseado na configuração do ambiente ou seleção interativa
    
    Returns:
        LLM instance
    """
    # Verificar se há uma configuração específica no .env
    preferred_provider = os.getenv("PREFERRED_LLM_PROVIDER", "").lower()
    
    if preferred_provider and preferred_provider in LLMFactory.list_available_providers():
        try:
            print(f"🎯 Usando provider configurado: {preferred_provider}")
            return LLMFactory.create_llm(preferred_provider)
        except Exception as e:
            print(f"⚠️ Erro ao usar provider configurado ({preferred_provider}): {e}")
            print("🔄 Caindo para seleção interativa...")
    
    # Seleção interativa
    _, llm = select_llm_provider()
    return llm

# Configurar o modelo LLM
print("🚀 Configurando modelo de LLM...")
try:
    llm = get_llm_from_config()
    print("✅ LLM configurado com sucesso!")
except Exception as e:
    print(f"❌ Erro na configuração do LLM: {e}")
    exit(1)

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
    goal=f"Criar uma questão de múltipla escolha clara, objetiva e pedagogicamente adequada baseada no edital do {prova}",
    backstory="""Você é um especialista em avaliação educacional com formação em Pedagogia. 
    Tem experiência em criar questões para vestibulares e concursos. 
    Conhece as melhores práticas para formulação de questões de múltipla escolha.""",
    verbose=True,
    llm=llm
)

# Revisor Pedagógico
revisor = Agent(
    role="Revisor Pedagógico",
    goal=f"Garantir a qualidade, clareza e adequação pedagógica da questão finalizada baseada no edital do {prova}",
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
    print("\n" + "="*60)
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
        print("💡 Dicas para resolver:")
        print("- Verifique se a API key está correta")
        print("- Verifique se há créditos disponíveis na sua conta")
        print("- Tente usar um provider diferente")
