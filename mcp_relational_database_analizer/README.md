# 🚀 MCP Relational Database Analyzer

Analisador de banco de dados PostgreSQL usando Model Context Protocol (MCP) com aplicação PetClinic integrada.

## 📋 Visão Geral

Este projeto fornece uma solução completa para análise de performance e estrutura de bancos PostgreSQL, incluindo:

- **🔍 MCP Database Analyzer**: Ferramenta de análise com prompts organizados
- **🌸 PetClinic Application**: Aplicação de exemplo com dados reais
- **🐘 PostgreSQL**: Banco de dados com dados populados
- **📦 Vagrant**: Ambiente virtualizado pronto para uso

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────┐
│           VM Única (Ubuntu 22.04)          │
├─────────────────────────────────────────────┤
│  🔍 MCP Analyzer     :8000                  │
│  🌸 PetClinic        :9080                  │
│  🐘 PostgreSQL       :5432                  │
└─────────────────────────────────────────────┘
```

## 🚀 Início Rápido

### Pré-requisitos

- [Vagrant](https://www.vagrantup.com/downloads) 2.3+
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) 7.0+
- 6GB+ RAM disponível
- 10GB+ espaço em disco

### Instalação

1. **Clone e configure:**
```bash
git clone <repository>
cd mcp_relational_database_analizer
./setup.sh  # Linux/macOS/Git Bash
# ou
setup.bat   # Windows CMD
```

2. **Inicie o ambiente:**
```bash
./manage.sh up
# ou
manage.bat up
```

3. **Acesse via SSH (prompt automático):**
```bash
./manage.sh ssh
# ou
vagrant ssh mcp-relational-database-analyzer
```

## 🎯 Funcionalidades

### 📊 Prompts Organizados

Os prompts estão organizados em categorias para melhor manutenção:

#### 🏗️ Estrutura
- **EST-001**: Estrutura Completa do Banco
- **EST-002**: Inventário de Tabelas  
- **EST-003**: Contagem de Registros
- **EST-004**: Análise de Índices
- **EST-005**: Chaves Estrangeiras

#### 💼 Negócio
- **NEG-001**: Proprietários por Localização
- **NEG-002**: Demografia de Proprietários
- **NEG-003**: Análise de Contatos
- **NEG-004**: Cadastro de Pets Completo
- **NEG-005**: Pets por Tipo
- **NEG-006**: Análise de Idade dos Pets
- **NEG-007**: Equipe Veterinária
- **NEG-008**: Distribuição de Especialidades
- **NEG-009**: Carga de Trabalho dos Veterinários
- **NEG-010**: Análise de Visitas
- **NEG-011**: Tipos de Visitas
- **NEG-012**: Frequência de Visitas por Pet
- **NEG-013**: Visitas Recentes

#### ⚡ Performance
- **PERF-001**: Análise de Query
- **PERF-002**: Queries Lentas
- **PERF-003**: Scans de Tabela
- **PERF-004**: Recomendação de Índices
- **PERF-005**: Índices Não Utilizados
- **PERF-006**: Eficiência dos Índices
- **PERF-007**: Índices Duplicados
- **PERF-008**: Configurações do Sistema
- **PERF-009**: Uso de Memória
- **PERF-010**: Estatísticas de Conexão
- **PERF-011**: Tamanho do Banco

## 🔧 Comandos Úteis

### Gerenciamento do Ambiente
```bash
./manage.sh up        # Iniciar VM
./manage.sh down      # Parar VM
./manage.sh status    # Status da VM
./manage.sh ssh       # SSH com prompt automático
./manage.sh test      # Testar conectividade
./manage.sh provision # Reprovisionar
./manage.sh clean     # Limpar e rebuildar
```

### Dentro da VM
```bash
mcp-start       # Iniciar prompt MCP
mcp-status      # Status do MCP Analyzer
mcp-logs        # Logs do MCP
app-status      # Status do PetClinic
app-logs        # Logs do PetClinic
pg-status       # Status do PostgreSQL
pg-logs         # Logs do PostgreSQL
pg-connect      # Conectar ao PostgreSQL
```

## 🌐 URLs de Acesso

- **MCP Analyzer**: http://localhost:8000
- **PetClinic**: http://localhost:9080  
- **PostgreSQL**: localhost:5432
  - Database: `petclinic`
  - User: `petclinic`
  - Password: `petclinic`

## 📁 Estrutura do Projeto

```
mcp_relational_database_analizer/
├── apps/
│   ├── mcp/                          # MCP Analyzer
│   │   └── src/
│   │       ├── prompts/              # Prompts organizados
│   │       │   ├── structure/        # Prompts de estrutura
│   │       │   ├── business/         # Prompts de negócio
│   │       │   └── performance/      # Prompts de performance
│   │       ├── analysis/             # Módulos de análise
│   │       ├── db/                   # Conectores de banco
│   │       └── tools/                # Ferramentas MCP
│   └── pet-clinic-hilla/             # Aplicação PetClinic
│       └── src/main/resources/db/postgres/
│           └── populate-db.sql       # Dados de exemplo
├── provisioner.sh                    # Script de provisionamento
├── manage.sh / manage.bat            # Scripts de gerenciamento
├── setup.sh / setup.bat              # Scripts de setup
└── Vagrantfile                       # Configuração Vagrant
```

## 🔍 Uso do MCP Analyzer

1. **Acesse via SSH:**
```bash
vagrant ssh mcp-relational-database-analyzer
```

2. **O prompt MCP inicia automaticamente** (ou use `mcp-start`)

3. **Execute prompts por ID:**
```
> 01_complete_structure
> 04_owners_by_location  
> 19_query_analysis
```

4. **Ou navegue por categorias:**
```
> help                 # Lista todos os prompts
> structure            # Prompts de estrutura
> business             # Prompts de negócio
> performance          # Prompts de performance
```

## 🛠️ Desenvolvimento

### Adicionando Novos Prompts

1. **Escolha a categoria apropriada:**
   - `prompts/structure/` - Análise de estrutura
   - `prompts/business/` - Análise de negócio  
   - `prompts/performance/` - Análise de performance

2. **Crie ou edite o arquivo Python correspondente**

3. **Siga o padrão existente:**
```python
CATEGORY_PROMPTS = {
    "prompt_id": {
        "name": "🔍 CAT-001: Nome do Prompt",
        "description": "Descrição detalhada",
        "category": "Categoria",
        "priority": "Alta|Média|Baixa",
        "tool": "nome_da_ferramenta",
        "query": "SQL query ou None",
        "example_result": "Exemplo do resultado",
        "execution_order": 30
    }
}
```

4. **Atualize o `__init__.py` se necessário**

## 🐛 Troubleshooting

### VM não inicia
```bash
./manage.sh clean      # Limpar e rebuildar
```

### Serviços não respondem
```bash
vagrant ssh mcp-relational-database-analyzer
sudo systemctl restart mcp-analyzer
sudo systemctl restart petclinic
sudo systemctl restart postgresql
```

### Problemas de rede
```bash
./manage.sh test       # Testar conectividade
```

### Logs detalhados
```bash
./manage.sh logs-mcp   # Logs do MCP
./manage.sh logs-app   # Logs do PetClinic
./manage.sh logs-pg    # Logs do PostgreSQL
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

**Desenvolvido com ❤️ para análise de bancos PostgreSQL**