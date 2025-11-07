"""
Prompts para análise de dados de visitas
"""

VISITS_PROMPTS = {
    "01_visits_analysis": {
        "name": "📈 NEG-010: Análise de Visitas",
        "description": "Estatísticas detalhadas de visitas veterinárias",
        "category": "Negócio",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                DATE_TRUNC('month', v.visit_date) as visit_month,
                COUNT(*) as total_visits,
                COUNT(DISTINCT v.pet_id) as unique_pets,
                COUNT(DISTINCT p.owner_id) as unique_owners,
                AVG(LENGTH(v.description)) as avg_description_length
            FROM visits v
            JOIN pets p ON v.pet_id = p.id
            GROUP BY DATE_TRUNC('month', v.visit_date)
            ORDER BY visit_month DESC;
        """,
        "example_result": "Tendências mensais de visitas com métricas",
        "execution_order": 15
    },

    "02_visit_types": {
        "name": "🏥 NEG-011: Tipos de Visitas",
        "description": "Categorização das visitas por tipo de procedimento",
        "category": "Negócio",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                CASE 
                    WHEN LOWER(description) LIKE '%shot%' OR LOWER(description) LIKE '%vaccination%' THEN 'Vacinação'
                    WHEN LOWER(description) LIKE '%spayed%' OR LOWER(description) LIKE '%neutered%' THEN 'Cirurgia Reprodutiva'
                    WHEN LOWER(description) LIKE '%checkup%' OR LOWER(description) LIKE '%exam%' THEN 'Exame de Rotina'
                    WHEN LOWER(description) LIKE '%dental%' OR LOWER(description) LIKE '%teeth%' THEN 'Cuidados Dentários'
                    WHEN LOWER(description) LIKE '%treatment%' OR LOWER(description) LIKE '%infection%' THEN 'Tratamento Médico'
                    ELSE 'Outros'
                END as visit_category,
                COUNT(*) as visit_count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM visits), 2) as percentage,
                AVG(LENGTH(description)) as avg_description_length
            FROM visits
            GROUP BY 
                CASE 
                    WHEN LOWER(description) LIKE '%shot%' OR LOWER(description) LIKE '%vaccination%' THEN 'Vacinação'
                    WHEN LOWER(description) LIKE '%spayed%' OR LOWER(description) LIKE '%neutered%' THEN 'Cirurgia Reprodutiva'
                    WHEN LOWER(description) LIKE '%checkup%' OR LOWER(description) LIKE '%exam%' THEN 'Exame de Rotina'
                    WHEN LOWER(description) LIKE '%dental%' OR LOWER(description) LIKE '%teeth%' THEN 'Cuidados Dentários'
                    WHEN LOWER(description) LIKE '%treatment%' OR LOWER(description) LIKE '%infection%' THEN 'Tratamento Médico'
                    ELSE 'Outros'
                END
            ORDER BY visit_count DESC;
        """,
        "example_result": "Distribuição de visitas por categoria de procedimento",
        "execution_order": 16
    },

    "03_visit_frequency": {
        "name": "📊 NEG-012: Frequência de Visitas por Pet",
        "description": "Análise da frequência de visitas por pet",
        "category": "Negócio",
        "priority": "Baixa",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                CASE 
                    WHEN visit_count = 0 THEN 'Sem visitas'
                    WHEN visit_count = 1 THEN '1 visita'
                    WHEN visit_count BETWEEN 2 AND 3 THEN '2-3 visitas'
                    WHEN visit_count BETWEEN 4 AND 5 THEN '4-5 visitas'
                    ELSE '6+ visitas'
                END as frequency_category,
                COUNT(*) as pet_count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM pets), 2) as percentage
            FROM (
                SELECT 
                    p.id,
                    p.name,
                    COUNT(v.id) as visit_count
                FROM pets p
                LEFT JOIN visits v ON p.id = v.pet_id
                GROUP BY p.id, p.name
            ) pet_visits
            GROUP BY 
                CASE 
                    WHEN visit_count = 0 THEN 'Sem visitas'
                    WHEN visit_count = 1 THEN '1 visita'
                    WHEN visit_count BETWEEN 2 AND 3 THEN '2-3 visitas'
                    WHEN visit_count BETWEEN 4 AND 5 THEN '4-5 visitas'
                    ELSE '6+ visitas'
                END
            ORDER BY 
                CASE 
                    WHEN visit_count = 0 THEN 1
                    WHEN visit_count = 1 THEN 2
                    WHEN visit_count BETWEEN 2 AND 3 THEN 3
                    WHEN visit_count BETWEEN 4 AND 5 THEN 4
                    ELSE 5
                END;
        """,
        "example_result": "Distribuição de pets por frequência de visitas",
        "execution_order": 17
    },

    "04_recent_visits": {
        "name": "🕒 NEG-013: Visitas Recentes",
        "description": "Análise das visitas mais recentes",
        "category": "Negócio",
        "priority": "Baixa",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                v.visit_date,
                p.name as pet_name,
                t.name as pet_type,
                o.first_name || ' ' || o.last_name as owner_name,
                o.city,
                v.description,
                EXTRACT(DAY FROM (CURRENT_DATE - v.visit_date)) as days_ago
            FROM visits v
            JOIN pets p ON v.pet_id = p.id
            JOIN types t ON p.type_id = t.id
            JOIN owners o ON p.owner_id = o.id
            WHERE v.visit_date >= CURRENT_DATE - INTERVAL '90 days'
            ORDER BY v.visit_date DESC
            LIMIT 20;
        """,
        "example_result": "Lista das 20 visitas mais recentes (últimos 90 dias)",
        "execution_order": 18
    }
}