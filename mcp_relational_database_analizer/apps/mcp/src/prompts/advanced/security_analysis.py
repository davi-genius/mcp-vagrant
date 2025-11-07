"""
Prompts para análise de segurança do banco de dados
"""

SECURITY_PROMPTS = {
    "01_user_permissions": {
        "name": "🔐 SEC-001: Análise de Permissões",
        "description": "Analisa permissões de usuários e roles no banco",
        "category": "Segurança",
        "priority": "Alta",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                r.rolname as role_name,
                r.rolsuper as is_superuser,
                r.rolcreaterole as can_create_roles,
                r.rolcreatedb as can_create_db,
                r.rolcanlogin as can_login,
                r.rolconnlimit as connection_limit,
                r.rolvaliduntil as valid_until
            FROM pg_roles r
            WHERE r.rolname NOT LIKE 'pg_%'
            ORDER BY r.rolsuper DESC, r.rolname;
        """,
        "example_result": "Lista de usuários com análise de permissões",
        "execution_order": 30
    },

    "02_connection_security": {
        "name": "🌐 SEC-002: Segurança de Conexões",
        "description": "Analisa configurações de segurança de conexão",
        "category": "Segurança",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                name,
                setting,
                context,
                short_desc
            FROM pg_settings 
            WHERE name IN (
                'ssl',
                'ssl_cert_file',
                'ssl_key_file',
                'ssl_ca_file',
                'log_connections',
                'log_disconnections',
                'log_statement'
            )
            ORDER BY name;
        """,
        "example_result": "Configurações de segurança de conexão",
        "execution_order": 31
    },

    "03_audit_trail": {
        "name": "📋 SEC-003: Trilha de Auditoria",
        "description": "Analisa logs e atividades de auditoria",
        "category": "Segurança",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                datname as database,
                usename as username,
                application_name,
                client_addr,
                state,
                query_start,
                state_change,
                CASE 
                    WHEN state = 'active' THEN 'Ativo'
                    WHEN state = 'idle' THEN 'Inativo'
                    WHEN state = 'idle in transaction' THEN 'Em Transação'
                    ELSE state
                END as status_pt
            FROM pg_stat_activity
            WHERE pid <> pg_backend_pid()
            ORDER BY query_start DESC;
        """,
        "example_result": "Atividades atuais com informações de auditoria",
        "execution_order": 32
    }
}