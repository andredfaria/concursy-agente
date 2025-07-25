"""
Agente especializado em analisar e extrair informações de arquivos PDF
"""

from crewai import Agent
import os
from typing import List, Dict, Optional
import PyPDF2
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class PDFAnalyzerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
    def create_agent(self) -> Agent:
        """
        Cria um agente especializado em análise de PDFs
        
        Returns:
            Agent configurado para análise de documentos PDF
        """
        return Agent(
            role="Especialista em Análise de Documentos PDF",
            goal="Extrair, analisar e estruturar informações relevantes de documentos PDF de editais e provas",
            backstory="""Você é um especialista em processamento e análise de documentos com experiência em:
            - Extração de texto de PDFs complexos
            - Identificação de estruturas em documentos (títulos, seções, tabelas)
            - Análise semântica de conteúdo
            - Organização de informações extraídas
            - Tratamento de diferentes formatações e layouts
            Sua expertise permite extrair o máximo de informação útil mesmo de PDFs mal formatados ou escaneados.""",
            verbose=True,
            llm=self.llm
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extrai texto de um arquivo PDF
        
        Args:
            pdf_path: Caminho do arquivo PDF
            
        Returns:
            Texto extraído do PDF
        """
        try:
            # Tenta primeiro com PyPDFLoader (melhor para PDFs complexos)
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            text = "\n".join([page.page_content for page in pages])
            
            if not text.strip():
                # Fallback para PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text()
            
            return text
            
        except Exception as e:
            return f"Erro ao extrair texto do PDF: {str(e)}"
    
    def analyze_pdf_structure(self, pdf_path: str) -> Dict:
        """
        Analisa a estrutura de um PDF
        
        Args:
            pdf_path: Caminho do arquivo PDF
            
        Returns:
            Dicionário com informações sobre a estrutura
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                structure = {
                    "num_paginas": len(pdf_reader.pages),
                    "metadata": {
                        "titulo": pdf_reader.metadata.get('/Title', 'N/A'),
                        "autor": pdf_reader.metadata.get('/Author', 'N/A'),
                        "assunto": pdf_reader.metadata.get('/Subject', 'N/A'),
                        "criador": pdf_reader.metadata.get('/Creator', 'N/A'),
                    },
                    "tem_formularios": bool(pdf_reader.get_form_text_fields()),
                    "tem_anexos": bool(pdf_reader.attachments),
                }
                
                return structure
                
        except Exception as e:
            return {"erro": str(e)}
    
    def create_extraction_task(self, pdf_path: str, tipo_documento: str = "edital") -> dict:
        """
        Cria tarefa para extrair informações específicas de um PDF
        
        Args:
            pdf_path: Caminho do arquivo PDF
            tipo_documento: Tipo do documento (edital, prova, apostila, etc.)
            
        Returns:
            Dicionário com a descrição da tarefa
        """
        text = self.extract_text_from_pdf(pdf_path)
        
        if tipo_documento == "edital":
            task_description = f"""
            Analise o texto extraído do PDF do edital e extraia as seguintes informações:
            
            1. **IDENTIFICAÇÃO DO CONCURSO**
               - Nome completo do concurso/certificação
               - Instituição organizadora
               - Banca examinadora
               - Número do edital
            
            2. **VAGAS E REQUISITOS**
               - Número total de vagas
               - Distribuição por cargo/área
               - Requisitos mínimos
               - Remuneração
            
            3. **CRONOGRAMA COMPLETO**
               - Período de inscrições
               - Data da prova
               - Divulgação de resultados
               - Outras datas relevantes
            
            4. **ESTRUTURA DA PROVA**
               - Disciplinas e número de questões
               - Peso de cada disciplina
               - Critérios de aprovação
               - Tempo de duração
            
            5. **CONTEÚDO PROGRAMÁTICO DETALHADO**
               - Liste cada disciplina
               - Tópicos de cada disciplina
               - Bibliografia recomendada (se houver)
            
            6. **INFORMAÇÕES ADMINISTRATIVAS**
               - Taxa de inscrição
               - Documentação necessária
               - Locais de prova
               
            Texto do PDF:
            {text[:10000]}...  # Limita para não sobrecarregar
            """
            
        elif tipo_documento == "prova":
            task_description = f"""
            Analise o texto extraído do PDF da prova e extraia:
            
            1. **IDENTIFICAÇÃO**
               - Nome da prova/concurso
               - Ano de aplicação
               - Banca organizadora
            
            2. **QUESTÕES**
               - Extraia cada questão com:
                 * Número da questão
                 * Enunciado completo
                 * Alternativas (A, B, C, D, E)
                 * Disciplina/tema
            
            3. **ANÁLISE GERAL**
               - Total de questões
               - Distribuição por disciplina
               - Nível de dificuldade geral
            
            Texto do PDF:
            {text[:10000]}...
            """
            
        else:
            task_description = f"""
            Analise o texto extraído do PDF e forneça:
            
            1. **RESUMO DO DOCUMENTO**
               - Tipo de documento
               - Assunto principal
               - Pontos-chave
            
            2. **ESTRUTURA**
               - Principais seções
               - Organização do conteúdo
            
            3. **INFORMAÇÕES RELEVANTES**
               - Dados importantes extraídos
               - Tabelas ou listas encontradas
            
            Texto do PDF:
            {text[:10000]}...
            """
        
        return {
            "description": task_description,
            "expected_output": f"Extração estruturada e completa das informações do {tipo_documento}"
        }
    
    def save_extracted_data(self, data: Dict, prova: str, filename: str) -> str:
        """
        Salva dados extraídos em formato estruturado
        
        Args:
            data: Dados extraídos
            prova: Nome da prova
            filename: Nome do arquivo de saída
            
        Returns:
            Caminho do arquivo salvo
        """
        import json
        
        base_path = f"data/provas/{prova.lower().replace(' ', '-')}/resumos"
        os.makedirs(base_path, exist_ok=True)
        
        file_path = os.path.join(base_path, f"{filename}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return file_path 