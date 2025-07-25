"""
Agente pedagogo especializado em criar explicações didáticas e educacionais
"""

from crewai import Agent
from typing import Dict, List, Optional

class PedagogoAgent:
    def __init__(self, llm):
        self.llm = llm
        
    def create_agent(self, nivel_ensino: str = "superior") -> Agent:
        """
        Cria um agente pedagogo especializado em explicações
        
        Args:
            nivel_ensino: Nível de ensino (fundamental, médio, superior, concurso)
            
        Returns:
            Agent configurado para explicações pedagógicas
        """
        return Agent(
            role="Pedagogo Especialista em Educação e Aprendizagem",
            goal=f"Criar explicações claras, didáticas e adaptadas ao nível {nivel_ensino}, facilitando o aprendizado",
            backstory="""Você é um pedagogo com doutorado em Educação e mais de 20 anos de experiência.
            Suas especialidades incluem:
            - Didática e metodologias de ensino
            - Teorias de aprendizagem (Piaget, Vygotsky, Ausubel)
            - Adaptação de conteúdo para diferentes níveis
            - Uso de analogias e exemplos práticos
            - Técnicas de memorização e fixação
            - Identificação de dificuldades de aprendizagem
            - Criação de mapas mentais e resumos visuais
            Você sempre busca tornar conceitos complexos em explicações simples e memoráveis.""",
            verbose=True,
            llm=self.llm
        )
    
    def create_explanation_task(self, 
                              conceito: str, 
                              nivel: str = "médio",
                              contexto: Optional[str] = None) -> dict:
        """
        Cria tarefa para explicar um conceito de forma didática
        
        Args:
            conceito: Conceito a ser explicado
            nivel: Nível de complexidade (básico, médio, avançado)
            contexto: Contexto específico (ex: para prova CPA-20)
            
        Returns:
            Dicionário com a descrição da tarefa
        """
        contexto_str = f" no contexto de {contexto}" if contexto else ""
        
        return {
            "description": f"""
            Crie uma explicação didática e completa sobre '{conceito}'{contexto_str}, 
            adequada ao nível {nivel}.
            
            Sua explicação deve incluir:
            
            1. **INTRODUÇÃO MOTIVADORA**
               - Por que é importante entender este conceito
               - Conexão com conhecimentos prévios
               - Objetivos de aprendizagem
            
            2. **EXPLICAÇÃO PRINCIPAL**
               - Definição clara e precisa
               - Decomposição em partes menores
               - Progressão do simples ao complexo
               - Linguagem adequada ao nível
            
            3. **ANALOGIAS E EXEMPLOS**
               - Pelo menos 2 analogias do cotidiano
               - 3 exemplos práticos progressivos
               - Casos de aplicação real
               - Comparações esclarecedoras
            
            4. **REPRESENTAÇÃO VISUAL**
               - Sugestão de diagrama ou mapa mental
               - Fluxograma do processo (se aplicável)
               - Tabela comparativa (se relevante)
            
            5. **ERROS COMUNS**
               - Principais equívocos sobre o tema
               - Pegadinhas em provas
               - Como evitar confusões
            
            6. **FIXAÇÃO DO CONTEÚDO**
               - Resumo em bullet points
               - Mnemônicos ou técnicas de memorização
               - 3 perguntas de verificação
               - Exercício prático proposto
            
            7. **APROFUNDAMENTO**
               - Sugestões de estudo adicional
               - Conexões com outros tópicos
               - Recursos complementares
            
            Lembre-se de:
            - Usar linguagem clara e acessível
            - Evitar jargões desnecessários
            - Incluir pausas para reflexão
            - Estimular o pensamento crítico
            """,
            "expected_output": "Explicação didática completa com todos os elementos pedagógicos solicitados"
        }
    
    def create_review_task(self, questao: Dict, resposta_aluno: str) -> dict:
        """
        Cria tarefa para revisar e explicar uma questão
        
        Args:
            questao: Dicionário com dados da questão
            resposta_aluno: Resposta dada pelo aluno
            
        Returns:
            Dicionário com a descrição da tarefa
        """
        return {
            "description": f"""
            Analise a questão e a resposta do aluno, fornecendo feedback pedagógico completo.
            
            QUESTÃO:
            {questao.get('enunciado', '')}
            
            Alternativas:
            A) {questao.get('alternativas', {}).get('A', '')}
            B) {questao.get('alternativas', {}).get('B', '')}
            C) {questao.get('alternativas', {}).get('C', '')}
            D) {questao.get('alternativas', {}).get('D', '')}
            
            Resposta Correta: {questao.get('resposta_correta', '')}
            Resposta do Aluno: {resposta_aluno}
            
            Forneça:
            
            1. **ANÁLISE DA RESPOSTA**
               - Se está correta ou incorreta
               - Análise do raciocínio provável do aluno
               - Identificação de possíveis lacunas
            
            2. **EXPLICAÇÃO DETALHADA**
               - Por que a resposta correta é correta
               - Análise de cada alternativa
               - Conceitos envolvidos na questão
            
            3. **FEEDBACK CONSTRUTIVO**
               - Pontos positivos (mesmo se errou)
               - Orientações específicas
               - Como melhorar o raciocínio
            
            4. **ESTRATÉGIA DE RESOLUÇÃO**
               - Passo a passo para resolver
               - Dicas para questões similares
               - Palavras-chave importantes
            
            5. **REFORÇO DO APRENDIZADO**
               - Conceitos para revisar
               - Exercícios complementares sugeridos
               - Links com outros tópicos
            """,
            "expected_output": "Feedback pedagógico completo e construtivo sobre a questão"
        }
    
    def create_study_plan_task(self, 
                             prova: str,
                             tempo_disponivel: str,
                             pontos_fracos: List[str]) -> dict:
        """
        Cria tarefa para elaborar plano de estudos personalizado
        
        Args:
            prova: Nome da prova/concurso
            tempo_disponivel: Tempo até a prova
            pontos_fracos: Lista de tópicos com dificuldade
            
        Returns:
            Dicionário com a descrição da tarefa
        """
        return {
            "description": f"""
            Elabore um plano de estudos personalizado para a prova {prova}.
            
            INFORMAÇÕES DO ALUNO:
            - Tempo disponível: {tempo_disponivel}
            - Pontos fracos identificados: {', '.join(pontos_fracos)}
            
            O plano deve incluir:
            
            1. **DIAGNÓSTICO INICIAL**
               - Análise dos pontos fracos
               - Priorização por importância na prova
               - Estimativa de tempo por tópico
            
            2. **CRONOGRAMA DETALHADO**
               - Divisão semanal
               - Horas por dia recomendadas
               - Distribuição de matérias
               - Momentos de revisão
            
            3. **METODOLOGIA DE ESTUDO**
               - Técnicas recomendadas por matéria
               - Ciclos de estudo (teoria + exercícios)
               - Métodos de revisão espaçada
               - Uso de recursos diversos
            
            4. **MATERIAL DE APOIO**
               - Livros/apostilas recomendados
               - Videoaulas sugeridas
               - Exercícios por nível
               - Simulados programados
            
            5. **ESTRATÉGIAS ESPECÍFICAS**
               - Como superar cada ponto fraco
               - Técnicas de memorização
               - Gestão do tempo na prova
               - Controle de ansiedade
            
            6. **ACOMPANHAMENTO**
               - Metas semanais
               - Indicadores de progresso
               - Ajustes no plano
               - Checkpoints de avaliação
            
            7. **DICAS MOTIVACIONAIS**
               - Como manter a disciplina
               - Gestão de energia
               - Equilíbrio estudo-descanso
               - Mindset de aprovação
            """,
            "expected_output": "Plano de estudos completo, personalizado e executável"
        } 