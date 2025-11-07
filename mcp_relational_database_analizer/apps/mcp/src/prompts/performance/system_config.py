"""
Prompts para análise de configuração do sistema
"""

SYSTEM_CONFIG_PROMPTS = {
    "01_postgresql_settings": {
        "name": "⚙️ PERF-008: Configurações do Sistema",
        "description": "Configurações críticas do PostgreSQL",
        "category": "Performance",
        "priority": "Média",
        "tool": "show_postgresql_settings",
        "pattern": "max_connections|shared_buffers|work_mem|maintenance_work_mem|effective_cache_size",
        "example_result": "Configurações de memória e conexões",
        "execution_order": 26
    },

    "02_memory_usage": {
        "name": "💾 PERF-009: Uso de Memória",
        "description": "Análise do uso de memória do PostgreSQL",
        "category": "Performance",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                name,
                setting,
                unit,
                context,
                short_desc
            FROM pg_settings 
            WHERE name IN (
                'shared_buffers',
                'work_mem',
                'maintenance_work_mem',
                'effective_cache_size',
                'wal_buffers'
            )
            ORDER BY name;
        """,
        "example_result": "Configurações de memória detalhadas",
        "execution_order": 27
    },

    "03_connection_stats": {
        "name": "🔌 PERF-010: Estatísticas de Conexão",
        "description": "Análise das conexões ativas e configurações",
        "category": "Performance",
        "priority": "Baixa",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                state,
                COUNT(*) as connection_count,
                MAX(now() - state_change) as max_duration
            FROM pg_stat_activity 
            WHERE pid <> pg_backend_pid()
            GROUP BY state
            ORDER BY connection_count DESC;
        """,
        "example_result": "Estatísticas de conexões por estado",
        "execution_order": 28
    },

    "04_database_size": {
        "name": "📏 PERF-011: Tamanho do Banco",
        "description": "Análise do tamanho do banco e objetos",
        "category": "Performance",
        "priority": "Baixa",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                'Database' as object_type,
                current_database() as object_name,
                pg_size_pretty(pg_database_size(current_database())) as size
            UNION ALL
            SELECT 
                'Table' as object_type,
                tablename as object_name,
                pg_size_pretty(pg_total_relation_size(quote_ident(tablename)::regclass)) as size
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY 
                CASE object_type 
                    WHEN 'Database' THEN 1 
                    ELSE 2 
                END,
                pg_total_relation_size(
                    CASE 
                        WHEN object_type = 'Database' THEN current_database()::regclass
                        ELSE quote_ident(object_name)::regclass
                    END
                ) DESC;
        """,
        "example_result": "Tamanhos do banco e tabelas ordenados",
        "execution_order": 29
    }
}