"""
Projeto 03 — Sistema de Agendamento (Clínica Vitalis)
Disciplina de Programação e Desenvolvimento Web — CEUB
Aluno: Roberto Vital de Araujo

Aplicação completa (frontend + backend) para marcação de consultas/exames.
- Escolha da especialidade e do profissional
- Exibição das datas/horários disponíveis
- Formulário com nome e CPF (CPF validado)
- Consulta de agendamentos por CPF e cancelamento
- Armazenamento local em JSON

Como rodar:
    pip install -r requirements.txt
    python app.py
Depois abra no navegador: http://localhost:5002
"""

import json
import re
import unicodedata
from datetime import date, timedelta
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory

BASE = Path(__file__).resolve().parent
WEB = BASE / "web"
DADOS = BASE.parent / "dados" / "profissionais.json"          # compartilhado com o Projeto 02
AGENDAMENTOS = BASE / "agendamentos.json"                     # armazenamento local

DIAS = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]       # date.weekday(): 0=seg
DIAS_LONGOS = {"seg": "Segunda", "ter": "Terça", "qua": "Quarta",
               "qui": "Quinta", "sex": "Sexta", "sab": "Sábado", "dom": "Domingo"}

app = Flask(__name__, static_folder=None)


# ---------------------------------------------------------------- dados
def carregar_dados():
    with open(DADOS, encoding="utf-8") as f:
        return json.load(f)


def carregar_agendamentos():
    if not AGENDAMENTOS.exists():
        return []
    try:
        with open(AGENDAMENTOS, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []


def salvar_agendamentos(lista):
    with open(AGENDAMENTOS, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)


def sem_acento(texto):
    texto = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in texto if not unicodedata.combining(c)).lower().strip()


def so_digitos(texto):
    return re.sub(r"\D", "", texto or "")


def cpf_valido(cpf):
    """Valida CPF pelos dígitos verificadores (algoritmo oficial)."""
    cpf = so_digitos(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    nums = [int(c) for c in cpf]
    for i in (9, 10):
        soma = sum(nums[j] * ((i + 1) - j) for j in range(i))
        dv = (soma * 10) % 11
        dv = 0 if dv == 10 else dv
        if dv != nums[i]:
            return False
    return True


def formatar_cpf(cpf):
    c = so_digitos(cpf)
    return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}" if len(c) == 11 else cpf


def achar_profissional(dados, pid):
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return None
    for p in dados["profissionais"]:
        if p["id"] == pid:
            return p
    return None


def slot_disponivel(prof, data_, horario):
    """Confere se a data/horário existem de fato na agenda do profissional."""
    try:
        dia = date.fromisoformat(str(data_))
    except (TypeError, ValueError):
        return False, "Data inválida."
    hoje = date.today()
    if not (hoje < dia <= hoje + timedelta(days=21)):
        return False, "Data fora do período de agendamento (próximos 21 dias)."
    if DIAS[dia.weekday()] not in prof["atende_dias"]:
        return False, "O profissional não atende nesse dia."
    if horario not in prof["horarios"]:
        return False, "Horário indisponível para esse profissional."
    return True, None


def nome_especialidade(dados, esp_id):
    for e in dados["especialidades"]:
        if e["id"] == esp_id:
            return e["nome"]
    return esp_id


# ---------------------------------------------------------------- API
@app.route("/api/especialidades")
def api_especialidades():
    return jsonify(carregar_dados()["especialidades"])


@app.route("/api/profissionais")
def api_profissionais():
    dados = carregar_dados()
    profs = dados["profissionais"]
    esp = request.args.get("especialidade")
    if esp:
        esp = sem_acento(esp)
        profs = [p for p in profs if sem_acento(p["especialidade"]) == esp]
    return jsonify([{
        "id": p["id"],
        "nome": p["nome"],
        "registro": p["registro"],
        "especialidade": p["especialidade"],
        "especialidade_nome": nome_especialidade(dados, p["especialidade"]),
    } for p in profs])


