from flask import Flask, render_template, request, redirect
import os
from unidecode import unidecode
import json

app = Flask(__name__)

os.environ["FLASK_DEBUG"] = "True"
app.debug = os.environ.get("FLASK_DEBUG") == "True"


def carregarGlossario(): # carrega o arquivo no app
    with open("dados.json", "r", encoding="utf-8") as db: # r = read
        conceitos = json.load(db)
    return conceitos


def salvarGlossario(dicio):  # salva as mudanças no arquivo
    # o parâmetro é a variável que enviará as mudanças
    with open("dados.json", "w", encoding="utf-8") as db: # w = write
        json.dump(dicio, db, ensure_ascii=False, indent=4)
        # load para ler e dump para enviar
        # ensure_ascii=False permite que caracteres especiais/acentuação sejam enviados para o arquivo


def carregarTarefas(arquivo):  # lê o arquivo
    # arquivo como parâmetro é usado pois temos três arquivos de tarefas
    with open(arquivo, "r", encoding="utf-8") as db:
        tarefas = [linha.strip() for linha in db.readlines()]
        # cada linha do arquivo será lida como um item da lista
    return tarefas


def salvarTarefas(tarefas, arquivo): # o primeiro parâmetro é a variável que enviará as mudanças
    # o segunto parâmetro é o arquivo que receberá as mudanças
    with open(arquivo, "w", encoding="utf-8") as db:
        for tarefa in tarefas:
            db.write(tarefa + "\n")
            # \n para quebrar a linha no arquivo txt


conceitos = carregarGlossario()

listaDeTarefas = carregarTarefas("tarefas.txt")

prioridades = carregarTarefas("tarefaspriorizadas.txt")

selecionadas = carregarTarefas("tarefasfeitas.txt")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/glossario", methods=["GET", "POST"])
def glossario():
    if request.method == "POST": # quando há adição de termos no glossário
        termo = request.form["termo"]
        definicao = request.form["definicao"]
        termo = termo.capitalize().rstrip()
        # para uniformizar os termos no arquivo e tirar o espaço no final
        conceitos.setdefault(termo, definicao)
        # setdefault adiciona termos mas não sobrepõe um termo que já existe no dicionário
        salvarGlossario(conceitos)
        return redirect("/glossario")
    else:
        pesquisa = request.args.get("pesquisar", "").lower()
        # request.args é um objeto do flask que pega o argumento da pesquisa e retorna num formato de dicionário
        # o get pega o valor associado a chave ou retorna o segundo argumento nesse caso a str vazia ""
        # "pesquisar" é o identificador da barra de pesquisa no html (name="pesquisar")
        # o lower() foi usado para uniformizar a pesquisa em lowercase
        pesquisa = unidecode(pesquisa)
        # unidecode é uma biblioteca do python que ignora a acentuação e caracteres especiais
        if pesquisa:
            pesquisado = {
                termo: descricao
                for termo, descricao in conceitos.items()
                if pesquisa in unidecode(termo.lower())
                # se houver pesquisa, a variável "pesquisado" retornará um dicionário com os termos em "conceitos" que correspondam ao que foi pesquisado
                # os termos de "conceitos" são passados filtros para ignorar de acentuação, caracteres especiais e capitalização de letras
            }
        else:
            pesquisado = {} 
            # a variável "pesquisado" precisa estar associada a um valor
            # pode ser qualquer valor pois quando não há pesquisa ele não irá interferir
            # esse valor é necessário para ele seja considerado como existente no render_template

    return render_template(
        "glossario.html",
        glossario=sorted(conceitos.items()),  # sorted coloca o glossário em ordem alfabética
        pesquisado=pesquisado,
        pesquisa=pesquisa,
    )


@app.route("/deletar/<string:termo>", methods=["GET", "POST"])
def deletarTermo(termo):
    del conceitos[termo]
    salvarGlossario(conceitos) # para atualizar o arquivo
    return redirect("/glossario")


@app.route("/alterar-termo/<string:termo>", methods=["GET", "POST"])
def alterarTermo(termo):
    novoTermo = request.form["novotermo"]
    novoTermo = novoTermo.capitalize().rstrip()
    novaDefinicao = request.form["novadefinicao"]
    if novoTermo == "" and novaDefinicao == "":
        return redirect("/glossario")
    elif novoTermo == "":
        conceitos[termo] = novaDefinicao
    elif novaDefinicao == "":
        conceitos[novoTermo] = conceitos.pop(termo)
    else:
        conceitos[novoTermo] = conceitos.pop(termo)
        conceitos[novoTermo] = novaDefinicao
    salvarGlossario(conceitos)
    return redirect("/glossario")


