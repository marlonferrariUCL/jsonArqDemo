from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route('/', methods=['get'])
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/estoque', methods=['post'])
def estoque():  # put application's code here
    codItem = request.form.get('codItem')
    desc = request.form.get('desc')
    medida = request.form.get('medida')
    fabricante = request.form.get('fabricante')
    quantidade = request.form.get('quantidade')
    precunit = request.form.get('precunit')

    #DICIONARIO DO ITEM ATUAL
    dici = {
        'codItem':codItem,
        'desc':desc,
        'medida':medida,
        'fabricante':fabricante,
        'quantidade':quantidade,
        'precunit':precunit,
    }
    arq = open('estoque.json', mode='r')
    dados = json.load(arq)
    dados = [d for d in dados]
    dados.append(dici)
    arq.close()
    arq = open('estoque.json', mode='w')
    arq.write(json.dumps(dados))
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run()
