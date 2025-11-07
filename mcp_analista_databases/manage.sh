#!/bin/bash

# MCP Vagrant - Utilitários de Gerenciamento
# Compass UOL Edition

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

function show_header() {
    echo -e "\n${YELLOW}================================${NC}"
    echo -e "${YELLOW}  $1${NC}"
    echo -e "${YELLOW}================================${NC}\n"
}

function show_usage() {
    echo -e "${CYAN}MCP Database Analyzer - Vagrant Edition${NC}"
    echo ""
    echo "Uso: $0 [comando]"
    echo ""
    echo -e "${YELLOW}Comandos disponíveis:${NC}"
    echo "  up        - Inicia a VM"
    echo "  down      - Para a VM"
    echo "  status    - Mostra status da VM"
    echo "  ssh       - SSH direto para a VM (auto-start prompt MCP)"
    echo "  logs-mcp  - Logs do MCP Analyzer"
    echo "  logs-pg   - Logs do PostgreSQL"
    echo "  logs-app  - Logs do PetClinic"
    echo "  test      - Testa conectividade"
    echo "  provision - Reprovisiona a VM"
    echo "  reload    - Reinicia a VM"
    echo "  clean     - Limpa e rebuilda o ambiente"
    echo "  fix-network - Corrige problemas de rede"
    echo ""
    echo -e "${GREEN}Exemplos:${NC}"
    echo "  $0 up                    # Inicia o ambiente completo"
    echo "  $0 ssh                   # Acessa a VM (auto-start do prompt MCP)"
    echo "  $0 provision             # Reprovisiona a VM"
    echo "  $0 status                # Verifica status"
    echo ""
    echo -e "${CYAN}Comandos Vagrant Diretos:${NC}"
    echo "  vagrant up               # Inicia a VM"
    echo "  vagrant ssh mcp-relational-database-analyzer # SSH para a VM (auto-start prompt)"
    echo "  vagrant halt             # Para a VM"
    echo "  vagrant provision        # Reprovisiona a VM"
    echo "  vagrant reload           # Reinicia a VM"
    echo "  vagrant destroy          # Destrói a VM"
    echo ""
    echo -e "${YELLOW}Arquitetura (VM Única):${NC}"
    echo -e "${CYAN}  • mcp-relational-database-analyzer: MCP + PetClinic + PostgreSQL (192.168.56.10)${NC}"
}

function cmd_up() {
    echo -e "${GREEN}▶ Iniciando ambiente MCP + PetClinic + PostgreSQL...${NC}"
    vagrant up mcp-relational-database-analyzer
    echo -e "${GREEN}✅ Ambiente iniciado!${NC}"
    echo -e "${YELLOW}💡 Acesse:${NC}"
    echo "  • MCP Analyzer: http://localhost:8000"
    echo "  • PetClinic: http://localhost:9080"
    echo "  • PostgreSQL: localhost:5432"
    echo ""
    echo -e "${CYAN}SSH na VM: ${NC}vagrant ssh mcp-relational-database-analyzer"
}

function cmd_down() {
    echo -e "${RED}▶ Parando ambiente...${NC}"
    vagrant halt mcp-relational-database-analyzer
    echo -e "${RED}✅ Ambiente parado!${NC}"
}

function cmd_status() {
    echo -e "${CYAN}▶ Status da VM:${NC}"
    vagrant status mcp-relational-database-analyzer
}

function cmd_ssh() {
    echo -e "${GREEN}▶ Conectando via SSH à VM (auto-start do prompt MCP)...${NC}"
    vagrant ssh mcp-relational-database-analyzer
}

function cmd_logs_mcp() {
    echo -e "${CYAN}▶ Logs do MCP Analyzer:${NC}"
    vagrant ssh mcp-relational-database-analyzer -c "sudo journalctl -u mcp-analyzer.service -f"
}

function cmd_logs_pg() {
    echo -e "${CYAN}▶ Logs do PostgreSQL:${NC}"
    vagrant ssh mcp-relational-database-analyzer -c "sudo journalctl -u postgresql -f"
}

function cmd_logs_app() {
    echo -e "${CYAN}▶ Logs do PetClinic:${NC}"
    vagrant ssh mcp-relational-database-analyzer -c "sudo journalctl -u petclinic.service -f"
}

