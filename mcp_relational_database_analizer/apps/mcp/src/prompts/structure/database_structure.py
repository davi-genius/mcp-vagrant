"""
Prompts para análise de estrutura do banco de dados
"""

STRUCTURE_PROMPTS = {
    "01_complete_structure": {
        "name": "🏗️ EST-001: Estrutura Completa do Banco",
        "description": "Análise detalhada de todas as tabelas, índices e relacionamentos",
        "category": "Estrutura",
        "priority": "Alta",
        "tool": "analyze_database_structure",
        "query": None,
        "example_result": "Relatório completo com recomendações de otimização",
        "execution_order": 1
    },
    
    "02_table_inventory": {
        "name": "📋 EST-002: Inventário de Tabelas",
        "description": "Lista todas as tabelas com informações básicas e contagem de colunas",
        "category": "Estrutura",
        "priority": "Alta",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                table_name,
                table_type,
                (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name AND table_schema = 'public') as column_count,
                (SELECT pg_size_pretty(pg_total_relation_size(quote_ident(table_name)::regclass)) 
                 FROM information_schema.tables t2 
                 WHERE t2.table_name = t.table_name AND t2.table_schema = 'public') as table_size
            FROM information_schema.tables t
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """,
        "example_result": "Lista com nomes, tipos, colunas e tamanho das tabelas",
        "execution_order": 2
    },
    
    "03_record_count": {
        "name": "📊 EST-003: Contagem de Registros",
        "description": "Conta registros em todas as tabelas para análise de volume",
        "category": "Estrutura",
        "priority": "Alta",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                schemaname,
                tablename,
                n_tup_ins as total_inserts,
                n_tup_upd as total_updates,
                n_tup_del as total_deletes,
                n_live_tup as live_tuples,
                n_dead_tup as dead_tuples
            FROM pg_stat_user_tables
            ORDER BY n_live_tup DESC;
        """,
        "example_result": "Estatísticas detalhadas de registros por tabela",
        "execution_order": 3
    },

    "04_indexes_analysis": {
        "name": "🔍 EST-004: Análise de Índices",
        "description": "Lista todos os índices existentes com estatísticas de uso",
        "category": "Estrutura",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                schemaname,
                tablename,
                indexname,
                indexdef,
                idx_tup_read,
                idx_tup_fetch
            FROM pg_stat_user_indexes
            JOIN pg_indexes ON pg_stat_user_indexes.indexname = pg_indexes.indexname
            ORDER BY idx_tup_read DESC;
        """,
        "example_result": "Lista de índices com estatísticas de uso",
        "execution_order": 4
    },

    "05_foreign_keys": {
        "name": "🔗 EST-005: Chaves Estrangeiras",
        "description": "Mapeia todos os relacionamentos entre tabelas",
        "category": "Estrutura",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                tc.table_name as source_table,
                kcu.column_name as source_column,
                ccu.table_name as target_table,
                ccu.column_name as target_column,
                tc.constraint_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu 
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            ORDER BY tc.table_name, kcu.column_name;
        """,
        "example_result": "Mapeamento completo de relacionamentos",
        "execution_order": 5
    }
}