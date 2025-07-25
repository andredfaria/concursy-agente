"""
Agente especializado em analisar e resumir editais de concursos
"""

from crewai import Agent
from typing import Optional

class EditalAgent:
    def __init__(self, llm):
        self.llm = llm
        
    def create_agent(self, prova: str) -> Agent:
        """
        Cria um agente especializado em resumir editais
        
        Args:
            prova: Nome da prova/concurso
            
        Returns:
            Agent configurado para análise de editais
        """
        return Agent(
            role="Especialista em Análise de Editais",
            goal=f"Analisar e criar resumos estruturados do edital da prova {prova}, destacando os pontos mais importantes",
            backstory="""Você é um especialista em concursos públicos com vasta experiência em análise de editais.
            Sua especialidade é identificar e resumir as informações mais relevantes dos editais, incluindo:
            - Conteúdo programático detalhado
            - Formato e estrutura da prova
            - Critérios de avaliação
            - Datas importantes
            - Requisitos e documentação
            Você sempre organiza as informações de forma clara e objetiva, facilitando o estudo dos candidatos.""",
            verbose=True,
            llm=self.llm
        )
    
    def create_summary_task(self, edital_content: str) -> dict:
        """
        Cria estrutura de tarefa para resumir um edital
        
        Args:
            edital_content: Conteúdo do edital a ser resumido
            
        Returns:
            Dicionário com a descrição da tarefa
        """
        return {
            "description": f"""
            Analise o edital fornecido e crie um resumo estruturado contendo:
            
            1. **INFORMAÇÕES GERAIS**
               - Nome do concurso/certificação
               - Organizadora
               - Número de vagas (se aplicável)
               - Requisitos básicos
            
            2. **ESTRUTURA DA PROVA**
               - Número de questões por disciplina
               - Peso de cada disciplina
               - Nota mínima para aprovação
               - Tempo de prova
            
            3. **CONTEÚDO PROGRAMÁTICO**
               - Liste as disciplinas
               - Para cada disciplina, liste os tópicos principais
               - Destaque os tópicos mais cobrados historicamente
            
            4. **DATAS IMPORTANTES**
               - Inscrições
               - Prova
               - Resultados
            
            5. **OBSERVAÇÕES IMPORTANTES**
               - Documentação necessária
               - Critérios de desempate
               - Outras informações relevantes
            
            Edital a analisar:
            {edital_content}
            """,
            "expected_output": "Resumo estruturado e completo do edital em formato markdown"
        } 