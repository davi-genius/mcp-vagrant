@echo off
REM MCP Vagrant - Utilitários de Gerenciamento - Windows
REM Compass UOL Edition

setlocal enabledelayedexpansion

if "%1"=="" goto show_usage
if "%1"=="help" goto show_usage

if "%1"=="up" goto cmd_up
if "%1"=="start" goto cmd_up
if "%1"=="down" goto cmd_down
if "%1"=="stop" goto cmd_down
if "%1"=="halt" goto cmd_down
if "%1"=="status" goto cmd_status
if "%1"=="ssh" goto cmd_ssh
if "%1"=="logs-mcp" goto cmd_logs_mcp
if "%1"=="logs-pg" goto cmd_logs_pg
if "%1"=="logs-app" goto cmd_logs_app
if "%1"=="test" goto cmd_test
if "%1"=="provision" goto cmd_provision
if "%1"=="reload" goto cmd_reload
if "%1"=="restart" goto cmd_reload
if "%1"=="clean" goto cmd_clean
if "%1"=="destroy" goto cmd_clean

echo Comando desconhecido: %1
goto show_usage

:show_usage
echo.
echo MCP Database Analyzer - Vagrant Edition
echo.
echo Uso: %0 [comando]
echo.
echo Comandos disponíveis:
echo   up        - Inicia a VM
echo   down      - Para a VM
echo   status    - Mostra status da VM
echo   ssh       - SSH direto para a VM (auto-start prompt MCP)
echo   logs-mcp  - Logs do MCP Analyzer
echo   logs-pg   - Logs do PostgreSQL
echo   logs-app  - Logs do PetClinic
echo   test      - Testa conectividade
echo   provision - Reprovisiona a VM
echo   reload    - Reinicia a VM
echo   clean     - Limpa e rebuilda o ambiente
echo.
echo Exemplos:
echo   %0 up                    # Inicia o ambiente completo
echo   %0 ssh                   # Acessa a VM (auto-start do prompt MCP)
echo   %0 provision             # Reprovisiona a VM
echo   %0 status                # Verifica status
echo.
echo Comandos Vagrant Diretos:
echo   vagrant up mcp-relational-database-analyzer       # Inicia a VM
echo   vagrant ssh mcp-relational-database-analyzer      # SSH para a VM (auto-start prompt)
echo   vagrant halt mcp-relational-database-analyzer     # Para a VM
echo   vagrant provision mcp-relational-database-analyzer # Reprovisiona a VM
echo   vagrant reload mcp-relational-database-analyzer   # Reinicia a VM
echo   vagrant destroy mcp-relational-database-analyzer  # Destrói a VM
echo.
echo Arquitetura (VM Única):
echo   • mcp-relational-database-analyzer: MCP + PetClinic + PostgreSQL (192.168.56.10)
echo.
goto end

:cmd_up
echo ▶ Iniciando ambiente MCP + PetClinic + PostgreSQL...
vagrant up mcp-relational-database-analyzer
if %errorlevel% equ 0 (
    echo ✅ Ambiente iniciado!
    echo 💡 Acesse:
    echo   • MCP Analyzer: http://localhost:8000
    echo   • PetClinic: http://localhost:9080
    echo   • PostgreSQL: localhost:5432
    echo.
    echo SSH na VM: vagrant ssh mcp-relational-database-analyzer
) else (
    echo ❌ Erro ao iniciar ambiente
)
goto end

:cmd_down
echo ▶ Parando ambiente...
vagrant halt mcp-relational-database-analyzer
if %errorlevel% equ 0 (
    echo ✅ Ambiente parado!
) else (
    echo ❌ Erro ao parar ambiente
)
goto end

:cmd_status
echo ▶ Status da VM:
vagrant status mcp-relational-database-analyzer
goto end

:cmd_ssh
echo ▶ Conectando via SSH à VM (auto-start do prompt MCP)...
vagrant ssh mcp-relational-database-analyzer
goto end

:cmd_logs_mcp
echo ▶ Logs do MCP Analyzer:
vagrant ssh mcp-relational-database-analyzer -c "sudo journalctl -u mcp-analyzer.service -f"
goto end

:cmd_logs_pg
echo ▶ Logs do PostgreSQL:
vagrant ssh mcp-relational-database-analyzer -c "sudo journalctl -u postgresql -f"
goto end

:cmd_logs_app
echo ▶ Logs do PetClinic:
vagrant ssh mcp-relational-database-analyzer -c "sudo journalctl -u petclinic.service -f"
goto end

:cmd_provision
echo ▶ Reprovisionando VM...
vagrant provision mcp-relational-database-analyzer
if %errorlevel% equ 0 (
    echo ✅ VM reprovisionada!
) else (
    echo ❌ Erro ao reprovisionar VM
)
goto end

:cmd_reload
echo ▶ Reiniciando VM...
vagrant reload mcp-relational-database-analyzer
if %errorlevel% equ 0 (
    echo ✅ VM reiniciada!
) else (
    echo ❌ Erro ao reiniciar VM
)
goto end

:cmd_clean
echo ▶ Limpando ambiente...
set /p confirm="Tem certeza? Isso destruirá a VM atual (y/N): "
if /i "!confirm!"=="y" (
    vagrant destroy -f mcp-relational-database-analyzer
    echo ▶ Reconstruindo ambiente...
    vagrant up mcp-relational-database-analyzer
    if %errorlevel% equ 0 (
        echo ✅ Ambiente reconstruído!
    ) else (
        echo ❌ Erro ao reconstruir ambiente
    )
) else (
    echo ❌ Cancelado.
)
goto end

:cmd_test
echo ▶ Testando conectividade dos serviços...
echo.

REM Testa PostgreSQL
echo 🔍 PostgreSQL (localhost:5432)...
powershell -Command "try { $tcp = New-Object System.Net.Sockets.TcpClient; $tcp.Connect('localhost', 5432); $tcp.Close(); Write-Host '✅ PostgreSQL: OK' -ForegroundColor Green } catch { Write-Host '❌ PostgreSQL: Falha' -ForegroundColor Red }"

REM Testa MCP Analyzer
echo 🔍 MCP Analyzer (localhost:8000)...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/health' -TimeoutSec 5 -UseBasicParsing; Write-Host '✅ MCP Analyzer: OK' -ForegroundColor Green } catch { Write-Host '❌ MCP Analyzer: Falha' -ForegroundColor Red }"

REM Testa PetClinic
echo 🔍 PetClinic (localhost:9080)...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:9080' -TimeoutSec 5 -UseBasicParsing; Write-Host '✅ PetClinic: OK' -ForegroundColor Green } catch { Write-Host '❌ PetClinic: Falha' -ForegroundColor Red }"

echo.
echo VM Status:
vagrant status mcp-relational-database-analyzer

echo.
echo Para logs detalhados:
echo   %0 logs-mcp     # Logs do MCP
echo   %0 logs-app     # Logs do PetClinic
echo   %0 logs-pg      # Logs do PostgreSQL

echo.
echo URLs de acesso:
echo   • PetClinic: http://localhost:9080
echo   • MCP API: http://localhost:8000
goto end

:end
echo.