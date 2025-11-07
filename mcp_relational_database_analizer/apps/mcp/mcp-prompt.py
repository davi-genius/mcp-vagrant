#!/usr/bin/env python3
"""
MCP Interactive Prompt - PostgreSQL Performance Analyzer
Compass UOL Edition
"""
import sys
import os
import psycopg2
import json
import re
from typing import Dict, List, Optional
import requests
from datetime import datetime

# Cores do UOL Compass e Amazon Q
class AmazonColors:
    ORANGE = '\033[38;5;214m'     # Laranja Amazon Q
    UOL_ORANGE = '\033[38;5;202m' # Laranja UOL vibrante (círculo externo)
    UOL_RED = '\033[38;5;196m'    # Vermelho UOL (círculo interno)
    UOL_YELLOW = '\033[38;5;220m' # Amarelo UOL (círculo meio)
    BLUE = '\033[38;5;33m'        # Azul Amazon Q
    DARK_BLUE = '\033[38;5;17m'   # Azul escuro para texto
    WHITE = '\033[97m'            # Branco
    GRAY = '\033[90m'             # Cinza
    BLACK = '\033[30m'            # Preto para "compass.uol"
    RESET = '\033[0m'             # Reset

# Configurações
MCP_URL = "http://localhost:8000"
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "petclinic",
    "username": "petclinic",
    "password": "petclinic"
}

def print_welcome_auto_start():
    """Exibe mensagem de boas-vindas para auto-start"""
    print(f"{AmazonColors.ORANGE}")
    print("    >> Conectando ao MCP Database Analyzer...")
    print("    >> Sistema inicializado com sucesso!")
    print(f"{AmazonColors.RESET}")
    print()

def is_auto_started():
    """Verifica se foi iniciado automaticamente"""
    return os.getenv('MCP_PROMPT_STARTED') == '1' or os.getenv('SSH_CONNECTION') is not None

# Logo ASCII da Compass UOL (baseado na imagem real)
COMPASS_LOGO = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                                                                              ║
║                                                                              ║
║                                                                              ║
║                                                                              ║
║          ██████╗ ██████╗ ███╗   ███╗██████╗  █████╗ ███████╗███████╗        ║
║         ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔════╝        ║
║         ██║     ██║   ██║██╔████╔██║██████╔╝███████║███████╗███████╗        ║
║         ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══██║╚════██║╚════██║        ║
║         ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ██║  ██║███████║███████║        ║
║          ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝        ║
║                                                                              ║
║                                                                              ║
║                                                                              ║
║                               ██╗   ██╗ ██████╗ ██╗                        ║
║                               ██║   ██║██╔═══██╗██║                        ║
║                               ██║   ██║██║   ██║██║                        ║
║                               ██║   ██║██║   ██║██║                        ║
║                               ╚██████╔╝╚██████╔╝███████╗                   ║
║                                ╚═════╝  ╚═════╝ ╚══════╝                   ║
║                                                                              ║
║                      PostgreSQL Performance Analyzer                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

def print_logo():
    """Exibe logo da Compass UOL limpo - COMPASS em preto, UOL em laranja"""
    logo_lines = COMPASS_LOGO.split('\n')
    for i, line in enumerate(logo_lines):
        if i in [1, 29]:  # Bordas superior e inferior
            print(f"{AmazonColors.BLUE}{line}{AmazonColors.RESET}")
        elif "██╗   ██╗ ██████╗ ██╗" in line or "██║   ██║██╔═══██╗██║" in line or "██║   ██║██║   ██║██║" in line or "╚██████╔╝╚██████╔╝███████╗" in line or "╚═════╝  ╚═════╝ ╚══════╝" in line:
            # "UOL" em laranja
            print(f"{AmazonColors.UOL_ORANGE}{line}{AmazonColors.RESET}")
        elif "██" in line and any(word in line for word in ["██████╗", "██╔", "██║", "╚██████╗", "╚═════╝"]):
            # "COMPASS" (incluindo SS na mesma linha) em preto
            print(f"{AmazonColors.BLACK}{line}{AmazonColors.RESET}")
        elif "PostgreSQL Performance Analyzer" in line:
            # Subtítulo em azul
            print(f"{AmazonColors.BLUE}{line}{AmazonColors.RESET}")
        elif line.strip().startswith("║") or line.strip().startswith("╚") or line.strip().startswith("╔"):
            # Bordas em azul
            print(f"{AmazonColors.BLUE}{line}{AmazonColors.RESET}")
        else:
            print(line)
    
    print(f"{AmazonColors.GRAY}        Versão: 1.0.0 | Data: {datetime.now().strftime('%d/%m/%Y %H:%M')} | compass.uol{AmazonColors.RESET}")
    print()

