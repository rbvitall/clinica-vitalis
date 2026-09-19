# Clínica Vitalis — Projetos Web (CEUB)

Repositório da disciplina de **Programação e Desenvolvimento Web** do CEUB.
Aluno: **Roberto Vital de Araujo**.

A Clínica Vitalis é uma clínica de saúde **fictícia**, criada para servir de
cenário aos três projetos da disciplina: a landing page institucional, a API
que expõe os profissionais e o sistema de agendamento de consultas. Clínica,
profissionais, registros e agendamentos são inventados.

---

## Projeto 01 — Landing Page (raiz)

Página institucional estática da clínica, em HTML, CSS e JavaScript puro, com
formulário de contato sem envio a servidor.

**Site publicado:** `<LINK DO PAGES>`

### Como abrir

Abra o arquivo `index.html` diretamente no navegador — os caminhos são
relativos e tudo funciona sem servidor.

Ou suba um servidor local:

```bash
python scripts/serve.py
# http://localhost:8000
```

Para regerar o `index.html` a partir de `dados/dados.json` e do template:

```bash
python scripts/build.py
```

Detalhes de direção de arte, efeitos e checklist de requisitos estão em
[`README-projeto-01.md`](README-projeto-01.md).

---

## Projeto 02 — API de Profissionais (`api/`)

API em Flask que lê um arquivo JSON local e permite consultar as
especialidades e os profissionais da clínica, com filtro por especialidade e
busca por nome (parcial e sem acento).

### Como rodar

```bash
cd api
pip install -r requirements.txt
python app.py
# http://localhost:5001
```

### Rotas

| Método | Rota | O que faz |
| --- | --- | --- |
| GET | `/` | Mostra as rotas disponíveis |
| GET | `/especialidades` | Lista todas as especialidades |
| GET | `/profissionais` | Lista todos os profissionais |
| GET | `/profissionais?especialidade=<id>` | Filtra por especialidade |
| GET | `/profissionais?nome=<texto>` | Busca por nome (parcial, sem acento) |
| GET | `/profissionais/<id>` | Detalha um profissional pelo id |

---

## Projeto 03 — Sistema de Agendamento (`agendamento/`)

Aplicação completa, com backend em Flask e frontend em `web/`, para marcação de
consultas. Permite escolher a especialidade e o profissional, ver as datas e os
horários livres, agendar informando nome e CPF (validado pelos dígitos
verificadores), consultar os agendamentos por CPF e cancelá-los. Os
agendamentos ficam gravados em `agendamentos.json`.

### Como rodar

```bash
cd agendamento
pip install -r requirements.txt
python app.py
# http://localhost:5002
```

### Rotas

| Método | Rota | O que faz |
| --- | --- | --- |
| GET | `/api/especialidades` | Lista especialidades |
| GET | `/api/profissionais?especialidade=<id>` | Profissionais da especialidade |
| GET | `/api/disponibilidade?profissional=<id>` | Datas e horários livres |
| POST | `/api/agendamentos` | Cria um agendamento |
| GET | `/api/agendamentos?cpf=<cpf>` | Consulta por CPF |
| POST | `/api/agendamentos/<id>/cancelar` | Cancela um agendamento |

---

## Estrutura do repositório

```
clinica-vitalis/
├── index.html                 # Projeto 01 — página publicada (gerada, versionada)
├── css/style.css
├── js/main.js
├── assets/img/                # ilustrações SVG, fotos e favicon
├── templates/                 # template com marcadores {{...}}
├── scripts/
│   ├── build.py               # dados/dados.json + template -> index.html
│   └── serve.py               # servidor local do Projeto 01
├── dados/
│   ├── dados.json             # conteúdo da landing page
│   └── profissionais.json     # compartilhado pelos Projetos 02 e 03
├── api/                       # Projeto 02
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── agendamento/               # Projeto 03
│   ├── app.py
│   ├── requirements.txt
│   ├── agendamentos.json      # agendamentos criados (começa vazio)
│   ├── README.md
│   ├── web/index.html         # frontend do agendamento
│   └── docs/                  # EAP e PDF de entrega
├── entrega/                   # roteiro de vídeo e PDFs do Projeto 01
├── referencia/                # implementação de referência (consulta)
├── README.md                  # este arquivo
└── README-projeto-01.md       # documentação detalhada da landing page
```

---

## Observações

Os Projetos 02 e 03 leem o mesmo arquivo **`dados/profissionais.json`**, com as
5 especialidades e os 6 profissionais da clínica. Alterar esse arquivo reflete
nos dois projetos ao mesmo tempo.

Todo o conteúdo é **fictício** e sem fins comerciais: a clínica, os
profissionais, os registros profissionais (CRM/CRN), os depoimentos e os
agendamentos foram inventados para o trabalho acadêmico. As ilustrações foram
criadas para este projeto e nenhuma pessoa real é retratada.
