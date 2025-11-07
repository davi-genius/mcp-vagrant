"""
Prompts para análise de dados de pets
"""

PETS_PROMPTS = {
    "01_pets_complete": {
        "name": "🐕 NEG-004: Cadastro de Pets Completo",
        "description": "Lista completa de pets com dados dos proprietários",
        "category": "Negócio",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                p.name as pet_name,
                t.name as pet_type,
                p.birth_date,
                EXTRACT(YEAR FROM AGE(p.birth_date)) as age_years,
                o.first_name || ' ' || o.last_name as owner_name,
                o.city,
                o.telephone,
                COUNT(v.id) as total_visits
            FROM pets p
            JOIN types t ON p.type_id = t.id
            JOIN owners o ON p.owner_id = o.id
            LEFT JOIN visits v ON p.id = v.pet_id
            GROUP BY p.id, p.name, t.name, p.birth_date, o.first_name, o.last_name, o.city, o.telephone
            ORDER BY o.last_name, p.name;
        """,
        "example_result": "Cadastro completo com idade e histórico de visitas",
        "execution_order": 9
    },

    "02_pets_by_type": {
        "name": "🐾 NEG-005: Pets por Tipo",
        "description": "Distribuição de pets por tipo e estatísticas de idade",
        "category": "Negócio",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                t.name as pet_type,
                COUNT(p.id) as total_pets,
                ROUND(AVG(EXTRACT(YEAR FROM AGE(p.birth_date))), 2) as avg_age_years,
                MIN(p.birth_date) as oldest_birth,
                MAX(p.birth_date) as youngest_birth,
                COUNT(DISTINCT p.owner_id) as unique_owners
            FROM pets p
            JOIN types t ON p.type_id = t.id
            GROUP BY t.id, t.name
            ORDER BY total_pets DESC;
        """,
        "example_result": "Estatísticas detalhadas por tipo de pet",
        "execution_order": 10
    },

    "03_pets_age_analysis": {
        "name": "📅 NEG-006: Análise de Idade dos Pets",
        "description": "Distribuição etária dos pets com categorização",
        "category": "Negócio",
        "priority": "Baixa",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                CASE 
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) < 1 THEN 'Filhote (< 1 ano)'
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 1 AND 3 THEN 'Jovem (1-3 anos)'
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 4 AND 7 THEN 'Adulto (4-7 anos)'
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 8 AND 12 THEN 'Sênior (8-12 anos)'
                    ELSE 'Idoso (> 12 anos)'
                END as age_category,
                COUNT(*) as pet_count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM pets), 2) as percentage
            FROM pets
            GROUP BY 
                CASE 
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) < 1 THEN 'Filhote (< 1 ano)'
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 1 AND 3 THEN 'Jovem (1-3 anos)'
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 4 AND 7 THEN 'Adulto (4-7 anos)'
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 8 AND 12 THEN 'Sênior (8-12 anos)'
                    ELSE 'Idoso (> 12 anos)'
                END
            ORDER BY 
                CASE 
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) < 1 THEN 1
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 1 AND 3 THEN 2
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 4 AND 7 THEN 3
                    WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 8 AND 12 THEN 4
                    ELSE 5
                END;
        """,
        "example_result": "Distribuição etária categorizada dos pets",
        "execution_order": 11
    }
}