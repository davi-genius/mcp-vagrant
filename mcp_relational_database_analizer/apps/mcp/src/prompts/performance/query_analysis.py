"""
Prompts para análise de performance de queries
"""

QUERY_PERFORMANCE_PROMPTS = {
    "01_query_analysis": {
        "name": "🔍 PERF-001: Análise de Query",
        "description": "Analisa plano de execução de query específica",
        "category": "Performance",
        "priority": "Alta",
        "tool": "analyze_query",
        "query": "SELECT o.*, p.name as pet_name FROM owners o JOIN pets p ON o.id = p.owner_id WHERE o.city = 'Madison'",
        "example_result": "Plano de execução detalhado com recomendações",
        "note": "Modifique a query conforme necessário",
        "execution_order": 19
    },

    "02_slow_queries": {
        "name": "🐌 PERF-002: Queries Lentas",
        "description": "Identifica queries com performance ruim",
        "category": "Performance",
        "priority": "Alta",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                query,
                calls,
                total_time,
                mean_time,
                rows,
                100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
            FROM pg_stat_statements 
            WHERE calls > 10
            ORDER BY mean_time DESC 
            LIMIT 10;
        """,
        "example_result": "Top 10 queries mais lentas",
        "execution_order": 20,
        "note": "Requer extensão pg_stat_statements habilitada"
    },

    "03_table_scans": {
        "name": "📊 PERF-003: Scans de Tabela",
        "description": "Identifica tabelas com muitos table scans",
        "category": "Performance",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                schemaname,
                tablename,
                seq_scan,
                seq_tup_read,
                idx_scan,
                idx_tup_fetch,
                CASE 
                    WHEN seq_scan = 0 THEN 0
                    ELSE ROUND(seq_tup_read::numeric / seq_scan, 2)
                END as avg_seq_tup_read
            FROM pg_stat_user_tables
            WHERE seq_scan > 0
            ORDER BY seq_scan DESC, seq_tup_read DESC;
        """,
        "example_result": "Tabelas com estatísticas de scans sequenciais",
        "execution_order": 21
    }
}