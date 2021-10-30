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
    categoria = request.form.get('categoria')
    fabricante = request.form.get('fabricante')
    quantidade = request.form.get('quantidade')
    precunit = request.form.get('precunit')

    #DICIONARIO DO ITEM ATUAL
    dici = {
        'codItem':codItem,
        'desc':desc,
        'medida':medida,
        'categoria':categoria,
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

@app.route('/relatorio', methods=['get'])
def relatorio():
    arq = open('estoque.json', mode='r')
    dados = json.load(arq)
    #CRIA UMA LISTA DE CATEGORIAS PRESENTES
    cat_produtos = []
    for d in dados:
        if d['categoria'] not in cat_produtos:
            cat_produtos.append(d['categoria'])
    #CRIA DICI PARA CONTAGEM DOS ITENS
    diciCat = {}
    for cat in cat_produtos:
        diciCat[cat] = 0
    #CONTAGEM DOS ITENS
    for d in dados:
        diciCat[d['categoria']] += 1
    return render_template('relatorio.html', diciCat=diciCat)

if __name__ == '__main__':
    app.run()
