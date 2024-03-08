from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests

# Cria uma instância da classe Flask
app = Flask(__name__)

# Define a rota para o post
@app.route('/age_calculate', methods=['POST'])

# Define a funçao do post 
def age_calculation():

    person_info = request.get_json() # Recebe a requisição POST e armazena o JSON recebido numa variável 
    json_fields = ["name", "birthdate", "date"]

    # Verifica se o body está completo
    for field in json_fields:
        if field not in person_info:
            return jsonify({'error': f"Certifique-se que o corpo da requisição possui o parâmetro '{field}'."}), 400 
            #Verificar erro

    # Define a data de hoje no formato YYYY-MM-DD
    today = datetime.today()

    # Armazena as informações do JSON
    name = person_info["name"]
    birthdate = person_info["birthdate"]
    date = person_info["date"]
        
    # Gera erros para informar inputs incorretos.
    try:
        palavras_nome = name.split() # Divide a string considerando os espaços como separadores

        if len(palavras_nome) != 2:
            raise ValueError("Certifique-se que o nome está no formato 'Nome Sobrenome'.") 
    
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
        
    except Exception:
        return jsonify({'error': "Certifique-se que o nome é uma string no formato 'Nome Sobrenome'."}), 400 # Erro 400 -> Request incompreensível


    try:
        dt_date = datetime.strptime(date, "%Y-%m-%d") # Converte a data para datetime
        dt_birthdate = datetime.strptime(birthdate, "%Y-%m-%d") # Converte a data de aniversário para datetime

        if dt_date <= today:
            raise ValueError("Insira uma data no futuro.") 

        if dt_birthdate > today:
            raise ValueError("Insira uma 'birthdate' no passado.")

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
                       
    except Exception:
        return jsonify({'error': f"Certifique-se que as datas inseridas em 'date' e 'birthdate' são válidas e estão no formato YYYY-MM-DD string no formato 'Nome Sobrenome'.{today}"}), 400
                  
    
    # Caculando a idade atual
    age = relativedelta(today, dt_birthdate).years

    # Calculando a idade futura
    future_age = relativedelta(dt_date, dt_birthdate).years

    response = {"quote": f"Olá, {name}! Você tem {age} anos e em {dt_date.strftime('%d/%m/%Y')} você terá {future_age} anos.",
                "ageNow": age,
                "ageThen": future_age
                }

    return jsonify(response)  # Converte a resposta em JSON e retorna ela


# Definindo funções para a segunda rota.
def get_id_municipio(nome_municipio):
    url = f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios' # Lista de municípios api IBGE
    response = requests.get(url)  # Faz a requisição
    municipios = response.json() # Guarda os municípios em uma alista

    # Faz um loop pela lista
    for municipio in municipios:
        if municipio['nome'].lower() == nome_municipio.lower():
            return int(municipio["id"]) # Retorn o id do município requisitado.
    
    # Gera um erro caso o município não seja encontrado na lista.
    raise ValueError(f"{nome_municipio} não foi encontrado na lista de municípios.")  

def get_bairros(id_municipio): # Bairro aqui equivale a subdistrito
    url = f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{id_municipio}/subdistritos' # Lista de subdistritos(bairros) api IBGE
    response = requests.get(url) 
    bairros_list = response.json()
    bairros = []                   # Define uma lista vazia

    # Faz o loop pela lista e armazena cada bairro na lista "bairros"
    for bairro in bairros_list:
        bairros.append(bairro['nome'])

    return bairros

# Define a rota para o get
@app.route('/bairros', methods=['GET'])
def request_response():
    nome_municipio = request.args.get('municipio') # Pega o parâmetro depois de &municipio = valor  -> estrutura request.args.get
    
    # Executa as funções e armazena o id do município digitado e a lista de bairros do mesmo.
    id_municipio = get_id_municipio(nome_municipio)
    bairros = get_bairros(id_municipio)

    return jsonify({"municipio": nome_municipio, "bairros": bairros})

         
# Executa
if __name__ == '__main__':
    app.run(debug=True)
