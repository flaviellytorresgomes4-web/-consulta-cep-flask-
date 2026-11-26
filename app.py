
from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# Página inicial
@app.route('/')
def index():
    return render_template('index.html')


# Rota para buscar o CEP
@app.route('/buscarcep', methods=['POST'])
def buscarcep():

    # Recebe o CEP digitado
    cep = request.form.get('cep', '').strip()

    # Remove caracteres que não sejam números
    cep = ''.join(filter(str.isdigit, cep))

    # Verifica se possui exatamente 8 números
    if len(cep) != 8:
        return render_template(
            'index.html',
            erro='O CEP deve conter exatamente 8 números!',
            cep=cep
        )

    # Consulta a API ViaCEP
    url = f'https://viacep.com.br/ws/{cep}/json/'

    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()

        dados = resposta.json()

        # Verifica se o CEP foi encontrado
        if dados.get('erro'):
            return render_template(
                'index.html',
                erro='CEP não encontrado!',
                cep=cep
            )

        # Retorna os dados para a mesma página
        return render_template(
            'index.html',
            endereco=dados,
            cep=cep
        )

    except requests.RequestException:
        return render_template(
            'index.html',
            erro='Erro ao conectar com a API ViaCEP.',
            cep=cep
        )


# Inicialização do servidor
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
