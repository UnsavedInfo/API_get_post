from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Bem-vindo à API muito básica em Flask!'

@app.route('/api/mensagem')
def get_message():
    message = {'mensagem': 'Esta é uma mensagem da API'}
    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True)
