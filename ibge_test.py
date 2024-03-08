from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Função para obter o ID do município pelo nome
def get_municipio_id(nome_municipio):
    url = f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    response = requests.get(url)
    municipios = response.json()
    for municipio in municipios:
        if municipio['nome'].lower() == nome_municipio.lower():
            return str(municipio['id'])
    return None

# Função para obter os bairros pelo ID do município
def get_bairros_por_municipio(municipio_id):
    url = f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{municipio_id}/subdistritos'
    response = requests.get(url)
    distritos = response.json()
    bairros = [distrito['nome'] for distrito in distritos]
    return bairros

# Rota GET para retornar os bairros de um município
@app.route('/bairros', methods=['GET'])
def bairros_por_municipio():
    nome_municipio = request.args.get('municipio')
    if nome_municipio:
        municipio_id = get_municipio_id(nome_municipio)
        if municipio_id:
            bairros = get_bairros_por_municipio(municipio_id)
            return jsonify({
                'municipio': nome_municipio,
                'bairros': bairros
            })
        else:
            return jsonify({'error': 'Município não encontrado'}), 404
    else:
        return jsonify({'error': 'Parâmetro "municipio" não encontrado'}), 400

if __name__ == '__main__':
    app.run(debug=True)
