"""
Compatibilidade com o sistema antigo - redireciona para a nova estrutura organizada
"""

# Importar da nova estrutura organizada
from . import ALL_PROMPTS, get_model_list, get_prompt_by_id, get_prompts_by_category

# Manter compatibilidade com código existente
MODELS = ALL_PROMPTS

def get_model_by_id(model_id):
    """Retorna modelo específico por ID (suporta formato 01, 1, etc.)"""
    # Normalizar ID para formato com zero à esquerda
    if model_id.isdigit():
        normalized_id = f"{int(model_id):02d}"
        return ALL_PROMPTS.get(normalized_id)
    return ALL_PROMPTS.get(model_id)

def get_model_curl_command(model_id):
    """Retorna comando curl para execução do modelo específico."""
    model = get_model_by_id(model_id)
    if not model:
        return None
    
    return f"""curl -X POST http://localhost:8000/execute \\
  -H "Content-Type: application/json" \\
  -d '{{"prompt_id": "{model_id}"}}'"""

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