"""
Prompts para análise de dados de proprietários
"""

OWNERS_PROMPTS = {
    "01_owners_by_location": {
        "name": "👥 NEG-001: Proprietários por Localização",
        "description": "Análise geográfica dos proprietários de pets",
        "category": "Negócio",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                city,
                COUNT(*) as total_owners,
                COUNT(DISTINCT last_name) as unique_surnames,
                COUNT(DISTINCT telephone) as unique_phones,
                ROUND(AVG(LENGTH(first_name || ' ' || last_name)), 2) as avg_name_length
            FROM owners 
            GROUP BY city 
            ORDER BY total_owners DESC;
        """,
        "example_result": "Distribuição geográfica com estatísticas detalhadas",
        "execution_order": 6
    },

    "02_owners_demographics": {
        "name": "📊 NEG-002: Demografia de Proprietários",
        "description": "Análise demográfica detalhada dos proprietários",
        "category": "Negócio",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                city,
                COUNT(*) as total_owners,
                COUNT(CASE WHEN LENGTH(telephone) = 10 THEN 1 END) as valid_phones,
                COUNT(CASE WHEN address LIKE '%St.%' THEN 1 END) as street_addresses,
                COUNT(CASE WHEN address LIKE '%Ave.%' THEN 1 END) as avenue_addresses,
                ROUND(AVG(LENGTH(address)), 2) as avg_address_length
            FROM owners 
            GROUP BY city 
            ORDER BY total_owners DESC;
        """,
        "example_result": "Análise demográfica com padrões de endereço",
        "execution_order": 7
    },

    "03_owners_contact_analysis": {
        "name": "📞 NEG-003: Análise de Contatos",
        "description": "Validação e análise dos dados de contato",
        "category": "Negócio",
        "priority": "Baixa",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                CASE 
                    WHEN LENGTH(telephone) = 10 THEN 'Válido'
                    WHEN LENGTH(telephone) < 10 THEN 'Muito Curto'
                    ELSE 'Muito Longo'
                END as phone_status,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM owners), 2) as percentage
            FROM owners 
            GROUP BY 
                CASE 
                    WHEN LENGTH(telephone) = 10 THEN 'Válido'
                    WHEN LENGTH(telephone) < 10 THEN 'Muito Curto'
                    ELSE 'Muito Longo'
                END
            ORDER BY count DESC;
        """,
        "example_result": "Estatísticas de qualidade dos dados de contato",
        "execution_order": 8
    }
}