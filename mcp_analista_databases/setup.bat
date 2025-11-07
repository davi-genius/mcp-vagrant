@echo off
REM Setup Script para MCP Database Analyzer - Windows
REM Funciona com Git Bash, PowerShell ou CMD

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║           🚀 MCP DATABASE ANALYZER - SETUP                      ║
echo ║              Compass UOL - Vagrant Edition                      ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo Sistema detectado: Windows
echo.

REM Verificar Vagrant
vagrant --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Vagrant não encontrado. Instale: https://www.vagrantup.com/downloads
    pause
    exit /b 1
) else (
    echo ✅ Vagrant encontrado
)

REM Verificar VirtualBox
VBoxManage --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ VirtualBox não encontrado. Instale: https://www.virtualbox.org/wiki/Downloads
    pause
    exit /b 1
) else (
    echo ✅ VirtualBox encontrado
)

echo.
echo ✅ Todas as dependências estão instaladas!
echo.

REM Criar diretórios necessários
if not exist "logs" mkdir logs
if not exist "config" mkdir config

echo ✅ Ambiente configurado!
echo.
echo 🎉 Setup concluído com sucesso!
echo.
echo Próximos passos:
echo   1. manage.bat up     - Iniciar o ambiente
echo   2. manage.bat ssh    - Acessar via SSH (auto-start MCP)
echo   3. manage.bat test   - Testar conectividade
echo.
echo URLs de acesso:
echo   • MCP API: http://localhost:8000
echo   • PetClinic: http://localhost:8080
echo   • PostgreSQL: localhost:5432
echo.
echo 💡 Para ajuda: manage.bat help
echo.
pause