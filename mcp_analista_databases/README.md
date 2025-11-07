# 🚀 MCP Database Analyzer - Vagrant Edition

## ✅ STATUS: TOTALMENTE CORRIGIDO E OTIMIZADO

**Última atualização**: 2025-01-27  
**Versão**: 2.1 - Prompts Organizados  
**Problemas corrigidos**: Python, dependências, caminhos dinâmicos, auto-start MCP, prompts organizados

## ⚡ Visão Geral

Sistema integrado de análise de performance PostgreSQL com **prompt MCP que inicia automaticamente** via SSH!

### 🎯 Principais Funcionalidades

- **🎪 Auto-Start**: Prompt MCP inicia automaticamente quando você faz SSH
- **🏗️ Arquitetura Simplificada**: VM única otimizada
- **🐘 PostgreSQL Integrado**: Banco de dados na mesma VM
- **🌍 Acesso Externo**: PetClinic e MCP acessíveis do host
- **🎨 Interface Rica**: Prompt colorido com comandos intuitivos
- **📁 Caminhos Dinâmicos**: Funciona em Windows, Linux e macOS
- **🔧 Setup Automático**: Scripts de configuração incluídos
- **📊 Prompts Organizados**: 10 análises categorizadas por prioridade
- **🚀 Execução Sequencial**: Análise completa automatizada

## 🏗️ Arquitetura (VM Única)

```
┌─────────────────────────────────────────────┐
│              MCP Analyzer                   │
│            (192.168.56.10)                 │
│                                             │
│  🔍 MCP API :8000    🌸 PetClinic :8080    │
│  🐘 PostgreSQL :5432                       │
│  🎯 Auto Prompt MCP                        │
│                                             │
│           4GB RAM / 2 CPU                   │
└─────────────────────────────────────────────┘
                      ▲
                      │
         localhost:8000, :8080, :5432
```

## ⚡ Início Rápido

### 1. Setup Inicial (Primeira vez)

```bash
# Windows
setup.bat

# Linux/macOS/Git Bash
./setup.sh
```

### 2. Iniciar Ambiente

```bash
# Windows
manage.bat up

# Linux/macOS/Git Bash  
./manage.sh up

# Ou comando direto
vagrant up mcp-relational-database-analyzer
```

### 3. Acessar MCP (Auto-Start!)

```bash
# O prompt MCP inicia automaticamente!
vagrant ssh mcp-relational-database-analyzer

# Você verá imediatamente:
# ╔══════════════════════════════════════════════════════════════════╗
# ║  🚀 BEM-VINDO AO MCP DATABASE ANALYZER - VAGRANT EDITION        ║
# ║     ✨ Iniciado automaticamente via SSH                         ║
# ║     🐘 PostgreSQL pronto para análise                           ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# compass> _
```

### 4. URLs de Acesso Externo

- **🌸 PetClinic**: http://localhost:9080
- **🔍 MCP API**: http://localhost:8000
- **❤️ Health Check**: http://localhost:8000/health
- **🐘 PostgreSQL**: localhost:5432 (petclinic/petclinic)

## 🎮 Comandos do MCP

Quando estiver no prompt MCP:

```bash
compass> mcp status     # Status dos serviços
compass> mcp actions    # Menu de ações interativo  
compass> mcp prompts    # Análises organizadas por categoria
compass> 01-10          # Executar prompt específico
compass> all            # Executar sequência completa
compass> mcp list       # Listar bancos
compass> mcp tables     # Listar tabelas
compass> quit           # Sair
```

## 🔧 Gerenciamento

### Scripts Multiplataforma

```bash
# Windows
manage.bat up          # Iniciar ambiente
manage.bat status      # Status da VM
manage.bat ssh         # SSH para MCP (auto-start)
manage.bat test        # Testar conectividade
manage.bat down        # Parar ambiente

# Linux/macOS/Git Bash
./manage.sh up         # Iniciar ambiente
./manage.sh status     # Status da VM
./manage.sh ssh        # SSH para MCP (auto-start)
./manage.sh test       # Testar conectividade
./manage.sh down       # Parar ambiente
```

### Comandos Vagrant Diretos

```bash
# Gerenciamento básico
vagrant up mcp-relational-database-analyzer      # Iniciar VM
vagrant ssh mcp-relational-database-analyzer     # SSH (prompt auto-start)
vagrant halt mcp-relational-database-analyzer    # Parar VM
vagrant provision mcp-relational-database-analyzer # Reprovisionar
vagrant reload mcp-relational-database-analyzer  # Reiniciar VM
vagrant destroy mcp-relational-database-analyzer # Destruir VM
```

**📚 Para lista completa de comandos**: Ver arquivo `commands.md`

### Logs e Monitoramento

```bash
# Via script (Windows)
manage.bat logs-mcp    # Logs do MCP
manage.bat logs-pg     # Logs PostgreSQL
manage.bat logs-app    # Logs PetClinic

# Via script (Linux/macOS)
./manage.sh logs-mcp   # Logs do MCP
./manage.sh logs-pg    # Logs PostgreSQL
./manage.sh logs-app   # Logs PetClinic

# Via SSH direto
vagrant ssh mcp-relational-database-analyzer -c "mcp-logs"
vagrant ssh mcp-relational-database-analyzer -c "pg-logs"
```

