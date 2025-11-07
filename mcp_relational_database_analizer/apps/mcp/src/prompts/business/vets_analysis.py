"""
Prompts para análise de dados de veterinários
"""

VETS_PROMPTS = {
    "01_veterinary_team": {
        "name": "🏥 NEG-007: Equipe Veterinária",
        "description": "Veterinários com especialidades e estatísticas",
        "category": "Negócio",
        "priority": "Média",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                v.first_name || ' ' || v.last_name as vet_name,
                STRING_AGG(s.name, ', ') as specialties,
                COUNT(DISTINCT s.id) as specialty_count,
                COUNT(DISTINCT vs2.vet_id) as total_vets_with_same_specialties
            FROM vets v
            LEFT JOIN vet_specialties vs ON v.id = vs.vet_id
            LEFT JOIN specialties s ON vs.specialty_id = s.id
            LEFT JOIN vet_specialties vs2 ON s.id = vs2.specialty_id
            GROUP BY v.id, v.first_name, v.last_name
            ORDER BY specialty_count DESC, v.last_name;
        """,
        "example_result": "Lista de veterinários com análise de especialidades",
        "execution_order": 12
    },

    "02_specialties_distribution": {
        "name": "🎯 NEG-008: Distribuição de Especialidades",
        "description": "Análise da distribuição de especialidades veterinárias",
        "category": "Negócio",
        "priority": "Baixa",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                s.name as specialty,
                COUNT(vs.vet_id) as vet_count,
                ROUND(COUNT(vs.vet_id) * 100.0 / (SELECT COUNT(*) FROM vets), 2) as coverage_percentage,
                STRING_AGG(v.first_name || ' ' || v.last_name, ', ') as veterinarians
            FROM specialties s
            LEFT JOIN vet_specialties vs ON s.id = vs.specialty_id
            LEFT JOIN vets v ON vs.vet_id = v.id
            GROUP BY s.id, s.name
            ORDER BY vet_count DESC;
        """,
        "example_result": "Distribuição de especialidades com cobertura",
        "execution_order": 13
    },

    "03_vet_workload": {
        "name": "⚖️ NEG-009: Carga de Trabalho dos Veterinários",
        "description": "Análise hipotética da distribuição de trabalho",
        "category": "Negócio",
        "priority": "Baixa",
        "tool": "execute_read_only_query",
        "query": """
            SELECT 
                v.first_name || ' ' || v.last_name as vet_name,
                COUNT(DISTINCT s.id) as specialties_count,
                CASE 
                    WHEN COUNT(DISTINCT s.id) = 0 THEN 'Generalista'
                    WHEN COUNT(DISTINCT s.id) = 1 THEN 'Especialista'
                    ELSE 'Multi-especialista'
                END as vet_type,
                STRING_AGG(s.name, ', ') as specialties
            FROM vets v
            LEFT JOIN vet_specialties vs ON v.id = vs.vet_id
            LEFT JOIN specialties s ON vs.specialty_id = s.id
            GROUP BY v.id, v.first_name, v.last_name
            ORDER BY specialties_count DESC, v.last_name;
        """,
        "example_result": "Classificação dos veterinários por tipo de especialização",
        "execution_order": 14
    }
}