@app.route("/tarefas", methods=["GET", "POST"])
def tarefas():
    if request.method == "POST":
        tarefa = request.form["tarefa"]
        if tarefa not in listaDeTarefas:
            listaDeTarefas.append(tarefa)
            salvarTarefas(listaDeTarefas, "tarefas.txt")
        return redirect("/tarefas")
    else:
        return render_template(
            "tarefas.html",
            listaDeTarefas=listaDeTarefas,
            prioridades=prioridades,
            selecionadas=selecionadas,
        )


@app.route("/priorizar/<int:indice>")
def priorizar(indice):
    mover = listaDeTarefas.pop(indice)
    prioridades.append(mover) # remove a tarefa de uma lista e coloca na outra
    salvarTarefas(listaDeTarefas, "tarefas.txt")
    salvarTarefas(prioridades, "tarefaspriorizadas.txt")
    return redirect("/tarefas")


@app.route("/retirar-prioridade/<int:indice>")
def retirarPrioridade(indice):
    mover = prioridades.pop(indice)
    listaDeTarefas.append(mover) # remove a tarefa de uma lista e coloca na outra
    salvarTarefas(listaDeTarefas, "tarefas.txt")
    salvarTarefas(prioridades, "tarefaspriorizadas.txt")
    return redirect("/tarefas")


@app.route("/check/<int:indice>")
def checkbox(indice):
    tarefa = listaDeTarefas[indice]
    if tarefa in selecionadas:
        selecionadas.remove(tarefa)
    else:
        selecionadas.append(tarefa)
    salvarTarefas(selecionadas, "tarefasfeitas.txt")
    return redirect("/tarefas")


# para tarefas de prioridades
@app.route("/check-up/<int:indice>")
def checkboxP(indice):
    tarefa = prioridades[indice]
    if tarefa in selecionadas:
        selecionadas.remove(tarefa)
    else:
        selecionadas.append(tarefa)
    salvarTarefas(selecionadas, "tarefasfeitas.txt")
    return redirect("/tarefas")


@app.route("/del-tarefa/<int:indice>")
def deletarTarefa(indice):
    if listaDeTarefas[indice] in selecionadas:
        selecionadas.remove(listaDeTarefas[indice])
        # usamos o remove pois não se sabe o seu índice na lista de tarefas feitas
        salvarTarefas(selecionadas, "tarefasfeitas.txt")
    del listaDeTarefas[indice]  # aqui sabemos o índice
    salvarTarefas(listaDeTarefas, "tarefas.txt")
    return redirect("/tarefas")


@app.route("/del-up-tarefa/<int:indice>")
def deletarTarefaPriorizada(indice):
    if prioridades[indice] in selecionadas:
        selecionadas.remove(prioridades[indice])
        salvarTarefas(selecionadas, "tarefasfeitas.txt")
    del prioridades[indice]
    salvarTarefas(prioridades, "tarefaspriorizadas.txt")
    return redirect("/tarefas")


@app.route("/alterar-tarefa/<int:indice>", methods=["GET", "POST"])
def editarTarefa(indice):
    novaTarefa = request.form["novatarefa"]
    if novaTarefa != "":
        if listaDeTarefas[indice] in selecionadas:
            selecionadas.remove(listaDeTarefas[indice])
            selecionadas.append(novaTarefa)
            salvarTarefas(selecionadas, "tarefasfeitas.txt")
        listaDeTarefas[indice] = novaTarefa
        salvarTarefas(listaDeTarefas, "tarefas.txt")
    return redirect("/tarefas")


@app.route("/alterar-up-tarefa/<int:indice>", methods=["GET", "POST"])
def editarTarefaPriorizada(indice):
    novaTarefa = request.form["novatarefapriorizada"]
    if novaTarefa != "":
        if prioridades[indice] in selecionadas:
            selecionadas.remove(prioridades[indice])
            selecionadas.append(novaTarefa)
            salvarTarefas(selecionadas, "tarefasfeitas.txt")
        prioridades[indice] = novaTarefa
        salvarTarefas(prioridades, "tarefaspriorizadas.txt")
    return redirect("/tarefas")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


if __name__ == "__main__":
    app.run(debug=True)
