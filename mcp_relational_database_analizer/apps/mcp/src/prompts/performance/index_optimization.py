"""
Prompts para otimização de índices
"""

INDEX_OPTIMIZATION_PROMPTS = {
    "01_index_recommendations": {
        "name": "💡 PERF-004: Recomendação de Índices",
        "description": "Sugere índices para otimização de performance",
        "category": "Performance",
        "priority": "Alta",
        "tool": "recommend_indexes",
        "query": "SELECT * FROM owners WHERE city = 'Madison' AND last_name LIKE 'D%'",
        "example_result": "Sugestões específicas de índices",
        "note": "Personalize a query para análise específica",
        "execution_order": 22
    },

    "02_unused_indexes": {
        "name": "🗑️ PERF-005: Índices Não Utilizados",
        "description": "Identifica índices que podem ser removidos",
        "category": "Performance",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                schemaname,
                tablename,
                indexname,
                idx_tup_read,
                idx_tup_fetch,
                pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
            FROM pg_stat_user_indexes
            WHERE idx_tup_read = 0 AND idx_tup_fetch = 0
            ORDER BY pg_relation_size(indexname::regclass) DESC;
        """,
        "example_result": "Lista de índices não utilizados com tamanho",
        "execution_order": 23
    },

    "03_index_efficiency": {
        "name": "⚡ PERF-006: Eficiência dos Índices",
        "description": "Analisa a eficiência dos índices existentes",
        "category": "Performance",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                schemaname,
                tablename,
                indexname,
                idx_tup_read,
                idx_tup_fetch,
                CASE 
                    WHEN idx_tup_read = 0 THEN 0
                    ELSE ROUND((idx_tup_fetch::numeric / idx_tup_read) * 100, 2)
                END as efficiency_percent,
                pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
            FROM pg_stat_user_indexes
            WHERE idx_tup_read > 0
            ORDER BY efficiency_percent DESC;
        """,
        "example_result": "Análise de eficiência dos índices com percentuais",
        "execution_order": 24
    },

    "04_duplicate_indexes": {
        "name": "🔄 PERF-007: Índices Duplicados",
        "description": "Identifica possíveis índices duplicados ou redundantes",
        "category": "Performance",
        "priority": "Baixa",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                t.tablename,
                array_agg(t.indexname) as similar_indexes,
                t.column_names
            FROM (
                SELECT 
                    schemaname,
                    tablename,
                    indexname,
                    string_agg(attname, ',' ORDER BY attnum) as column_names
                FROM pg_index i
                JOIN pg_class c ON c.oid = i.indexrelid
                JOIN pg_namespace n ON n.oid = c.relnamespace
                JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
                WHERE n.nspname = 'public'
                GROUP BY schemaname, tablename, indexname
            ) t
            GROUP BY t.tablename, t.column_names
            HAVING COUNT(*) > 1
            ORDER BY t.tablename;
        """,
        "example_result": "Grupos de índices com colunas similares",
        "execution_order": 25
    }
}