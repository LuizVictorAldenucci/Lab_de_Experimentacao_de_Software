# Setup Guide - Configuração do Ambiente

## Pré-requisitos

- Node.js 18+ instalado
- PostgreSQL 14+ instalado
- npm ou yarn

## Passo 1: Preparar o Banco de Dados

### 1.1 Conectar ao PostgreSQL
```bash
psql -U postgres
```

### 1.2 Criar banco de dados
```sql
CREATE DATABASE lab05_db;
\c lab05_db
```

### 1.3 Aplicar schema
```bash
psql -U postgres -d lab05_db -f database/schema.sql
```

### 1.4 Carregar dados de seed (escolher um volume)
```bash
# Para 100 registros:
psql -U postgres -d lab05_db -f database/seed_100.sql

# Para 1.000 registros:
psql -U postgres -d lab05_db -f database/seed_1000.sql

# Para 10.000 registros:
psql -U postgres -d lab05_db -f database/seed_10000.sql
```

### Verificar dados carregados:
```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM posts;
SELECT COUNT(*) FROM comments;
SELECT COUNT(*) FROM comment_authors;
```

## Passo 2: Configurar Variáveis de Ambiente

```bash
cp .env.example .env
```

Editar `.env`:
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=seu_senha_aqui
DB_NAME=lab05_db

REST_PORT=3001
GRAPHQL_PORT=3002

NODE_ENV=development
```

## Passo 3: Instalar Dependências

```bash
npm install
```

### Dependências principais:
- `express` - REST API framework
- `apollo-server-express` - GraphQL server
- `pg` - PostgreSQL client
- `axios` - HTTP client para testes
- `@apollo/client` - GraphQL client
- `dotenv` - Variáveis de ambiente

## Passo 4: Iniciar APIs

**Terminal 1 - REST API:**
```bash
npm run start:rest
# Saída esperada: REST API running on http://localhost:3001
```

**Terminal 2 - GraphQL API:**
```bash
npm run start:graphql
# Saída esperada: GraphQL running on http://localhost:3002
```

## Passo 5: Testar APIs

### REST API
```bash
curl http://localhost:3001/users | jq .
```

### GraphQL API
```bash
curl -X POST http://localhost:3002/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{users{id name email}}"}'
```

## Passo 6: Executar Cliente de Testes

```bash
npm run test

# Saída esperada:
# 🚀 Iniciando experimento...
# Scenario 1: Simple queries...
# ✅ Resultados salvos em ./results/raw_results.csv
```

## Troubleshooting

### Erro de conexão com PostgreSQL
```bash
# Verificar se PostgreSQL está rodando
psql -U postgres -c "SELECT version();"
```

### Porta 3001 ou 3002 já em uso
```bash
# Matar processo na porta
lsof -ti:3001 | xargs kill -9
lsof -ti:3002 | xargs kill -9
```

### Erro de módulo não encontrado
```bash
# Reinstalar node_modules
rm -rf node_modules
npm install
```

### Erro de autenticação PostgreSQL
```bash
# Verificar credenciais em .env
# Resetar senha (como postgres user):
psql -U postgres
postgres=# ALTER USER postgres WITH PASSWORD 'nova_senha';
```

## Verificação Final

Executar checklist:
- [ ] PostgreSQL rodando
- [ ] Database `lab05_db` criada
- [ ] Tabelas com dados carregados
- [ ] REST API respondendo em http://localhost:3001
- [ ] GraphQL API respondendo em http://localhost:3002
- [ ] Cliente de testes executa sem erros
- [ ] Arquivo `results/raw_results.csv` gerado

✅ Ambiente pronto para executar Lab05S01!