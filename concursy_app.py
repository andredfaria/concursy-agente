"""
Sistema Concursy - Gerador de Questões e Assistente de Estudos com IA
"""

from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv
from llm_config import LLMFactory
from agents import EditalAgent, QuestoesExemploAgent, PDFAnalyzerAgent, PedagogoAgent

# Carregar variáveis de ambiente
load_dotenv()

class ConcursyApp:
    def __init__(self):
        print("🚀 Inicializando Sistema Concursy...")
        self.llm = self._setup_llm()
        self._setup_agents()
        
    def _setup_llm(self):
        """Configura o LLM usando a factory"""
        from index import get_llm_from_config
        return get_llm_from_config()
    
    def _setup_agents(self):
        """Inicializa todos os agentes especializados"""
        self.edital_agent = EditalAgent(self.llm)
        self.questoes_agent = QuestoesExemploAgent(self.llm)
        self.pdf_agent = PDFAnalyzerAgent(self.llm)
        self.pedagogo_agent = PedagogoAgent(self.llm)
        
        # Agentes originais do index.py
        self.especialista = None
        self.gerador = None
        self.revisor = None
    
    def menu_principal(self):
        """Menu principal do sistema"""
        while True:
            print("\n" + "="*60)
            print("🎯 SISTEMA CONCURSY - Menu Principal")
            print("="*60)
            print("1. 📝 Gerar Nova Questão")
            print("2. 📄 Analisar PDF (Edital/Prova)")
            print("3. 📚 Buscar Questões Exemplo")
            print("4. 🎓 Explicação Pedagógica")
            print("5. 📊 Criar Plano de Estudos")
            print("6. 📋 Resumir Edital")
            print("7. ❌ Sair")
            print("-"*60)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.gerar_questao()
            elif opcao == "2":
                self.analisar_pdf()
            elif opcao == "3":
                self.buscar_questoes_exemplo()
            elif opcao == "4":
                self.explicacao_pedagogica()
            elif opcao == "5":
                self.criar_plano_estudos()
            elif opcao == "6":
                self.resumir_edital()
            elif opcao == "7":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida!")
    
    def gerar_questao(self):
        """Gera uma nova questão usando os agentes originais"""
        print("\n📝 GERADOR DE QUESTÕES")
        print("-"*40)
        
        prova = input("Nome da prova/certificação: ").strip()
        tema = input("Tema da questão: ").strip()
        nivel = input("Nível (Fácil/Médio/Difícil): ").strip()
        area = input("Área de conhecimento: ").strip()
        
        # Criar agentes específicos
        self.especialista = Agent(
            role="Especialista em Conteúdo Educacional",
            goal=f"Identificar e estruturar os conceitos fundamentais sobre '{tema}' adequados ao nível {nivel}",
            backstory=f"""Você é um professor experiente com doutorado na área de '{area}'. 
            Tem mais de 20 anos de experiência em concurso da area de '{area}' e é especialista em adaptar conteúdos 
            complexos para diferentes níveis de aprendizado.""",
            verbose=True,
            llm=self.llm
        )
        
        self.gerador = Agent(
            role="Criador de Questões de Múltipla Escolha",
            goal=f"Criar uma questão de múltipla escolha clara, objetiva e pedagogicamente adequada baseada no edital do {prova}",
            backstory="""Você é um especialista em avaliação educacional com formação em Pedagogia. 
            Tem experiência em criar questões para vestibulares e concursos. 
            Conhece as melhores práticas para formulação de questões de múltipla escolha.""",
            verbose=True,
            llm=self.llm
        )
        
        # Criar tarefas
        tarefa_especialista = Task(
            description=f"""
            Analise o tema '{tema}' e identifique os 5 pontos principais que devem ser abordados 
            em uma questão de nível {nivel}. 
            
            Forneça:
            1. Lista dos conceitos fundamentais
            2. Aspectos mais importantes para avaliação
            3. Possíveis conexões com outros temas
            4. Sugestões de enfoque adequado ao nível
            """,
            agent=self.especialista,
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
            """,
            agent=self.gerador,
            expected_output="Questão de múltipla escolha completa com 4 alternativas e resposta correta identificada"
        )
        
        # Executar
        equipe = Crew(
            agents=[self.especialista, self.gerador],
            tasks=[tarefa_especialista, tarefa_gerador],
            verbose=True,
            process="sequential"
        )
        
        print("\n🔄 Gerando questão...")
        resultado = equipe.kickoff()
        
        print("\n" + "="*60)
        print("✅ QUESTÃO GERADA")
        print("="*60)
        print(resultado)
        
        # Salvar questão se desejado
        salvar = input("\nDeseja salvar esta questão? (s/n): ").lower()
        if salvar == 's':
            questao_dict = {
                "prova": prova,
                "tema": tema,
                "nivel": nivel,
                "area": area,
                "enunciado": "Extrair do resultado",
                "alternativas": {"A": "", "B": "", "C": "", "D": ""},
                "resposta_correta": "",
                "resultado_completo": str(resultado)
            }
            question_id = self.questoes_agent.save_question(questao_dict, prova)
            print(f"✅ Questão salva com ID: {question_id}")
    
    def analisar_pdf(self):
        """Analisa um arquivo PDF"""
        print("\n📄 ANALISADOR DE PDF")
        print("-"*40)
        
        pdf_path = input("Caminho do arquivo PDF: ").strip()
        if not os.path.exists(pdf_path):
            print("❌ Arquivo não encontrado!")
            return
        
        tipo = input("Tipo de documento (edital/prova/outro): ").lower().strip()
        prova = input("Nome da prova/concurso: ").strip()
        
        # Criar agente e tarefa
        agent = self.pdf_agent.create_agent()
        task_info = self.pdf_agent.create_extraction_task(pdf_path, tipo)
        
        task = Task(
            description=task_info["description"],
            agent=agent,
            expected_output=task_info["expected_output"]
        )
        
        # Executar
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        print("\n🔄 Analisando PDF...")
        resultado = crew.kickoff()
        
        print("\n" + "="*60)
        print("✅ ANÁLISE CONCLUÍDA")
        print("="*60)
        print(resultado)
        
        # Salvar resultado
        salvar = input("\nDeseja salvar a análise? (s/n): ").lower()
        if salvar == 's':
            filename = os.path.basename(pdf_path).replace('.pdf', '_analise')
            saved_path = self.pdf_agent.save_extracted_data(
                {"analise": str(resultado), "tipo": tipo},
                prova,
                filename
            )
            print(f"✅ Análise salva em: {saved_path}")
    
    def buscar_questoes_exemplo(self):
        """Busca questões exemplo sobre um tema"""
        print("\n📚 BUSCAR QUESTÕES EXEMPLO")
        print("-"*40)
        
        prova = input("Nome da prova/certificação: ").strip()
        tema = input("Tema das questões: ").strip()
        nivel = input("Nível (Fácil/Médio/Difícil): ").strip()
        num = int(input("Número de questões (padrão 3): ") or "3")
        
        # Criar agente e tarefa
        agent = self.questoes_agent.create_agent(prova)
        task_info = self.questoes_agent.create_analysis_task(tema, nivel, num)
        
        task = Task(
            description=task_info["description"],
            agent=agent,
            expected_output=task_info["expected_output"]
        )
        
        # Executar
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        print("\n🔄 Buscando questões exemplo...")
        resultado = crew.kickoff()
        
        print("\n" + "="*60)
        print("✅ QUESTÕES ENCONTRADAS")
        print("="*60)
        print(resultado)
    
    def explicacao_pedagogica(self):
        """Cria explicação pedagógica de um conceito"""
        print("\n🎓 EXPLICAÇÃO PEDAGÓGICA")
        print("-"*40)
        
        conceito = input("Conceito a ser explicado: ").strip()
        nivel = input("Nível (básico/médio/avançado): ").strip()
        contexto = input("Contexto específico (opcional): ").strip() or None
        
        # Criar agente e tarefa
        agent = self.pedagogo_agent.create_agent()
        task_info = self.pedagogo_agent.create_explanation_task(conceito, nivel, contexto)
        
        task = Task(
            description=task_info["description"],
            agent=agent,
            expected_output=task_info["expected_output"]
        )
        
        # Executar
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        print("\n🔄 Criando explicação pedagógica...")
        resultado = crew.kickoff()
        
        print("\n" + "="*60)
        print("✅ EXPLICAÇÃO PEDAGÓGICA")
        print("="*60)
        print(resultado)
    
    def criar_plano_estudos(self):
        """Cria plano de estudos personalizado"""
        print("\n📊 CRIAR PLANO DE ESTUDOS")
        print("-"*40)
        
        prova = input("Nome da prova/concurso: ").strip()
        tempo = input("Tempo disponível até a prova: ").strip()
        
        print("Informe seus pontos fracos (digite 'fim' quando terminar):")
        pontos_fracos = []
        while True:
            ponto = input("- ").strip()
            if ponto.lower() == 'fim':
                break
            if ponto:
                pontos_fracos.append(ponto)
        
        if not pontos_fracos:
            print("❌ Informe pelo menos um ponto fraco!")
            return
        
        # Criar agente e tarefa
        agent = self.pedagogo_agent.create_agent("concurso")
        task_info = self.pedagogo_agent.create_study_plan_task(prova, tempo, pontos_fracos)
        
        task = Task(
            description=task_info["description"],
            agent=agent,
            expected_output=task_info["expected_output"]
        )
        
        # Executar
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        print("\n🔄 Criando plano de estudos personalizado...")
        resultado = crew.kickoff()
        
        print("\n" + "="*60)
        print("✅ PLANO DE ESTUDOS")
        print("="*60)
        print(resultado)
    
    def resumir_edital(self):
        """Resume um edital"""
        print("\n📋 RESUMIR EDITAL")
        print("-"*40)
        
        prova = input("Nome da prova/concurso: ").strip()
        
        print("Como deseja fornecer o edital?")
        print("1. Caminho do arquivo PDF")
        print("2. Colar texto do edital")
        opcao = input("Opção: ").strip()
        
        if opcao == "1":
            pdf_path = input("Caminho do PDF: ").strip()
            if not os.path.exists(pdf_path):
                print("❌ Arquivo não encontrado!")
                return
            edital_content = self.pdf_agent.extract_text_from_pdf(pdf_path)
        else:
            print("Cole o texto do edital (digite '###FIM###' em uma nova linha quando terminar):")
            lines = []
            while True:
                line = input()
                if line.strip() == "###FIM###":
                    break
                lines.append(line)
            edital_content = "\n".join(lines)
        
        # Criar agente e tarefa
        agent = self.edital_agent.create_agent(prova)
        task_info = self.edital_agent.create_summary_task(edital_content)
        
        task = Task(
            description=task_info["description"],
            agent=agent,
            expected_output=task_info["expected_output"]
        )
        
        # Executar
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        print("\n🔄 Resumindo edital...")
        resultado = crew.kickoff()
        
        print("\n" + "="*60)
        print("✅ RESUMO DO EDITAL")
        print("="*60)
        print(resultado)
        
        # Salvar resumo
        salvar = input("\nDeseja salvar o resumo? (s/n): ").lower()
        if salvar == 's':
            base_path = f"data/provas/{prova.lower().replace(' ', '-')}/resumos"
            os.makedirs(base_path, exist_ok=True)
            
            filename = f"resumo_edital_{prova.lower().replace(' ', '_')}.md"
            file_path = os.path.join(base_path, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# Resumo do Edital - {prova}\n\n")
                f.write(str(resultado))
            
            print(f"✅ Resumo salvo em: {file_path}")

if __name__ == "__main__":
    try:
        app = ConcursyApp()
        app.menu_principal()
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Verifique as configurações e tente novamente.") 