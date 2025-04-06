import json
import os

# Encontra o caminho absoluto para o arquivo JSON
# __file__ é o caminho deste arquivo (destination_service.py)
# os.path.dirname(__file__) é a pasta 'services'
# '..' volta uma pasta (para 'backend')
# os.path.join junta as partes para formar o caminho completo
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'destinations.json')

def load_destinations():
    """Carrega os destinos do arquivo JSON."""
    try:
        # Use 'utf-8' para garantir compatibilidade com acentos
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"AVISO: Arquivo de dados não encontrado em {DATA_FILE}")
        return [] # Retorna lista vazia se o arquivo não existir
    except json.JSONDecodeError:
        print(f"AVISO: Erro ao decodificar JSON em {DATA_FILE}")
        return []

def get_all_destinations(query=None):
    """Retorna todos os destinos ou filtra por query (nome ou país)."""
    destinations = load_destinations()
    if query:
        query = query.lower()
        # Filtra destinos cujo nome OU país contenham a query (ignorando maiúsculas/minúsculas)
        return [
            dest for dest in destinations
            if query in dest['name'].lower() or query in dest['country'].lower()
        ]
    # Se não houver query, retorna todos, ordenados por popularidade (se existir)
    return sorted(destinations, key=lambda x: x.get('popularity', 999))

def get_destination_by_id(destination_id):
    """Busca um destino específico pelo ID."""
    destinations = load_destinations()
    for dest in destinations:
        # Compara o ID do destino com o ID fornecido
        if dest['id'] == destination_id:
            return dest # Retorna o dicionário do destino encontrado
    return None # Retorna None se nenhum destino com esse ID for encontrado