from flask import Flask, request, jsonify

# Essa é uma api que permite fazer uma requisição get

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Bem-vindo à API muito básica em Flask!'

@app.route('/api/mensagem') # ao entrar nessa rota, o usuário faz uma get request pro servidor e ele retorna a mensagem

def get_message(): # as informações de uma requisição get fica exposta na URL, diferente do POST, onde a informação enviada não fica exposta.
    message = {'mensagem': 'Esta é uma mensagem da API'} 
    return jsonify(message)


@app.route('/api/post_example', methods=['POST']) # Rota para um requisição post. Ela geralmente não é executada por um browser.

def post_data():
    data = request.get_json()  # Faz a requisição dos dados em json
    
    resposta = {"resposta": "Positivo e operante"}
    return jsonify(data) # Retorna os dados. jsonfy transforma os dados em um arquivo JSON



if __name__ == '__main__':
    app.run(debug=True)