## 📁 Estrutura Organizada

```
mcp_analista_databases/
├── Vagrantfile                 # Configuração principal (caminhos dinâmicos)
├── setup.sh / setup.bat        # Scripts de configuração inicial
├── manage.sh / manage.bat      # Scripts de gerenciamento
├── vagrant/
│   ├── provision-analyzer.sh   # Setup MCP + PostgreSQL
│   └── provision-petclinic.sh  # Setup PetClinic
├── apps/
│   ├── mcp/                    # Código MCP Analyzer
│   │   ├── mcp-prompt.py       # Prompt interativo
│   │   ├── requirements.txt    # Dependências corrigidas
│   │   └── src/                # API e ferramentas
│   └── pet-clinic-hilla/       # Aplicação Spring Boot
├── config/
│   └── vagrant.env             # Configurações do ambiente
├── logs/                       # Diretório para logs
├── CORREÇÕES_FINAIS.md         # Documentação das correções
└── commands.md                 # Lista completa de comandos
```

## 🎯 Casos de Uso

### Análise Rápida
```bash
# Setup inicial (primeira vez)
./setup.sh  # ou setup.bat no Windows

# Iniciar ambiente
./manage.sh up  # ou manage.bat up no Windows

# Acessar MCP (auto-start!)
vagrant ssh mcp-relational-database-analyzer
```

### Desenvolvimento
```bash
# Acessar aplicação web
curl http://localhost:9080

# Conectar no banco
psql -h localhost -U petclinic -d petclinic

# API do MCP
curl http://localhost:8000/health
```

### Troubleshooting
```bash
# Status completo
./manage.sh status     # ou manage.bat status

# Testar conectividade
./manage.sh test       # ou manage.bat test

# Ver logs de erro
vagrant ssh mcp-relational-database-analyzer -c "journalctl -u mcp-analyzer -n 50"
vagrant ssh mcp-relational-database-analyzer -c "journalctl -u petclinic -n 50"
```

## ⚙️ Requisitos

- **Vagrant** + **VirtualBox**
- **4GB RAM** disponível
- **15GB** espaço em disco
- **Portas**: 5432, 8000, 8080
- **SO**: Windows, Linux ou macOS

## 🎊 Resultado Final

**Uma vez configurado**, basta digitar:
```bash
vagrant ssh mcp-relational-database-analyzer
```

E você estará **imediatamente** no prompt MCP, pronto para analisar o PostgreSQL! 🚀

## 📊 Prompts de Análise Organizados

### 🏗️ **ESTRUTURA E INVENTÁRIO (01-03)** - Execute Primeiro
- **01**: 🏗️ EST-001: Estrutura Completa do Banco 🔴 ALTA
- **02**: 📋 EST-002: Inventário de Tabelas 🔴 ALTA  
- **03**: 📊 EST-003: Contagem de Registros 🔴 ALTA

### 💼 **DADOS DE NEGÓCIO (04-07)** - Execute Segundo
- **04**: 👥 NEG-001: Proprietários por Localização 🟡 MÉDIA
- **05**: 🐕 NEG-002: Cadastro de Pets Completo 🟡 MÉDIA
- **06**: 🏥 NEG-003: Equipe Veterinária 🟡 MÉDIA
- **07**: 📈 NEG-004: Análise de Visitas 🟡 MÉDIA

### ⚡ **PERFORMANCE E OTIMIZAÇÃO (08-10)** - Execute Conforme Necessário
- **08**: 🔍 PERF-001: Análise de Query 🔴 ALTA
- **09**: 💡 PERF-002: Recomendação de Índices 🔴 ALTA
- **10**: ⚙️ PERF-003: Configurações do Sistema 🟡 MÉDIA

### 🚀 Execução Recomendada
```bash
# Análise completa automatizada
compass❯ all

# Ou execução individual
compass❯ 01    # Estrutura do banco
compass❯ 05    # Cadastro de pets
compass❯ 08    # Análise de performance
```

## 🔧 Correções Implementadas

- ✅ **Python 3.10**: Instalação completa com todas as dependências
- ✅ **Caminhos Dinâmicos**: Funciona em qualquer sistema operacional
- ✅ **VM Única**: Arquitetura simplificada e otimizada
- ✅ **Auto-Start MCP**: Prompt inicia automaticamente no SSH
- ✅ **Scripts Multiplataforma**: Windows (.bat) e Unix (.sh)
- ✅ **Setup Automático**: Verificação de dependências incluída
- ✅ **Prompts Organizados**: 10 análises categorizadas (EST/NEG/PERF)
- ✅ **Execução Sequencial**: Comando 'all' para análise completa
- ✅ **Interface Melhorada**: Cores, prioridades e navegação intuitiva

---

**🎯 Zero configuração manual necessária!** O ambiente está completamente otimizado e portável para análise profissional de bancos de dados PostgreSQL em qualquer sistema operacional.