function cmd_provision() {
    echo -e "${YELLOW}▶ Reprovisionando VM...${NC}"
    vagrant provision mcp-relational-database-analyzer
    echo -e "${GREEN}✅ VM reprovisionada!${NC}"
}

function cmd_reload() {
    echo -e "${YELLOW}▶ Reiniciando VM...${NC}"
    vagrant reload mcp-relational-database-analyzer
    echo -e "${GREEN}✅ VM reiniciada!${NC}"
}

function cmd_clean() {
    echo -e "${RED}▶ Limpando ambiente...${NC}"
    read -p "Tem certeza? Isso destruirá a VM atual (y/N): " confirm
    if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
        vagrant destroy -f mcp-relational-database-analyzer
        echo -e "${GREEN}▶ Reconstruindo ambiente...${NC}"
        vagrant up mcp-relational-database-analyzer
        echo -e "${GREEN}✅ Ambiente reconstruído!${NC}"
    else
        echo -e "${YELLOW}❌ Cancelado.${NC}"
    fi
}

function test_connectivity() {
    echo -e "${CYAN}▶ Testando conectividade dos serviços...${NC}"
    
    # Testa PostgreSQL
    echo -e "${YELLOW}🔍 PostgreSQL (localhost:5432)...${NC}"
    if timeout 5 nc -zv localhost 5432 2>/dev/null; then
        echo -e "${GREEN}✅ PostgreSQL: OK${NC}"
    else
        echo -e "${RED}❌ PostgreSQL: Falha${NC}"
    fi
    
    # Testa MCP Analyzer
    echo -e "${YELLOW}🔍 MCP Analyzer (localhost:8000)...${NC}"
    if curl -s --connect-timeout 5 http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ MCP Analyzer: OK${NC}"
    else
        echo -e "${RED}❌ MCP Analyzer: Falha${NC}"
        echo -e "${YELLOW}   Tentando http://localhost:8000...${NC}"
        if curl -s --connect-timeout 5 http://localhost:8000 > /dev/null 2>&1; then
            echo -e "${GREEN}✅ MCP Analyzer: OK (endpoint raiz)${NC}"
        fi
    fi
    
    # Testa PetClinic
    echo -e "${YELLOW}🔍 PetClinic (localhost:9080)...${NC}"
    if curl -s --connect-timeout 5 http://localhost:9080 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PetClinic: OK${NC}"
    else
        echo -e "${RED}❌ PetClinic: Falha${NC}"
    fi
    
    echo ""
    echo -e "${CYAN}VM Status:${NC}"
    vagrant status mcp-relational-database-analyzer
    
    echo ""
    echo -e "${YELLOW}Para logs detalhados:${NC}"
    echo "  ./manage.sh logs-mcp     # Logs do MCP"
    echo "  ./manage.sh logs-app     # Logs do PetClinic"
    echo "  ./manage.sh logs-pg      # Logs do PostgreSQL"
    
    echo ""
    echo -e "${YELLOW}URLs de acesso:${NC}"
    echo -e "${CYAN}  • PetClinic: http://localhost:9080${NC}"
    echo -e "${CYAN}  • MCP API: http://localhost:8000${NC}"
}

function show_header() {
    local title="$1"
    echo ""
    echo -e "${CYAN}╭──────────────────────────────────────────────╮${NC}"
    echo -e "${CYAN}│ $(printf "%-44s" "$title") │${NC}"
    echo -e "${CYAN}╰──────────────────────────────────────────────╯${NC}"
    echo ""
}

# Main execution
case "${1:-help}" in
    "up"|"start")
        cmd_up
        ;;
    "down"|"stop"|"halt")
        cmd_down
        ;;
    "status")
        cmd_status
        ;;
    "provision")
        cmd_provision
        ;;
    "reload"|"restart")
        cmd_reload
        ;;
    "ssh")
        cmd_ssh
        ;;
    "logs-mcp")
        cmd_logs_mcp
        ;;
    "logs-pg")
        cmd_logs_pg
        ;;
    "logs-app")
        cmd_logs_app
        ;;
    "test")
        test_connectivity
        ;;
    "clean"|"destroy")
        cmd_clean
        ;;
    "fix-network")
        echo -e "${YELLOW}▶ Corrigindo problemas de rede...${NC}"
        ./fix-network.sh
        ;;
    "help"|*)
        show_usage
        ;;
esac