import os
# Muda a importação principal
from openai import OpenAI # Importa a classe OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

# Use a variável de ambiente correta para a chave da OpenAI
API_KEY = os.getenv("OPENAI_API_KEY") # Ou "AI_API_KEY" se você manteve esse nome no .env

# Configura o cliente OpenAI (nova forma recomendada)
if API_KEY:
    # Cria uma instância do cliente
    client = OpenAI(api_key=API_KEY)
else:
    print("AVISO: OPENAI_API_KEY (ou AI_API_KEY) não encontrada no arquivo .env. O serviço de IA não funcionará.")
    client = None

# A função em si
def get_ai_insights_for_destination(destination_name, country_name):
    """Busca insights da IA (OpenAI) sobre um destino específico usando a nova sintaxe."""
    if not client: # Verifica se o cliente foi inicializado
        return {
            "error": "AI Service not configured (OpenAI API key missing or invalid)",
            "news": "N/A", "tips": "N/A", "prices": "N/A", "recommendations": "N/A" # Inclui recommendations se quiser
        }

    # Mantenha ou ajuste seu prompt aqui
    prompt_content = (
        f"Forneça informações úteis e atualizadas para turistas sobre {destination_name}, {country_name}. "
        "Siga estritamente este formato JSON:\n"
        "{\n"
        '  "news": "Resumo conciso de 1-2 notícias/eventos MUITO recentes (últimos meses) relevantes para turistas. Se nada, diga \'Sem notícias recentes relevantes\'.",\n'
        '  "tips": "3-4 dicas práticas essenciais e acionáveis (ex: melhor época, moeda/gorjeta, tomada, segurança, transporte).",\n'
        '  "prices": "Estimativas de preços médios ATUAIS em moeda local (especifique qual) para: 1 noite hotel 3 estrelas, 1 refeição casual, 1 ticket atração popular.",\n'
        '  "recommendations": "Sugira 2-3 atividades ou experiências imperdíveis e únicas para se fazer neste destino."\n' # Mantenha se quiser recomendações
        "}\n"
        "Responda APENAS com o objeto JSON formatado, sem nenhum texto adicional antes ou depois, e sem usar markdown como ```json."
    )

    try:
        # === MUDANÇA PRINCIPAL AQUI ===
        # Usa o objeto 'client' para chamar a API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente de viagens que fornece informações concisas e úteis em formato JSON."
                },
                {
                    "role": "user",
                    "content": prompt_content,
                }
            ],
            model="gpt-3.5-turbo", # Ou outro modelo como "gpt-4"
            # Pede para a API tentar retornar JSON
            response_format={ "type": "json_object" }
        )
        # ===============================

        # Extrai o conteúdo da resposta
        response_content = chat_completion.choices[0].message.content

        # Tenta analisar o JSON (mesma lógica de antes)
        try:
            insights = json.loads(response_content.strip())
            if all(key in insights for key in ["news", "tips", "prices", "recommendations"]): # Verifique as chaves que você pediu
                 return insights
            else:
                 print(f"AVISO: Resposta JSON da OpenAI incompleta: {response_content}")
                 return {"error": "Incomplete data structure from AI", "news": "N/A", "tips": "N/A", "prices": "N/A", "recommendations": "N/A"} # Adapte as chaves de erro
        except (json.JSONDecodeError, AttributeError) as parse_error:
            print(f"Erro ao decodificar JSON da OpenAI: {parse_error}")
            print(f"Resposta recebida da OpenAI:\n---\n{response_content}\n---")
            return {"error": "Failed to parse OpenAI response", "raw_response": response_content, "news": "N/A", "tips": "N/A", "prices": "N/A", "recommendations": "N/A"} # Adapte as chaves de erro

    except Exception as e:
        print(f"Erro durante a chamada à API da OpenAI: {e}")
        # Erros específicos da API da OpenAI podem ser tratados aqui (e.code, e.status_code...)
        return {"error": f"OpenAI API call failed: {str(e)}", "news": "N/A", "tips": "N/A", "prices": "N/A", "recommendations": "N/A"} # Adapte as chaves de erro

# Bloco para teste direto do arquivo (opcional, não afeta o Flask)
if __name__ == "__main__":
    destination = "Paris"
    country = "França"
    print(f"Testando AI Service para {destination}, {country}...")
    insights = get_ai_insights_for_destination(destination, country)
    print(json.dumps(insights, indent=2, ensure_ascii=False)) # Imprime formatado