def print_welcome():
    """Exibe o logo da Compass e menu principal"""
    print_logo()
    print(f"{AmazonColors.BLUE}>> Digite 'mcp help' para ver os comandos disponíveis{AmazonColors.RESET}")
    print()

def print_header(title):
    """Exibe cabeçalho formatado"""
    print(f"\n{AmazonColors.BLUE}{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}{AmazonColors.RESET}\n")

def check_mcp_status():
    """Verifica status do MCP"""
    try:
        response = requests.get(f"{MCP_URL}/health", timeout=2)
        if response.status_code == 200:
            return True, "Healthy"
        return False, "Unhealthy"
    except:
        return False, "Offline"

def list_databases():
    """Lista todos os bancos de dados disponíveis"""
    print_header("BANCOS DE DADOS DISPONIVEIS")
    
    try:
        import psycopg2
        # Conectar no postgres padrão para listar databases
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database='postgres',  # Conectar no postgres padrão
            user=DB_CONFIG['username'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname")
        databases = cursor.fetchall()
        
        for i, (dbname,) in enumerate(databases, 1):
            print(f"{i}. {dbname}")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erro ao conectar com PostgreSQL: {e}")
        print("Verifique se o PostgreSQL está rodando e as credenciais estão corretas.")

def list_tables(dbname=None):
    """Lista todas as tabelas de um banco"""
    if not dbname:
        dbname = DB_CONFIG['dbname']
    
    print_header(f"TABELAS DO BANCO: {dbname}")
    
    try:
        import psycopg2
        # Conectar no banco especificado
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=dbname,
            user=DB_CONFIG['username'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Query para listar tabelas com contagem de colunas
        cursor.execute("""
            SELECT 
                table_name,
                (SELECT COUNT(*) 
                 FROM information_schema.columns 
                 WHERE table_name = t.table_name 
                   AND table_schema = 'public') as column_count
            FROM information_schema.tables t
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        
        if tables:
            for i, (table_name, column_count) in enumerate(tables, 1):
                print(f"{i}. {table_name} ({column_count} colunas)")
        else:
            print("Nenhuma tabela encontrada no schema public.")
            print("\n>> DICA: O banco pode estar vazio. Execute o PetClinic primeiro:")
            print("   curl http://localhost:9080")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erro ao conectar com PostgreSQL: {e}")
        print("Verifique se o PostgreSQL está rodando e as base de dados existe.")

def show_table_details(table_name, dbname=None):
    """Mostra detalhes de uma tabela específica"""
    if not dbname:
        dbname = DB_CONFIG['dbname']
    
    print_header(f"DETALHES DA TABELA: {table_name}")
    
    try:
        import psycopg2
        # Conectar no banco especificado
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=dbname,
            user=DB_CONFIG['username'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Buscar informações das colunas
        cursor.execute("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = %s AND table_schema = 'public'
            ORDER BY ordinal_position
        """, (table_name,))
        
        columns = cursor.fetchall()
        
        if columns:
            print("\nCOLUNAS:")
            print("-" * 70)
            for column_name, data_type, max_length, is_nullable, default in columns:
                nullable = "NULL" if is_nullable == 'YES' else "NOT NULL"
                type_info = data_type
                if max_length:
                    type_info += f"({max_length})"
                default_info = f" DEFAULT {default}" if default else ""
                print(f"  - {column_name}: {type_info} {nullable}{default_info}")
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\nTOTAL DE REGISTROS: {count}")
        else:
            print(f"Tabela '{table_name}' não encontrada.")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erro ao conectar com PostgreSQL: {e}")

def show_db_actions():
    """Mostra menu de ações do banco de dados"""
    print_header("MENU DE ACOES")
    
    print("Escolha uma opcao:")
    print()
    print("  1 - Listar bancos de dados")
    print("  2 - Listar tabelas do banco atual")
    print("  3 - Executar prompts prontos")
    print("  4 - Informações da aplicação")
    print("  0 - Voltar")
    print()
    
    choice = input("Digite o numero da opcao: ").strip()
    
    if choice == '1':
        list_databases()
        print()
        show_db_actions()
    elif choice == '2':
        list_tables()
        print()
        show_db_actions()
    elif choice == '3':
        show_prompts_menu()
        print()
        show_db_actions()
    elif choice == '4':
        show_mcp_app()
        print()
        show_db_actions()
    elif choice == '0':
        return
    else:
        print("Opção inválida!")
        print()
        show_db_actions()

def show_prompts_menu():
    """Mostra menu de prompts organizados por categoria"""
    try:
        print_header("PROMPTS ORGANIZADOS DE ANALISE")
        print("PostgreSQL Performance Analyzer - Compass UOL")
        print("=" * 60)
        print()
        
        # Prompts organizados por categoria e prioridade
        print(f"{AmazonColors.UOL_ORANGE}>> ESTRUTURA E INVENTÁRIO (EXECUTAR PRIMEIRO):{AmazonColors.RESET}")
        print(f"  01. EST-001: Estrutura Completa do Banco              [PRIORIDADE ALTA]")
        print(f"  02. EST-002: Inventário de Tabelas                    [PRIORIDADE ALTA]")
        print(f"  03. EST-003: Contagem de Registros                    [PRIORIDADE ALTA]")
        print()
        
        print(f"{AmazonColors.BLUE}>> DADOS DE NEGÓCIO (EXECUTAR SEGUNDO):{AmazonColors.RESET}")
        print(f"  04. NEG-001: Proprietários por Localização           [PRIORIDADE MÉDIA]")
        print(f"  05. NEG-002: Cadastro de Pets Completo               [PRIORIDADE MÉDIA]")
        print(f"  06. NEG-003: Equipe Veterinária                      [PRIORIDADE MÉDIA]")
        print(f"  07. NEG-004: Análise de Visitas                      [PRIORIDADE MÉDIA]")
        print()
        
        print(f"{AmazonColors.ORANGE}>> PERFORMANCE E OTIMIZAÇÃO (EXECUTAR POR ÚLTIMO):{AmazonColors.RESET}")
        print(f"  08. PERF-001: Análise de Query                       [PRIORIDADE ALTA]")
        print(f"  09. PERF-002: Recomendação de Índices                [PRIORIDADE ALTA]")
        print(f"  10. PERF-003: Configurações do Sistema               [PRIORIDADE MÉDIA]")
        print()
        
        print(f"{AmazonColors.GRAY}>> INSTRUÇÕES DE USO:{AmazonColors.RESET}")
        print(f"  • Execute na ordem sequencial (01→10) para análise completa")
        print(f"  • Prompts [PRIORIDADE ALTA] são essenciais para diagnóstico")
        print(f"  • Prompts [PRIORIDADE MÉDIA] fornecem insights adicionais")
        print(f"  • Digite 'all' para executar sequência completa")
        print()
        
        prompt_id = input(f"{AmazonColors.ORANGE}Digite o número (01-10) ou 'all' (0=voltar): {AmazonColors.RESET}").strip()
        
        if prompt_id.lower() == 'all':
            execute_all_prompts_sequence()
        elif prompt_id and prompt_id != '0':
            # Normalizar ID (aceitar 1 ou 01)
            if prompt_id.isdigit():
                normalized_id = f"{int(prompt_id):02d}"
                execute_prompt(normalized_id)
            else:
                execute_prompt(prompt_id)
        elif prompt_id == '0':
            return
            
    except Exception as e:
        print(f"Erro ao carregar prompts: {e}")
        print("Verifique se o serviço MCP está rodando.")

def execute_prompt(prompt_id):
    """Executa análises diretas no banco com nova nomenclatura"""
    try:
        print(f">> Conectando ao banco de dados...")
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['dbname'],
            user=DB_CONFIG['username'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        print(f">> Conexão estabelecida com sucesso!")
        
        # Mapear IDs para nomes descritivos
        prompt_names = {
            '01': 'EST-001: Estrutura Completa do Banco',
            '02': 'EST-002: Inventário de Tabelas', 
            '03': 'EST-003: Contagem de Registros',
            '04': 'NEG-001: Proprietários por Localização',
            '05': 'NEG-002: Cadastro de Pets Completo',
            '06': 'NEG-003: Equipe Veterinária',
            '07': 'NEG-004: Análise de Visitas',
            '08': 'PERF-001: Análise de Query',
            '09': 'PERF-002: Recomendação de Índices',
            '10': 'PERF-003: Configurações do Sistema'
        }
        
        prompt_name = prompt_names.get(prompt_id, f"ANÁLISE {prompt_id}")
        print_header(f"EXECUTANDO: {prompt_name}")
        
        if prompt_id == '01':  # EST-001: Estrutura Completa
            print(">> Analisando estrutura completa do banco...\n")
            cursor.execute("""
                SELECT 
                    t.table_name,
                    t.table_type,
                    COUNT(c.column_name) as column_count,
                    pg_size_pretty(pg_total_relation_size(quote_ident(t.table_name)::regclass)) as table_size
                FROM information_schema.tables t
                LEFT JOIN information_schema.columns c ON t.table_name = c.table_name AND c.table_schema = 'public'
                WHERE t.table_schema = 'public'
                GROUP BY t.table_name, t.table_type
                ORDER BY pg_total_relation_size(quote_ident(t.table_name)::regclass) DESC;
            """)
            results = cursor.fetchall()
            if results:
                print(">> ESTRUTURA DAS TABELAS:")
                print("-" * 60)
                for table, table_type, col_count, size in results:
                    print(f">> {table}: {col_count} colunas, {size}, tipo: {table_type}")
                    
                    # Mostrar colunas de cada tabela
                    cursor.execute("""
                        SELECT column_name, data_type, is_nullable, column_default
                        FROM information_schema.columns
                        WHERE table_name = %s AND table_schema = 'public'
                        ORDER BY ordinal_position
                    """, (table,))
                    columns = cursor.fetchall()
                    for col_name, data_type, nullable, default in columns[:5]:  # Mostrar apenas primeiras 5
                        null_info = "NULL" if nullable == 'YES' else "NOT NULL"
                        default_info = f" DEFAULT {default}" if default else ""
                        print(f"   • {col_name}: {data_type} ({null_info}){default_info}")
                    if len(columns) > 5:
                        print(f"   ... e mais {len(columns) - 5} colunas")
                    print()
            else:
                print("[!] Nenhuma tabela encontrada.")
                print(">> DIAGNÓSTICO:")
                print("   • Verifique se o PetClinic foi iniciado pelo menos uma vez")
                print("   • Execute: vagrant ssh -c 'systemctl status petclinic'")
                print("   • As tabelas são criadas automaticamente na primeira execução")
                
                # Verificar se o banco existe
                cursor.execute("SELECT current_database()")
                current_db = cursor.fetchone()[0]
                print(f"   • Banco atual: {current_db}")
                
                # Listar todos os schemas
                cursor.execute("SELECT schema_name FROM information_schema.schemata")
                schemas = cursor.fetchall()
                schema_list = [s[0] for s in schemas]
                print(f"   • Schemas disponíveis: {', '.join(schema_list)}")
                
        elif prompt_id == '02':  # EST-002: Inventário de Tabelas
            print(">> Gerando inventário detalhado...\n")
            cursor.execute("""
                SELECT 
                    schemaname,
                    relname as tablename,
                    n_live_tup as live_tuples,
                    n_dead_tup as dead_tuples,
                    last_vacuum,
                    last_analyze
                FROM pg_stat_user_tables
                ORDER BY n_live_tup DESC;
            """)
            results = cursor.fetchall()
            if results:
                print(">> INVENTÁRIO DETALHADO:")
                print("-" * 80)
                for schema, table, live, dead, vacuum, analyze in results:
                    vacuum_info = vacuum.strftime('%Y-%m-%d %H:%M') if vacuum else 'Nunca'
                    analyze_info = analyze.strftime('%Y-%m-%d %H:%M') if analyze else 'Nunca'
                    print(f"   {table}: {live:,} registros ativos, {dead} mortos")
                    print(f"   >> Último VACUUM: {vacuum_info} | Último ANALYZE: {analyze_info}")
                    print()
            else:
                print("[!] Nenhuma estatística encontrada.")
                
        elif prompt_id == '03':  # EST-003: Contagem de Registros
            print(">> Contando registros em todas as tabelas...\n")
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' ORDER BY table_name
            """)
            tables = cursor.fetchall()
            if tables:
                total_records = 0
                print(">> CONTAGEM POR TABELA:")
                print("-" * 40)
                for (table_name,) in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    total_records += count
                    print(f"   {table_name:15}: {count:,} registros")
                print("-" * 40)
                print(f">> TOTAL GERAL: {total_records:,} registros")
            else:
                print("[!] Nenhuma tabela encontrada.")
                
        elif prompt_id == '04':  # NEG-001: Proprietários por Localização
            print("🌍 Analisando distribuição geográfica...\n")
            cursor.execute("""
                SELECT 
                    city,
                    COUNT(*) as total_owners,
                    COUNT(DISTINCT last_name) as unique_surnames,
                    COUNT(DISTINCT telephone) as unique_phones
                FROM owners 
                GROUP BY city 
                ORDER BY total_owners DESC;
            """)
            results = cursor.fetchall()
            if results:
                print(">> DISTRIBUIÇÃO POR CIDADE:")
                print("-" * 50)
                for city, total, surnames, phones in results:
                    print(f"🌆 {city:15}: {total:2} proprietários, {surnames} sobrenomes únicos")
            else:
                print("[!] Nenhum proprietário encontrado.")
                
        elif prompt_id == '05':  # NEG-002: Cadastro de Pets
            print(">> Analisando cadastro de pets...\n")
            cursor.execute("""
                SELECT 
                    p.name as pet_name,
                    t.name as pet_type,
                    EXTRACT(YEAR FROM AGE(p.birth_date)) as age_years,
                    o.first_name || ' ' || o.last_name as owner_name,
                    o.city
                FROM pets p
                JOIN types t ON p.type_id = t.id
                JOIN owners o ON p.owner_id = o.id
                ORDER BY age_years DESC
                LIMIT 10;
            """)
            results = cursor.fetchall()
            if results:
                print("🐾 TOP 10 PETS MAIS VELHOS:")
                print("-" * 60)
                for pet, pet_type, age, owner, city in results:
                    print(f"   {pet} ({pet_type}): {age} anos - {owner} ({city})")
            else:
                print("[!] Nenhum pet encontrado.")
                
        elif prompt_id == '10':  # PERF-003: Configurações
            print(">> Verificando configurações críticas...\n")
            cursor.execute("""
                SELECT name, setting, unit, context 
                FROM pg_settings 
                WHERE name IN ('max_connections', 'shared_buffers', 'work_mem', 'maintenance_work_mem', 'effective_cache_size')
                ORDER BY name
            """)
            configs = cursor.fetchall()
            if configs:
                print(">> CONFIGURAÇÕES CRÍTICAS:")
                print("-" * 50)
                for name, setting, unit, context in configs:
                    unit_str = f" {unit}" if unit else ""
                    print(f"   {name:20}: {setting}{unit_str} ({context})")
            else:
                print("[!] Configurações não encontradas.")
                
        elif prompt_id == '06':  # NEG-003: Equipe Veterinária
            print(">> Analisando equipe veterinária...\n")
            cursor.execute("""
                SELECT 
                    v.first_name || ' ' || v.last_name as vet_name,
                    COUNT(DISTINCT s.name) as specialties_count,
                    STRING_AGG(s.name, ', ') as specialties
                FROM vets v
                LEFT JOIN vet_specialties vs ON v.id = vs.vet_id
                LEFT JOIN specialties s ON vs.specialty_id = s.id
                GROUP BY v.id, v.first_name, v.last_name
                ORDER BY specialties_count DESC;
            """)
            results = cursor.fetchall()
            if results:
                print(">> EQUIPE VETERINÁRIA:")
                print("-" * 60)
                for vet_name, spec_count, specialties in results:
                    specs = specialties if specialties else "Clínico Geral"
                    print(f"   {vet_name}: {spec_count} especialidades ({specs})")
            else:
                print("[!] Nenhum veterinário encontrado.")
                
        elif prompt_id == '07':  # NEG-004: Análise de Visitas
            print(">> Analisando padrões de visitas...\n")
            cursor.execute("""
                SELECT 
                    EXTRACT(YEAR FROM visit_date) as year,
                    EXTRACT(MONTH FROM visit_date) as month,
                    COUNT(*) as visit_count,
                    COUNT(DISTINCT pet_id) as unique_pets
                FROM visits 
                WHERE visit_date IS NOT NULL
                GROUP BY EXTRACT(YEAR FROM visit_date), EXTRACT(MONTH FROM visit_date)
                ORDER BY year DESC, month DESC
                LIMIT 12;
            """)
            results = cursor.fetchall()
            if results:
                print(">> VISITAS POR MÊS:")
                print("-" * 50)
                for year, month, visits, pets in results:
                    print(f"📅 {int(year)}/{int(month):02d}: {visits} visitas de {pets} pets únicos")
            else:
                print("[!] Nenhuma visita encontrada.")
                
        elif prompt_id == '08':  # PERF-001: Análise de Query
            print(">> Analisando performance de queries...\n")
            cursor.execute("""
                SELECT 
                    schemaname,
                    relname as tablename,
                    seq_scan,
                    seq_tup_read,
                    idx_scan,
                    idx_tup_fetch,
                    n_tup_ins + n_tup_upd + n_tup_del as total_modifications
                FROM pg_stat_user_tables
                ORDER BY seq_scan DESC;
            """)
            results = cursor.fetchall()
            if results:
                print(">> ESTATÍSTICAS DE ACESSO:")
                print("-" * 70)
                for schema, table, seq_scan, seq_read, idx_scan, idx_fetch, mods in results:
                    seq_scan = seq_scan or 0
                    idx_scan = idx_scan or 0
                    print(f"   {table}: {seq_scan} seq scans, {idx_scan} index scans, {mods} modificações")
            else:
                print("[!] Estatísticas não disponíveis.")
                
        elif prompt_id == '09':  # PERF-002: Recomendação de Índices
            print(">> Analisando necessidade de índices...\n")
            cursor.execute("""
                SELECT 
                    schemaname,
                    relname as tablename,
                    seq_scan,
                    idx_scan,
                    CASE 
                        WHEN idx_scan = 0 AND seq_scan > 100 THEN 'CRÍTICO - Precisa de índice'
                        WHEN idx_scan < seq_scan AND seq_scan > 10 THEN 'ATENÇÃO - Verificar índices'
                        ELSE 'OK'
                    END as recommendation
                FROM pg_stat_user_tables
                WHERE seq_scan > 0
                ORDER BY seq_scan DESC;
            """)
            results = cursor.fetchall()
            if results:
                print(">> RECOMENDAÇÕES DE ÍNDICES:")
                print("-" * 60)
                critical = 0
                for schema, table, seq_scan, idx_scan, rec in results:
                    if 'CRÍTICO' in rec:
                        print(f"[CRÍTICO] {table}: {rec} ({seq_scan} seq scans)")
                        critical += 1
                    elif 'ATENÇÃO' in rec:
                        print(f"[ATENÇÃO] {table}: {rec} ({seq_scan} seq scans)")
                    else:
                        print(f"� {table}: {rec}")
                print(f"\n>> RESUMO: {critical} tabelas precisam de atenção imediata")
            else:
                print("[!] Estatísticas não disponíveis.")
                
        else:
            print(f"[!] Prompt {prompt_id} não reconhecido.")
            print(">> Disponíveis: 01-10")
            print(">> Use 'mcp prompts' para ver a lista completa")
            
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"[!] Erro de banco de dados: {e}")
        print(">> Possíveis causas:")
        print("   • PostgreSQL não está rodando")
        print("   • Credenciais incorretas")
        print("   • Banco de dados 'petclinic' não existe")
        print("   • Tabelas não foram criadas")
    except Exception as e:
        print(f"[!] Erro geral: {e}")
        print(">> Verifique se o PostgreSQL está rodando e acessível.")

def execute_all_prompts_sequence():
    """Executa todos os prompts na sequência recomendada"""
    print_header("EXECUTANDO SEQUÊNCIA COMPLETA DE ANÁLISE")
    print(">> Iniciando análise completa do banco de dados...\n")
    
    sequence = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']  # Todos implementados
    
    for i, prompt_id in enumerate(sequence, 1):
        print(f"\n{'='*60}")
        print(f"📍 ETAPA {i}/{len(sequence)}: Executando prompt {prompt_id}")
        print(f"{'='*60}")
        
        try:
            execute_prompt(prompt_id)
            print(f"\n>> Prompt {prompt_id} concluído com sucesso!")
            
            if i < len(sequence):
                input("\n>> Pressione ENTER para continuar para a próxima etapa...")
                
        except Exception as e:
            print(f"\n[!] Erro no prompt {prompt_id}: {e}")
            choice = input("\n>> Continuar mesmo assim? (s/N): ").strip().lower()
            if choice != 's':
                print("🛑 Sequência interrompida pelo usuário.")
                break
    
    print(f"\n{'='*60}")
    print("🎉 ANÁLISE COMPLETA FINALIZADA!")
    print(f"{'='*60}")
    print(">> Resumo: Análise estrutural e de negócio concluída.")
    print(">> Para análises de performance, execute os prompts 08-09 individualmente.")

def show_mcp_app():
    """Mostra informações da aplicação"""
    print_header("INFORMACOES DO SISTEMA")
    
    print(f">> Aplicação: PostgreSQL Performance Analyzer")
    print(f">> Versão: 1.0.0")
    print(f"🏢 Compass UOL - Vagrant Edition")
    print(f">> Ambiente: Ubuntu 22.04 LTS")
    print()
    print("🔗 CONEXÕES:")
    print(f"  >> MCP API: {MCP_URL}")
    print(f"  🐘 PostgreSQL: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"  >> Database: {DB_CONFIG['dbname']}")
    print()
    print(">> ACESSO EXTERNO:")
    print(f"  >> MCP API: http://localhost:8000")
    print(f"  🐘 PostgreSQL: localhost:5432")
    print()

def clear_screen():
    """Limpa a tela"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_help():
    """Exibe ajuda completa do sistema"""
    print_header("AJUDA COMPLETA - MCP DATABASE ANALYZER")
    
    print(f"{AmazonColors.ORANGE}COMANDOS PRINCIPAIS:{AmazonColors.RESET}")
    print("  mcp status   - Verificar status dos serviços")
    print("  mcp tables   - Listar tabelas do banco")
    print("  mcp prompts  - Menu de análises organizadas")
    print("  all          - Executar sequência completa de análise")
    print("  help         - Exibir esta ajuda")
    print("  quit         - Sair do sistema")
    print()
    
    print(f"{AmazonColors.BLUE}PROMPTS DE ANÁLISE (01-10):{AmazonColors.RESET}")
    print("  01 - EST-001: Estrutura Completa do Banco")
    print("  02 - EST-002: Inventário de Tabelas")
    print("  03 - EST-003: Contagem de Registros")
    print("  04 - NEG-001: Proprietários por Localização")
    print("  05 - NEG-002: Cadastro de Pets Completo")
    print("  06 - NEG-003: Equipe Veterinária")
    print("  07 - NEG-004: Análise de Visitas")
    print("  08 - PERF-001: Análise de Query")
    print("  09 - PERF-002: Recomendação de Índices")
    print("  10 - PERF-003: Configurações do Sistema")
    print()
    
    print(f"{AmazonColors.UOL_ORANGE}>> EXEMPLOS DE USO:{AmazonColors.RESET}")
    print("  compass❯ 01          # Executar análise de estrutura")
    print("  compass❯ all         # Executar todos os prompts")
    print("  compass❯ mcp tables  # Listar tabelas")
    print("  compass❯ mcp status  # Ver status dos serviços")
    print()
    
    print(f"{AmazonColors.GRAY}>> DICAS:{AmazonColors.RESET}")
    print("  • Execute '01' primeiro para verificar a estrutura")
    print("  • Use 'all' para análise completa automatizada")
    print("  • Pressione Ctrl+C para cancelar operações longas")
    print("  • Comandos são case-insensitive")
    print()

def test_database_connection():
    """Testa conexão com banco de dados"""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['dbname'],
            user=DB_CONFIG['username'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
        table_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return True, f"{table_count} tabelas disponíveis"
    except Exception as e:
        return False, f"Erro: {str(e)[:50]}..."

def main_loop():
    """Loop principal do prompt interativo"""
    clear_screen()
    
    # Se foi iniciado automaticamente, mostra boas-vindas especial
    if is_auto_started():
        print_welcome_auto_start()
    
    print_logo()
    
    # Verificar status inicial
    is_healthy, status = check_mcp_status()
    if is_healthy:
        print(f"    Status MCP: \033[32m{status}\033[0m")
    else:
        print(f"    Status MCP: \033[31m{status}\033[0m")
    
    # Verificar conexão com banco
    db_ok, db_status = test_database_connection()
    if db_ok:
        print(f"    Status DB: \033[32m{db_status}\033[0m")
    else:
        print(f"    Status DB: \033[31m{db_status}\033[0m")
    
    if not is_healthy and not db_ok:
        print("\n    [!] ATENÇÃO: Alguns serviços não estão acessíveis")
        print("    >> Mas você ainda pode usar os prompts de análise direta do banco!")
    
    print()
    print("    \033[93m>> COMANDOS PRINCIPAIS:\033[0m")
    print("    \033[36mmcp status\033[0m   - Status do sistema     │  \033[36mmcp actions\033[0m - Menu principal")
    print("    \033[36mmcp list\033[0m     - Listar bancos         │  \033[36mmcp tables\033[0m  - Listar tabelas")
    print("    \033[36mmcp prompts\033[0m  - Análises organizadas   │  \033[36m01-10\033[0m       - Executar prompt")
    print("    \033[36mall\033[0m          - Sequência completa     │  \033[36mmcp quit\033[0m    - Sair")
    print()
    
    # Se foi auto-iniciado, mostrar dica de acesso rápido
    if is_auto_started():
        print("    \033[94m>> GUIA RÁPIDO:\033[0m")
        print("    \033[95mINÍCIO RÁPIDO: Digite 'mcp prompts' para ver análises organizadas\033[0m")
        print("    \033[95mSEQUÊNCIA: Digite 'all' para executar análise completa\033[0m") 
        print("    \033[95mDIRETO: Digite '01' a '10' para executar prompt específico\033[0m")
        print()
    
    while True:
        try:
            command = input(f"{AmazonColors.ORANGE}compass❯ {AmazonColors.RESET}").strip().lower()
            
            if not command:
                continue
            
            # Comandos de saída
            if command in ['quit', 'exit', 'q', 'mcp quit']:
                print("\n>> Encerrando MCP Agent. Até logo!")
                break
            
            # Comandos MCP essenciais
            elif command in ['mcp clear', 'clear']:
                clear_screen()
                print_logo()
            
            elif command in ['mcp status', 'status']:
                is_healthy, status = check_mcp_status()
                print(f"\n>> Status MCP: {status}")
                if is_healthy:
                    print(f">> Endpoint: {MCP_URL}")
                    print(">> Estado: Operacional\n")
                else:
                    print("[!] Estado: Indisponível\n")
            
            elif command in ['mcp list', 'list']:
                list_databases()
            
            elif command in ['mcp tables', 'tables']:
                list_tables()
            
            elif command in ['mcp actions', 'actions']:
                show_db_actions()
            
            elif command in ['mcp prompts', 'prompts']:
                show_prompts_menu()
            
            elif command in ['mcp app', 'app']:
                show_mcp_app()
            
            elif command in ['help', 'mcp help', '?']:
                print_help()
            
            # Comandos diretos por número (suporta 01-10)
            elif command.isdigit():
                num = int(command)
                if 1 <= num <= 10:
                    # Normalizar para formato 01, 02, etc.
                    normalized_id = f"{num:02d}"
                    execute_prompt(normalized_id)
                    print()
                else:
                    print(f"[!] Número inválido: {command}. Use 01-10 para análises.")
            
            # Comandos com formato 01, 02, etc.
            elif command in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']:
                execute_prompt(command)
                print()
            
            # Comando para executar todos os prompts
            elif command == 'all':
                execute_all_prompts_sequence()
                print()
            
            # Comandos diretos por nome de banco
            elif command in ['petclinic', 'postgres']:
                list_tables(command)
                print()
            
            else:
                print(f"[!] Comando desconhecido: '{command}'")
                print(">> Comandos disponíveis:")
                print("   • 'mcp prompts' - Ver análises organizadas")
                print("   • '01' a '10' - Executar prompt específico")
                print("   • 'all' - Executar sequência completa")
                print("   • 'mcp actions' - Menu completo\n")
                
        except KeyboardInterrupt:
            print("\n\nUse 'quit' para sair\n")
        except EOFError:
            print("\n\nEncerrando...")
            break
        except Exception as e:
            print(f"Erro: {e}\n")

if __name__ == "__main__":
    main_loop()