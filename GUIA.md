# 🚀 Guia Rápido - Sistema Concursy

## Executar o Sistema

```bash
# 1. Ative o ambiente virtual (se estiver usando)
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 2. Execute o sistema principal
python concursy_app.py
```

## Funcionalidades Principais

### 1️⃣ Gerar Questão
- Cria questões personalizadas para sua prova
- Exemplo: CPA-20, tema "Fundos de Investimento"

### 2️⃣ Analisar PDF
- Extrai informações de editais ou provas
- Coloque seus PDFs em: `data/provas/[nome-prova]/pdfs/`

### 3️⃣ Buscar Questões
- Encontra questões similares já cadastradas
- Analisa padrões de cobrança

### 4️⃣ Explicação Pedagógica
- Explica conceitos difíceis de forma simples
- Ideal para tirar dúvidas específicas

### 5️⃣ Plano de Estudos
- Cria cronograma personalizado
- Baseado em seus pontos fracos

### 6️⃣ Resumir Edital
- Resume editais longos
- Destaca informações essenciais

## 💡 Dicas

1. **Primeira execução**: O sistema pedirá para escolher um provider de LLM
2. **PDFs**: Coloque seus editais em PDF na pasta correspondente antes de analisar
3. **Questões**: São salvas automaticamente para consulta futura

## 🆘 Problemas Comuns

- **"Provider não disponível"**: Instale o provider ou configure a API key
- **"Arquivo não encontrado"**: Verifique o caminho do PDF
- **Erro de API**: Confirme se tem créditos/cota disponível

---