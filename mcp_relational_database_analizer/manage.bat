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
if "%1"=="setup" goto cmd_setup
if "%1"=="fix" goto cmd_fix

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
echo   ssh       - SSH para a VM
echo   logs-mcp  - Logs do MCP Analyzer
echo   logs-pg   - Logs do PostgreSQL
echo   logs-app  - Logs do PetClinic
echo   test      - Testa conectividade
echo   provision - Reprovisiona a VM
echo   reload    - Reinicia a VM
echo   clean     - Limpa e rebuilda o ambiente
echo   setup     - Setup inicial completo
echo   fix       - Corrigir problemas comuns
echo.
echo Exemplos:
echo   %0 setup                 # Setup inicial completo
echo   %0 up                    # Inicia o ambiente completo
echo   %0 ssh                   # Acessa a VM
echo   %0 provision             # Reprovisiona a VM
echo   %0 status                # Verifica status
echo   %0 fix                   # Corrigir problemas
echo.
echo Comandos Vagrant Diretos:
echo   vagrant up               # Inicia a VM
echo   vagrant ssh              # SSH para a VM
echo   vagrant halt             # Para a VM
echo   vagrant provision        # Reprovisiona a VM
echo   vagrant reload           # Reinicia a VM
echo   vagrant destroy          # Destrói a VM
echo.
echo Arquitetura (VM Única):
echo   • mcp-relational-database-analyzer: MCP + PetClinic + PostgreSQL (192.168.56.10)
echo.
goto end

:cmd_up
vagrant up
goto end

:cmd_down
vagrant halt
goto end

:cmd_status
vagrant status
goto end

:cmd_ssh
vagrant ssh
goto end

:cmd_logs_mcp
vagrant ssh -c "sudo journalctl -u mcp-analyzer.service -f"
goto end

:cmd_logs_pg
vagrant ssh -c "sudo journalctl -u postgresql -f"
goto end

:cmd_logs_app
vagrant ssh -c "sudo journalctl -u petclinic.service -f"
goto end

:cmd_provision
vagrant provision
goto end

:cmd_reload
vagrant reload
goto end

:cmd_clean
set /p confirm="Tem certeza? Isso destruirá a VM atual (y/N): "
if /i "!confirm!"=="y" (
    vagrant destroy -f
    vagrant up
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
vagrant status

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

:cmd_setup
echo ▶ Setup inicial completo do MCP Database Analyzer...
echo.
echo 1. Iniciando ambiente Vagrant...
vagrant up
echo.
echo 2. Verificando provisionamento...
vagrant provision
echo.
echo 3. Copiando script MCP (correção)...
vagrant ssh -c "sudo cp /opt/mcp/mcp-prompt.py /home/vagrant/ && sudo chown vagrant:vagrant /home/vagrant/mcp-prompt.py && sudo chmod +x /home/vagrant/mcp-prompt.py"
echo.
echo 4. Testando conectividade...
%0 test
echo.
echo ✅ Setup completo! Execute: %0 ssh
goto end

:cmd_fix
echo ▶ Corrigindo problemas comuns...
echo.
echo 1. Recopiando script MCP...
vagrant ssh -c "sudo cp /opt/mcp/mcp-prompt.py /home/vagrant/ && sudo chown vagrant:vagrant /home/vagrant/mcp-prompt.py && sudo chmod +x /home/vagrant/mcp-prompt.py"
echo.
echo 2. Verificando serviços...
vagrant ssh -c "sudo systemctl restart mcp-analyzer petclinic"
echo.
echo 3. Testando banco...
vagrant ssh -c "sudo -u postgres psql -d petclinic -c 'SELECT count(*) FROM information_schema.tables;'"
echo.
echo ✅ Correções aplicadas!
goto end

:end
echo.