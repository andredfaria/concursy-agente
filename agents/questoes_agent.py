"""
Agente especializado em analisar e fornecer questões exemplo de provas antigas
"""

from crewai import Agent
import json
import os
from typing import List, Dict, Optional

class QuestoesExemploAgent:
    def __init__(self, llm):
        self.llm = llm
        
    def create_agent(self, prova: str) -> Agent:
        """
        Cria um agente especializado em questões de provas antigas
        
        Args:
            prova: Nome da prova/concurso
            
        Returns:
            Agent configurado para análise de questões
        """
        return Agent(
            role="Especialista em Questões de Concursos",
            goal=f"Analisar e fornecer questões exemplo da prova {prova}, identificando padrões e temas recorrentes",
            backstory="""Você é um especialista em análise de questões de concursos com mais de 15 anos de experiência.
            Sua especialidade inclui:
            - Identificar padrões de questões em provas anteriores
            - Classificar questões por tema e nível de dificuldade
            - Analisar a evolução dos temas ao longo dos anos
            - Destacar pegadinhas comuns e pontos de atenção
            - Fornecer questões exemplo similares às cobradas
            Você tem profundo conhecimento sobre as bancas examinadoras e seus estilos de questões.""",
            verbose=True,
            llm=self.llm
        )
    
    def load_questions_from_file(self, prova: str) -> List[Dict]:
        """
        Carrega questões do arquivo JSON da prova
        
        Args:
            prova: Nome da prova
            
        Returns:
            Lista de questões
        """
        base_path = f"data/provas/{prova.lower().replace(' ', '-')}/questoes"
        questions = []
        
        if os.path.exists(base_path):
            for file in os.listdir(base_path):
                if file.endswith('.json'):
                    with open(os.path.join(base_path, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            questions.extend(data)
                        else:
                            questions.append(data)
        
        return questions
    
    def create_analysis_task(self, tema: str, nivel: str, num_questoes: int = 3) -> dict:
        """
        Cria tarefa para analisar e fornecer questões exemplo
        
        Args:
            tema: Tema das questões
            nivel: Nível de dificuldade
            num_questoes: Número de questões exemplo
            
        Returns:
            Dicionário com a descrição da tarefa
        """
        return {
            "description": f"""
            Analise o banco de questões e forneça {num_questoes} questões exemplo sobre o tema '{tema}' 
            com nível de dificuldade '{nivel}'.
            
            Para cada questão fornecida, inclua:
            
            1. **QUESTÃO EXEMPLO**
               - Enunciado completo
               - Todas as alternativas
               - Resposta correta marcada
               - Ano e prova de origem (se disponível)
            
            2. **ANÁLISE DA QUESTÃO**
               - Conceitos cobrados
               - Dificuldade real (fácil/médio/difícil)
               - Pegadinhas ou pontos de atenção
               - Estratégia para resolver
            
            3. **PADRÕES IDENTIFICADOS**
               - Como esse tema costuma ser cobrado
               - Variações comuns da questão
               - Tópicos relacionados que aparecem junto
            
            4. **DICAS DE ESTUDO**
               - Pontos principais a estudar
               - Erros comuns dos candidatos
               - Material de apoio recomendado
            
            Se não houver questões exatas sobre o tema, forneça questões similares 
            e explique a relação com o tema solicitado.
            """,
            "expected_output": f"{num_questoes} questões exemplo com análise completa e dicas de estudo"
        }
    
    def save_question(self, question: Dict, prova: str) -> str:
        """
        Salva uma nova questão no banco de dados
        
        Args:
            question: Dicionário com os dados da questão
            prova: Nome da prova
            
        Returns:
            ID da questão salva
        """
        base_path = f"data/provas/{prova.lower().replace(' ', '-')}/questoes"
        os.makedirs(base_path, exist_ok=True)
        
        # Gera ID único
        question_id = f"{prova.lower()}_{question.get('ano', '2024')}_{question.get('tema', 'geral')}_{len(os.listdir(base_path)) + 1}"
        question['id'] = question_id
        
        # Salva no arquivo
        file_path = os.path.join(base_path, f"{question_id}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(question, f, ensure_ascii=False, indent=2)
        
        return question_id 