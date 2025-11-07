"""
Prompts para análise de manutenção do banco de dados
"""

MAINTENANCE_PROMPTS = {
    "01_vacuum_analysis": {
        "name": "MAINT-001: Análise de Vacuum",
        "description": "Analisa necessidade de vacuum e estatísticas",
        "category": "Manutenção",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                schemaname,
                tablename,
                last_vacuum,
                last_autovacuum,
                vacuum_count,
                autovacuum_count,
                n_dead_tup,
                n_live_tup,
                CASE 
                    WHEN n_live_tup > 0 THEN 
                        ROUND((n_dead_tup::numeric / n_live_tup) * 100, 2)
                    ELSE 0
                END as dead_tuple_percent
            FROM pg_stat_user_tables
            ORDER BY dead_tuple_percent DESC, n_dead_tup DESC;
        """,
        "example_result": "Estatísticas de vacuum com percentual de tuplas mortas",
        "execution_order": 33
    },

    "02_analyze_stats": {
        "name": "MAINT-002: Estatísticas de Analyze",
        "description": "Analisa estatísticas de analyze das tabelas",
        "category": "Manutenção",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                schemaname,
                tablename,
                last_analyze,
                last_autoanalyze,
                analyze_count,
                autoanalyze_count,
                n_mod_since_analyze,
                CASE 
                    WHEN last_analyze IS NULL AND last_autoanalyze IS NULL THEN 'Nunca analisada'
                    WHEN last_analyze > last_autoanalyze OR last_autoanalyze IS NULL THEN 'Analyze manual'
                    ELSE 'Auto-analyze'
                END as last_analyze_type
            FROM pg_stat_user_tables
            ORDER BY n_mod_since_analyze DESC;
        """,
        "example_result": "Estatísticas de analyze com modificações pendentes",
        "execution_order": 34
    },

    "03_bloat_analysis": {
        "name": "MAINT-003: Análise de Bloat",
        "description": "Estima bloat em tabelas e índices",
        "category": "Manutenção",
        "priority": "Baixa",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
                pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
                n_live_tup,
                n_dead_tup,
                CASE 
                    WHEN n_live_tup + n_dead_tup > 0 THEN
                        ROUND((n_dead_tup::numeric / (n_live_tup + n_dead_tup)) * 100, 2)
                    ELSE 0
                END as estimated_bloat_percent
            FROM pg_stat_user_tables
            WHERE n_live_tup + n_dead_tup > 0
            ORDER BY estimated_bloat_percent DESC;
        """,
        "example_result": "Estimativa de bloat por tabela",
        "execution_order": 35
    },

    "04_replication_lag": {
        "name": "MAINT-004: Lag de Replicação",
        "description": "Monitora lag de replicação (se aplicável)",
        "category": "Manutenção",
        "priority": "Baixa",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                client_addr,
                client_hostname,
                client_port,
                state,
                sent_lsn,
                write_lsn,
                flush_lsn,
                replay_lsn,
                write_lag,
                flush_lag,
                replay_lag,
                sync_state
            FROM pg_stat_replication
            ORDER BY client_addr;
        """,
        "example_result": "Status de replicação (vazio se não configurada)",
        "execution_order": 36,
        "note": "Retorna vazio se replicação não estiver configurada"
    }
}