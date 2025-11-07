#!/bin/bash

# Setup Script para MCP Database Analyzer
# Funciona em Windows (Git Bash/WSL), Linux e macOS

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Detectar sistema operacional
detect_os() {
    case "$(uname -s)" in
        Linux*)     OS=Linux;;
        Darwin*)    OS=Mac;;
        CYGWIN*)    OS=Cygwin;;
        MINGW*)     OS=MinGw;;
        MSYS*)      OS=Git_Bash;;
        *)          OS="UNKNOWN:$(uname -s)"
    esac
    echo $OS
}

# Verificar dependências
check_dependencies() {
    echo -e "${CYAN}🔍 Verificando dependências...${NC}"
    
    # Verificar Vagrant
    if ! command -v vagrant &> /dev/null; then
        echo -e "${RED}❌ Vagrant não encontrado. Instale: https://www.vagrantup.com/downloads${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ Vagrant: $(vagrant --version)${NC}"
    fi
    
    # Verificar VirtualBox
    if ! command -v VBoxManage &> /dev/null; then
        echo -e "${RED}❌ VirtualBox não encontrado. Instale: https://www.virtualbox.org/wiki/Downloads${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ VirtualBox: $(VBoxManage --version)${NC}"
    fi
    
    echo -e "${GREEN}✅ Todas as dependências estão instaladas!${NC}"
}

# Verificar recursos do sistema
check_resources() {
    echo -e "${CYAN}🔍 Verificando recursos do sistema...${NC}"
    
    # Verificar RAM disponível
    case $(detect_os) in
        Linux)
            TOTAL_RAM=$(free -m | awk 'NR==2{printf "%.0f", $2/1024}')
            ;;
        Mac)
            TOTAL_RAM=$(sysctl -n hw.memsize | awk '{printf "%.0f", $1/1024/1024/1024}')
            ;;
        *)
            TOTAL_RAM=8  # Assumir 8GB para Windows
            ;;
    esac
    
    if [ "$TOTAL_RAM" -lt 6 ]; then
        echo -e "${YELLOW}⚠️  RAM disponível: ${TOTAL_RAM}GB (recomendado: 6GB+)${NC}"
        echo -e "${YELLOW}   O ambiente pode ficar lento com pouca RAM${NC}"
    else
        echo -e "${GREEN}✅ RAM disponível: ${TOTAL_RAM}GB${NC}"
    fi
}

# Configurar ambiente
setup_environment() {
    echo -e "${CYAN}🔧 Configurando ambiente...${NC}"
    
    # Criar diretórios necessários se não existirem
    mkdir -p logs
    mkdir -p config
    
    # Tornar scripts executáveis
    chmod +x manage.sh 2>/dev/null || true
    
    echo -e "${GREEN}✅ Ambiente configurado!${NC}"
}

# Função principal
main() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                                                                  ║"
    echo "║           🚀 MCP DATABASE ANALYZER - SETUP                      ║"
    echo "║              Compass UOL - Vagrant Edition                      ║"
    echo "║                                                                  ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${YELLOW}Sistema detectado: $(detect_os)${NC}"
    echo ""
    
    check_dependencies
    echo ""
    
    check_resources
    echo ""
    
    setup_environment
    echo ""
    
    echo -e "${GREEN}🎉 Setup concluído com sucesso!${NC}"
    echo ""
    echo -e "${CYAN}Próximos passos:${NC}"
    echo "  1. ${YELLOW}./manage.sh up${NC}     - Iniciar o ambiente"
    echo "  2. ${YELLOW}./manage.sh ssh${NC}    - Acessar via SSH (auto-start MCP)"
    echo "  3. ${YELLOW}./manage.sh test${NC}   - Testar conectividade"
    echo ""
    echo -e "${CYAN}URLs de acesso:${NC}"
    echo "  • MCP API: http://localhost:8000"
    echo "  • PetClinic: http://localhost:8080"
    echo "  • PostgreSQL: localhost:5432"
    echo ""
    echo -e "${BLUE}💡 Para ajuda: ./manage.sh help${NC}"
}

# Executar se chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi