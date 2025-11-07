"""
Modelos de prompts organizados para PostgreSQL Performance Analyzer
Organizados por categoria e ordem de execução lógica
"""

# Prompts organizados por categoria e ordem de execução
MODELS = {
    # === CATEGORIA 1: ESTRUTURA E INVENTÁRIO (01-03) ===
    "01": {
        "name": "🏗️ EST-001: Estrutura Completa do Banco",
        "description": "Análise detalhada de todas as tabelas, índices e relacionamentos",
        "category": "Estrutura",
        "priority": "Alta",
        "tool": "analyze_database_structure",
        "query": None,
        "example_result": "Relatório completo com recomendações de otimização",
        "execution_order": 1
    },
    
    "02": {
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
    
    "03": {
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
    
    # === CATEGORIA 2: DADOS DE NEGÓCIO (04-07) ===
    "04": {
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
        "execution_order": 4
    },
    
    "05": {
        "name": "🐕 NEG-002: Cadastro de Pets Completo",
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
        "execution_order": 5
    },
    
    "06": {
        "name": "🏥 NEG-003: Equipe Veterinária",
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
        "execution_order": 6
    },
    
    "07": {
        "name": "📈 NEG-004: Análise de Visitas",
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
        "execution_order": 7
    },
    
    # === CATEGORIA 3: PERFORMANCE E OTIMIZAÇÃO (08-10) ===
    "08": {
        "name": "🔍 PERF-001: Análise de Query",
        "description": "Analisa plano de execução de query específica",
        "category": "Performance",
        "priority": "Alta",
        "tool": "analyze_query",
        "query": "SELECT o.*, p.name as pet_name FROM owners o JOIN pets p ON o.id = p.owner_id WHERE o.city = 'Madison'",
        "example_result": "Plano de execução detalhado com recomendações",
        "note": "Modifique a query conforme necessário",
        "execution_order": 8
    },
    
    "09": {
        "name": "💡 PERF-002: Recomendação de Índices",
        "description": "Sugere índices para otimização de performance",
        "category": "Performance",
        "priority": "Alta",
        "tool": "recommend_indexes",
        "query": "SELECT * FROM owners WHERE city = 'Madison' AND last_name LIKE 'D%'",
        "example_result": "Sugestões específicas de índices",
        "note": "Personalize a query para análise específica",
        "execution_order": 9
    },
    
    "10": {
        "name": "⚙️ PERF-003: Configurações do Sistema",
        "description": "Configurações críticas do PostgreSQL",
        "category": "Performance",
        "priority": "Média",
        "tool": "show_postgresql_settings",
        "pattern": "max_connections|shared_buffers|work_mem|maintenance_work_mem|effective_cache_size",
        "example_result": "Configurações de memória e conexões",
        "execution_order": 10
    }
}

def get_model_list():
    """Retorna lista formatada e organizada dos modelos disponíveis"""
    result = "\n🚀 PROMPTS ORGANIZADOS - PostgreSQL Performance Analyzer\n"
    result += "=" * 70 + "\n\n"
    
    # Organizar por categoria
    categories = {}
    for key, model in MODELS.items():
        category = model.get('category', 'Outros')
        if category not in categories:
            categories[category] = []
        categories[category].append((key, model))
    
    # Ordenar por ordem de execução dentro de cada categoria
    for category in categories:
        categories[category].sort(key=lambda x: x[1].get('execution_order', 999))
    
    # Exibir por categoria
    category_icons = {
        'Estrutura': '🏗️',
        'Negócio': '💼', 
        'Performance': '⚡'
    }
    
    for category, models in categories.items():
        icon = category_icons.get(category, '📁')
        result += f"{icon} === CATEGORIA: {category.upper()} ===\n\n"
        
        for key, model in models:
            priority_icon = "🔴" if model.get('priority') == 'Alta' else "🟡" if model.get('priority') == 'Média' else "🟢"
            result += f"{key:2}. {model['name']} {priority_icon}\n"
            result += f"    📝 {model['description']}\n"
            result += f"    🎯 Prioridade: {model.get('priority', 'Baixa')}\n"
            if model.get('note'):
                result += f"    💡 {model['note']}\n"
            result += "\n"
        result += "\n"
    
    result += "📋 ORDEM DE EXECUÇÃO RECOMENDADA:\n"
    result += "   1️⃣ Estrutura (01-03): Entenda o banco primeiro\n"
    result += "   2️⃣ Negócio (04-07): Analise os dados\n"
    result += "   3️⃣ Performance (08-10): Otimize conforme necessário\n\n"
    
    result += "💻 COMO USAR:\n"
    result += "   - Digite o número (01-10) do prompt desejado\n"
    result += "   - Use ordem sequencial para análise completa\n"
    result += "   - Prompts de alta prioridade são essenciais\n\n"
    
    return result

def get_model_by_id(model_id):
    """Retorna modelo específico por ID (suporta formato 01, 1, etc.)"""
    # Normalizar ID para formato com zero à esquerda
    if model_id.isdigit():
        normalized_id = f"{int(model_id):02d}"
        return MODELS.get(normalized_id) or MODELS.get(str(model_id))
    return MODELS.get(str(model_id))

def get_model_curl_command(model_id, host="localhost", port=5432, dbname="petclinic", username="petclinic", password="petclinic"):
    """Gera comando curl para executar o modelo com informações organizadas"""
    model = get_model_by_id(model_id)
    if not model:
        return None
    
    base_params = {
        "host": host,
        "port": port, 
        "dbname": dbname,
        "username": username,
        "password": password
    }
    
    if model["tool"] == "execute_read_only_query":
        params = {**base_params, "query": model["query"].strip()}
    elif model["tool"] == "analyze_database_structure":
        params = base_params
    elif model["tool"] == "analyze_query":
        params = {**base_params, "query": model["query"]}
    elif model["tool"] == "recommend_indexes":
        params = {**base_params, "query": model["query"]}
    elif model["tool"] == "show_postgresql_settings":
        params = {**base_params, "pattern": model.get("pattern", "")}
    else:
        params = base_params
    
    return {
        "tool": model["tool"],
        "params": params,
        "description": model["description"],
        "category": model.get("category", "Outros"),
        "priority": model.get("priority", "Baixa"),
        "execution_order": model.get("execution_order", 999)
    }

def get_models_by_category():
    """Retorna modelos organizados por categoria"""
    categories = {}
    for key, model in MODELS.items():
        category = model.get('category', 'Outros')
        if category not in categories:
            categories[category] = []
        categories[category].append((key, model))
    
    # Ordenar por ordem de execução
    for category in categories:
        categories[category].sort(key=lambda x: x[1].get('execution_order', 999))
    
    return categories

def get_execution_sequence():
    """Retorna sequência recomendada de execução"""
    sequence = []
    for key, model in sorted(MODELS.items(), key=lambda x: x[1].get('execution_order', 999)):
        sequence.append({
            'id': key,
            'name': model['name'],
            'category': model.get('category', 'Outros'),
            'priority': model.get('priority', 'Baixa'),
            'order': model.get('execution_order', 999)
        })
    return sequence