@app.route("/api/disponibilidade")
def api_disponibilidade():
    """Datas e horários livres do profissional nos próximos 21 dias."""
    dados = carregar_dados()
    pid = request.args.get("profissional")
    prof = achar_profissional(dados, pid) if pid else None
    if not prof:
        return jsonify({"erro": "Profissional não encontrado"}), 404

    ocupados = {
        (a["profissional_id"], a["data"], a["horario"])
        for a in carregar_agendamentos() if a["status"] == "ativo"
    }

    agenda = []
    hoje = date.today()
    for i in range(1, 22):                       # a partir de amanhã
        dia = hoje + timedelta(days=i)
        sigla = DIAS[dia.weekday()]
        if sigla not in prof["atende_dias"]:
            continue
        livres = [h for h in prof["horarios"]
                  if (prof["id"], dia.isoformat(), h) not in ocupados]
        if livres:
            agenda.append({
                "data": dia.isoformat(),
                "data_br": dia.strftime("%d/%m/%Y"),
                "dia_semana": DIAS_LONGOS[sigla],
                "horarios": livres,
            })
    return jsonify({
        "profissional": prof["nome"],
        "especialidade_nome": nome_especialidade(dados, prof["especialidade"]),
        "dias": agenda,
    })


@app.route("/api/agendamentos", methods=["POST"])
def api_criar():
    dados = carregar_dados()
    corpo = request.get_json(silent=True) or {}
    nome = (corpo.get("nome") or "").strip()
    cpf = corpo.get("cpf") or ""
    pid = corpo.get("profissional_id")
    data_ = corpo.get("data")
    horario = corpo.get("horario")

    # validações
    if len(nome) < 3 or len(nome) > 80:
        return jsonify({"erro": "Informe o nome completo (3 a 80 caracteres)."}), 400
    if not cpf_valido(cpf):
        return jsonify({"erro": "CPF inválido. Confira os números."}), 400
    prof = achar_profissional(dados, pid) if pid else None
    if not prof:
        return jsonify({"erro": "Selecione um profissional válido."}), 400
    if not data_ or not horario:
        return jsonify({"erro": "Selecione a data e o horário."}), 400
    ok, msg = slot_disponivel(prof, data_, horario)
    if not ok:
        return jsonify({"erro": msg}), 400

    agendamentos = carregar_agendamentos()
    # evita marcar o mesmo horário duas vezes
    for a in agendamentos:
        if (a["status"] == "ativo" and a["profissional_id"] == prof["id"]
                and a["data"] == data_ and a["horario"] == horario):
            return jsonify({"erro": "Esse horário acabou de ser ocupado. Escolha outro."}), 409

    novo = {
        "id": (max([a["id"] for a in agendamentos], default=0) + 1),
        "profissional_id": prof["id"],
        "profissional_nome": prof["nome"],
        "especialidade_nome": nome_especialidade(dados, prof["especialidade"]),
        "data": data_,
        "data_br": date.fromisoformat(data_).strftime("%d/%m/%Y"),
        "horario": horario,
        "nome": nome,
        "cpf": formatar_cpf(cpf),
        "status": "ativo",
    }
    agendamentos.append(novo)
    salvar_agendamentos(agendamentos)
    return jsonify({"ok": True, "agendamento": novo}), 201


@app.route("/api/agendamentos")
def api_consultar():
    """Consulta agendamentos por CPF."""
    cpf = request.args.get("cpf")
    if not cpf:
        return jsonify({"erro": "Informe o CPF para consultar."}), 400
    alvo = so_digitos(cpf)
    encontrados = [a for a in carregar_agendamentos() if so_digitos(a["cpf"]) == alvo]
    return jsonify({"total": len(encontrados), "agendamentos": encontrados})


@app.route("/api/agendamentos/<int:aid>/cancelar", methods=["POST"])
def api_cancelar(aid):
    agendamentos = carregar_agendamentos()
    for a in agendamentos:
        if a["id"] == aid:
            if a["status"] == "cancelado":
                return jsonify({"erro": "Esse agendamento já estava cancelado."}), 409
            a["status"] = "cancelado"
            salvar_agendamentos(agendamentos)
            return jsonify({"ok": True, "agendamento": a})
    return jsonify({"erro": "Agendamento não encontrado."}), 404


# ---------------------------------------------------------------- frontend
@app.route("/")
def index():
    return send_from_directory(WEB, "index.html")


@app.route("/<path:arquivo>")
def estaticos(arquivo):
    return send_from_directory(WEB, arquivo)


if __name__ == "__main__":
    print("Agendamento da Clínica Vitalis em http://localhost:5002")
    # debug=False: não expõe o depurador interativo do Werkzeug (evita execução
    # remota de código) nem stack traces ao usuário.
    app.run(host="127.0.0.1", port=5002, debug=False)
