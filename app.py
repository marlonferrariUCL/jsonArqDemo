from flask import Flask, render_template, request
import json

app = Flask(__name__)

def joinProdEstoque():
    #le os dados
    arq = open('capEstoque.json', 'r')
    est = json.load(arq)
    arq = open('estoque.json', 'r')
    prod = json.load(arq)
    arq = open('codProd.json', 'r')
    desc = json.load(arq)
    #cria o dicionario das categorias no estoque
    chaves = [x for x in est.keys()]
    diciProdEst = {}
    for chave in chaves:
        diciProdEst[chave] = []
    #adiciona a capacidade da categoria no dicionario
    #{'beb': [100], 'frig': [20], 'limp': [350], 'vest': [50]}
    for chave, valor in est.items():
        diciProdEst[chave].append(valor)
    #cria a soma total das categorias existentes nos produtos do estoque
    #{'beb': 103, 'vest': 2}
    aux = {}
    for produto in prod:
        aux[produto['categoria']] = 0
    for produto in prod:
        aux[produto['categoria']] += int(produto['quantidade'])
    #adicionar os totais do estoque no dicionario
    for chave, valor in aux.items():
        diciProdEst[chave].append(valor)
    #cria os zeros nas categorias sem estoque
    for chave, valor in diciProdEst.items():
        if len(valor) < 2:
            diciProdEst[chave].append(0)
    #{'beb': [100, 103], 'frig': [20, 0], 'limp': [350, 0], 'vest': [50, 2]}
    #cria o dicionario com chaves da descricao
    diciProdEstMelhor = {}
    for codigo, descricao in desc.items():
        diciProdEstMelhor[descricao] = codigo
    #transfere os valores do dicionario antigo para o novo
    for chave, id in diciProdEstMelhor.items():
        diciProdEstMelhor[chave] = diciProdEst[id]
    #{'Bebida': [100, 103], 'Frigorífico': [20, 0], 'Limpeza': [350, 0],'Vestuário': [50, 2]}
    return diciProdEstMelhor

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
    diciProdEstoque = joinProdEstoque()
    return render_template('relatorio.html', diciCat=diciCat, diciProdEstoque=diciProdEstoque)

if __name__ == '__main__':
    app.run()
