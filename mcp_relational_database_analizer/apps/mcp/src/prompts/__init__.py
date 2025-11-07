"""
Módulo de prompts organizados para PostgreSQL Performance Analyzer
Importa todos os prompts de diferentes categorias
"""

from .structure.database_structure import STRUCTURE_PROMPTS
from .business.owners_analysis import OWNERS_PROMPTS
from .business.pets_analysis import PETS_PROMPTS
from .business.vets_analysis import VETS_PROMPTS
from .business.visits_analysis import VISITS_PROMPTS
from .performance.query_analysis import QUERY_PERFORMANCE_PROMPTS
from .performance.index_optimization import INDEX_OPTIMIZATION_PROMPTS
from .performance.system_config import SYSTEM_CONFIG_PROMPTS
from .advanced.security_analysis import SECURITY_PROMPTS
from .advanced.maintenance_analysis import MAINTENANCE_PROMPTS

# Combinar todos os prompts em um dicionário unificado
ALL_PROMPTS = {}
ALL_PROMPTS.update(STRUCTURE_PROMPTS)
ALL_PROMPTS.update(OWNERS_PROMPTS)
ALL_PROMPTS.update(PETS_PROMPTS)
ALL_PROMPTS.update(VETS_PROMPTS)
ALL_PROMPTS.update(VISITS_PROMPTS)
ALL_PROMPTS.update(QUERY_PERFORMANCE_PROMPTS)
ALL_PROMPTS.update(INDEX_OPTIMIZATION_PROMPTS)
ALL_PROMPTS.update(SYSTEM_CONFIG_PROMPTS)
ALL_PROMPTS.update(SECURITY_PROMPTS)
ALL_PROMPTS.update(MAINTENANCE_PROMPTS)

# Manter compatibilidade com o código existente
MODELS = ALL_PROMPTS

def get_model_list():
    """Retorna lista formatada e organizada dos modelos disponíveis"""
    result = "\n>> PROMPTS ORGANIZADOS - PostgreSQL Performance Analyzer\n"
    result += "=" * 70 + "\n\n"
    
    # Organizar por categoria
    categories = {}
    for key, model in ALL_PROMPTS.items():
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
        'Performance': '⚡',
        'Segurança': '🔐',
        'Manutenção': '🔧'
    }
    
    for category, models in categories.items():
        icon = category_icons.get(category, '📁')
        result += f"{icon} === CATEGORIA: {category.upper()} ===\n\n"
        
        for key, model in models:
            priority_icon = {
                'Alta': '🔴',
                'Média': '🟡',
                'Baixa': '🟢'
            }.get(model.get('priority', 'Média'), '⚪')
            
            result += f"  {priority_icon} {key}: {model['name']}\n"
            result += f"     📝 {model['description']}\n"
            result += f"     🔧 Tool: {model['tool']}\n"
            
            if model.get('note'):
                result += f"     💡 {model['note']}\n"
            
            result += f"     📊 Resultado: {model['example_result']}\n\n"
    
    result += "\n" + "=" * 70 + "\n"
    result += "💡 Para executar um prompt: use o ID (ex: '01_complete_structure')\n"
    result += "🎯 Prioridades: 🔴 Alta | 🟡 Média | 🟢 Baixa\n"
    result += "📋 Categorias: 🏗️ Estrutura | 💼 Negócio | ⚡ Performance | 🔐 Segurança | 🔧 Manutenção\n"
    
    return result

def get_prompt_by_id(prompt_id):
    """Retorna um prompt específico pelo ID"""
    return ALL_PROMPTS.get(prompt_id)

def get_prompts_by_category(category):
    """Retorna todos os prompts de uma categoria específica"""
    return {k: v for k, v in ALL_PROMPTS.items() if v.get('category') == category}

def get_prompts_by_priority(priority):
    """Retorna todos os prompts de uma prioridade específica"""
    return {k: v for k, v in ALL_PROMPTS.items() if v.get('priority') == priority}

def get_execution_order():
    """Retorna prompts ordenados por ordem de execução"""
    sorted_prompts = sorted(ALL_PROMPTS.items(), key=lambda x: x[1].get('execution_order', 999))
    return sorted_prompts