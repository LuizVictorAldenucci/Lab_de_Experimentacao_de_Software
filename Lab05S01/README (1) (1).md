# GraphQL vs REST - Experimento Controlado

## Lab05S01: Desenho e Preparação do Experimento

Este repositório contém o design experimental e scripts de preparação para um experimento controlado comparando o desempenho de APIs GraphQL versus REST.

### 📋 Documentação

- **Lab05S01_design.pdf** - Documento completo com design experimental e plano de preparação
- **setup_guide.md** - Guia passo-a-passo para configurar o ambiente
- **execution_plan.md** - Plano detalhado de execução (Sprint 1)

### 🎯 Objetivos

Responder duas perguntas de pesquisa:
- **RQ1:** Respostas GraphQL são mais rápidas que REST?
- **RQ2:** Respostas GraphQL são menores que REST?

### 📊 Estrutura Experimental

- **Fatores:** Tipo de API (2) × Complexidade (3) × Volume (3) × Seleção de Campos (2)
- **Total de Cenários:** 36 tratamentos
- **Repetições:** 30 por cenário
- **Total de Medições:** 1.080 observações

### 🗂️ Estrutura de Diretórios

```
lab05s01/
├── database/              # Scripts SQL e conexão
├── rest-api/              # Implementação REST (Express.js)
├── graphql-api/           # Implementação GraphQL (Apollo)
├── test-client/           # Cliente de teste e coleta de métricas
├── analysis/              # Scripts de análise estatística
└── docs/                  # Documentação
```

### 🚀 Quick Start

```bash
# 1. Instalar dependências
npm install

# 2. Configurar banco de dados
psql -U postgres -f database/schema.sql
psql -U postgres -d lab05_db -f database/seed_100.sql

# 3. Iniciar APIs (em terminais separados)
npm run start:rest
npm run start:graphql

# 4. Executar testes
npm run test

# 5. Analisar resultados
python analysis/statistical_analysis.py
```

### 📦 Stack Tecnológico

- **Backend:** Node.js 18+, Express.js, Apollo Server
- **Banco:** PostgreSQL 14+
- **Testes:** Axios, Apollo Client
- **Análise:** Python (SciPy, Pandas, Matplotlib)

### 📝 Próximos Passos (Sprint 2 & 3)

- **Lab05S02:** Execução experimental, coleta de dados e análise estatística
- **Lab05S03:** Criação de dashboard de visualização dos resultados

### ✍️ Autores

[Nome do Grupo]

### 📅 Data

November 27, 2025

### 📞 Suporte

Para questões sobre o design experimental, consultar `Lab05S01_design.pdf` Seção 1 e 2.