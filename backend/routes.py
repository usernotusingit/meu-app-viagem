from flask import Blueprint, jsonify, request
from services_f import destination_service, ai_service

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/destinations', methods=['GET'])
def get_destinations():
    """Endpoint para buscar destinos. Aceita um parâmetro 'q' para busca."""
    query = request.args.get('q', None)
    destinations = destination_service.get_all_destinations(query)
    return jsonify(destinations)

@api_bp.route('/destinations/<string:destination_id>', methods=['GET'])
def get_destination_detail(destination_id):
    """Endpoint para buscar detalhes de um destino específico."""
    destination = destination_service.get_destination_by_id(destination_id)
    if destination:
        return jsonify(destination)
    else:
        return jsonify({"error": "Destination not found"}), 404

@api_bp.route('/destinations/<string:destination_id>/insights', methods=['GET'])
def get_destination_insights(destination_id):
    """Endpoint para buscar insights da IA para um destino."""
    destination = destination_service.get_destination_by_id(destination_id)
    if not destination:
        return jsonify({"error": "Destination not found"}), 404

    # Chama o serviço de IA usando a versão atualizada que integra a API do OpenAI
    insights = ai_service.get_ai_insights_for_destination(destination['name'], destination['country'])

    # Se a resposta da IA contiver um erro, retorne um status 500
    if insights.get("error"):
        return jsonify(insights), 500

    return jsonify(insights)
