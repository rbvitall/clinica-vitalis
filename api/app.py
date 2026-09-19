"""
Projeto 02 — API de Profissionais de Saúde (Clínica Vitalis)
Disciplina de Programação e Desenvolvimento Web — CEUB
Aluno: Roberto Vital de Araujo

API em Flask que lê um arquivo JSON local e permite consultar as
especialidades e os profissionais da clínica, com filtro por
especialidade e busca por nome.

Como rodar:
    pip install -r requirements.txt
    python app.py
Depois abra no navegador: http://localhost:5001
"""

import json
import unicodedata
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(__name__)

# Caminho do arquivo de dados (compartilhado com o Projeto 03).
# Fica em ../dados/profissionais.json em relação a este arquivo.
DADOS = Path(__file__).resolve().parent.parent / "dados" / "profissionais.json"


def carregar_dados():
    """Lê o arquivo JSON local a cada requisição (leitura de arquivo local)."""
    with open(DADOS, encoding="utf-8") as f:
        return json.load(f)


def sem_acento(texto):
    """Normaliza texto para busca: minúsculo e sem acentos."""
    texto = unicodedata.normalize("NFKD", texto or "")
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower().strip()


def nome_especialidade(dados, esp_id):
    for e in dados["especialidades"]:
        if e["id"] == esp_id:
            return e["nome"]
    return esp_id


def formatar_profissional(dados, p):
    """Devolve o profissional com o nome legível da especialidade."""
    return {
        "id": p["id"],
        "nome": p["nome"],
        "especialidade": p["especialidade"],
        "especialidade_nome": nome_especialidade(dados, p["especialidade"]),
        "registro": p["registro"],
    }


@app.route("/")
def raiz():
    """Página inicial da API: mostra as rotas disponíveis."""
    return jsonify({
        "api": "Clínica Vitalis — Profissionais de Saúde",
        "versao": "1.0",
        "rotas": {
            "GET /especialidades": "Lista todas as especialidades",
            "GET /profissionais": "Lista todos os profissionais",
            "GET /profissionais?especialidade=<id>": "Filtra por especialidade",
            "GET /profissionais?nome=<texto>": "Busca por nome (parcial, sem acento)",
            "GET /profissionais/<id>": "Detalha um profissional",
        },
    })


@app.route("/especialidades")
def listar_especialidades():
    dados = carregar_dados()
    return jsonify(dados["especialidades"])


@app.route("/profissionais")
def listar_profissionais():
    dados = carregar_dados()
    profissionais = dados["profissionais"]

    # Filtro por especialidade (?especialidade=nutricao)
    especialidade = request.args.get("especialidade")
    if especialidade:
        especialidade = sem_acento(especialidade)
        profissionais = [
            p for p in profissionais
            if sem_acento(p["especialidade"]) == especialidade
            or sem_acento(nome_especialidade(dados, p["especialidade"])) == especialidade
        ]

    # Busca por nome (?nome=helena) — parcial e sem acento
    nome = request.args.get("nome")
    if nome:
        alvo = sem_acento(nome)
        profissionais = [p for p in profissionais if alvo in sem_acento(p["nome"])]

    resultado = [formatar_profissional(dados, p) for p in profissionais]
    return jsonify({"total": len(resultado), "profissionais": resultado})


@app.route("/profissionais/<int:pid>")
def detalhar_profissional(pid):
    dados = carregar_dados()
    for p in dados["profissionais"]:
        if p["id"] == pid:
            return jsonify(formatar_profissional(dados, p))
    return jsonify({"erro": "Profissional não encontrado", "id": pid}), 404


@app.errorhandler(404)
def nao_encontrado(_):
    return jsonify({"erro": "Rota não encontrada"}), 404


if __name__ == "__main__":
    print("API da Clínica Vitalis rodando em http://localhost:5001")
    # debug=False e host local: sem depurador exposto nem acesso pela rede.
    app.run(host="127.0.0.1", port=5001, debug=False)
