from flask import Flask, jsonify, request # Adicione 'request'
from flask_cors import CORS
# Importe as funções do seu novo serviço
from services_f import destination_service, ai_service

app = Flask(__name__) 
CORS(app) # Permite requisições do seu frontend React

@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    """Endpoint para buscar destinos. Aceita um parâmetro 'q' para busca."""
    # Pega o valor do parâmetro 'q' da URL (ex: /api/destinations?q=paris)
    query = request.args.get('q', None)
    # Chama a função do serviço para obter os destinos (filtrados ou todos)
    destinations = destination_service.get_all_destinations(query)
    # Retorna a lista de destinos em formato JSON
    return jsonify(destinations)

@app.route('/api/destinations/<string:destination_id>', methods=['GET'])
def get_destination_detail(destination_id):
    """Endpoint para buscar detalhes de um destino específico pelo ID."""
    # Chama a função do serviço para obter um destino pelo ID
    destination = destination_service.get_destination_by_id(destination_id)
    if destination:
        # Se encontrou, retorna o destino em JSON
        return jsonify(destination)
    else:
        # Se não encontrou, retorna erro 404 (Not Found)
        return jsonify({"error": "Destination not found"}), 404
# --- INÍCIO DO CÓDIGO PARA ADICIONAR ---

@app.route('/api/destinations/<string:destination_id>/insights', methods=['GET'])
def get_destination_insights(destination_id):
    """Endpoint para buscar insights da IA para um destino."""
    # Busca os dados básicos do destino para obter nome e país
    destination = destination_service.get_destination_by_id(destination_id)
    if not destination:
        # Se o destino base não for encontrado, retorna 404
        return jsonify({"error": "Destination base data not found"}), 404

    # Log para sabermos que a função foi chamada
    print(f"Buscando insights da IA para: {destination['name']}, {destination['country']}")

    # Chama a função do ai_service para obter os insights
    insights = ai_service.get_ai_insights_for_destination(destination['name'], destination['country'])

    # Log para vermos o que a IA retornou (ou o erro)
    print(f"Insights recebidos: {insights}")

    # Retorna os insights (ou o objeto de erro do ai_service) em formato JSON
    # Se a chamada da IA falhar, o 'insights' já conterá uma chave 'error'
    return jsonify(insights)

# --- FIM DO CÓDIGO PARA ADICIONAR ---

# Mantemos a rota raiz apenas para verificar se o servidor está no ar
@app.route('/')
def index():
    return "o futuro se trilha a partir de agora !"

# Este bloco só é relevante se você rodar com 'python app.py'
# Se usar 'flask run', ele não é executado diretamente,
# mas é bom manter para referência ou uso futuro.
if __name__ == '__main__':
    app.run(debug=True, port=5000)