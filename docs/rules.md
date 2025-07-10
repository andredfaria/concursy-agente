**Documentação do Projeto: Gerador de Provas de Simulado**

---

## 🌍 Visão Geral do Projeto

Este projeto tem como objetivo a **criação automatizada de provas simuladas para concursos públicos**, com base em editais específicos. Utiliza uma arquitetura baseada em **multiagentes inteligentes**, com o uso de ferramentas como **CrewAI**, **LangGraph** e **OpenAI** para geração de conteúdo.

Inicialmente, é gerada apenas uma questão por vez, com **enunciado, resposta correta e justificativa**. A evolução do projeto contempla a junção dessas questões em uma prova completa, padronizada e formatada para PDF.

---

## 📈 Objetivo

* Gerar **provas personalizadas** a partir de editais de concursos.
* Padronizar a **estrutura da prova e correções**.
* Permitir exportação do conteúdo como **documento PDF**.

---

## 👨‍🎓 Público-Alvo

* Estudantes de concursos públicos ("concurseiros").
* Não há diferenciação entre perfis de usuário.

---

## ⚖️ Funcionalidades

### Existentes

* Geração de **uma pergunta** com resposta e justificativa.

### Planejadas

* Agrupamento de questões em uma prova completa.
* Geração de **documento texto** padronizado.
* Conversão para **formato PDF** com layout definido.

---

## 🧬 Lógica de Negócio

* O sistema recebe um **edital** como base.
* Com base no edital:

  * Define-se a **quantidade de questões por matéria**.
  * Cada agente gera questões com **nível de dificuldade**, resposta e justificativa.
* As questões são agrupadas e formatadas como prova.

---

## 🧰 Arquitetura

* Arquitetura baseada em **multiagentes**.
* Ferramentas utilizadas:

  * **Python** como linguagem principal.
  * **CrewAI** para orquestração de agentes.
  * **LangGraph** para fluxos de controle.
  * **OpenAI API** para geração de conteúdo (perguntas, justificativas, formatação).

---

## 📊 Entradas e Saídas

* **Entradas:**

  * Texto do edital.
  * Número de questões.
  * Matérias e pesos (se houver).

* **Saídas:**

  * Documento com perguntas, respostas e justificativas.
  * PDF padronizado.

---

## 💡 Guia de Desenvolvimento

> *"Desenvolva como um programador Python com mais de 10 anos de experiência."*

* Utilize **boas práticas de engenharia de software**, como:

  * Modularização de componentes.
  * Padrões de projeto (ex: Strategy, Factory para agentes).
  * Testes automatizados unitários e de integração.
* Estrutura sugerida:

  ```bash
  /agents           # Definição e configuração de agentes
  /core             # Lógica principal da geração de prova
  /parsers          # Leitura e interpretação de editais
  /outputs          # Exportação para texto e PDF
  /tests            # Testes unitários e de integração
  main.py           # Ponto de entrada do projeto
  requirements.txt  # Dependências
  ```

---

## 🔄 Fluxo de Execução

1. Input do edital e dados de prova
2. Agentes geram perguntas individualmente
3. Cada pergunta possui: enunciado, alternativas, resposta correta e justificativa
4. As perguntas são agrupadas, formatadas e ordenadas
5. Exportação para PDF final padronizado

---

## 📅 Roadmap (Curto Prazo)

* [ ] Refatorar agentes para padronizar a saída
* [ ] Desenvolver função de agrupamento de questões
* [ ] Implementar gerador de documento (Markdown ou LaTeX)
* [ ] Adicionar exportação em PDF com layout fixo

---
