# Projeto 02 — API de Profissionais de Saúde

API em **Python + Flask** que lê um arquivo **JSON local** e permite consultar
as especialidades e os profissionais da Clínica Vitalis (fictícia), com
**filtro por especialidade** e **busca por nome**.

Disciplina de Programação e Desenvolvimento Web — CEUB
Aluno: Roberto Vital de Araujo

## Como executar

Na pasta `api/`:

```bash
pip install -r requirements.txt
python app.py
```

A API sobe em `http://localhost:5001`.

## Fonte de dados

Lê o arquivo local `../dados/profissionais.json` (JSON), compartilhado com o
Projeto 03. Contém as especialidades e os profissionais.

## Rotas

| Método | Rota | O que faz |
| --- | --- | --- |
| GET | `/` | Mostra as rotas disponíveis |
| GET | `/especialidades` | Lista todas as especialidades |
| GET | `/profissionais` | Lista todos os profissionais |
| GET | `/profissionais?especialidade=nutricao` | Filtra por especialidade |
| GET | `/profissionais?nome=helena` | Busca por nome (parcial, sem acento) |
| GET | `/profissionais/1` | Detalha um profissional pelo id |

## Exemplos

```bash
curl http://localhost:5001/especialidades
curl http://localhost:5001/profissionais
curl "http://localhost:5001/profissionais?especialidade=clinica-geral"
curl "http://localhost:5001/profissionais?nome=nakamura"
```

## Observações

- A busca por nome é **parcial** e **ignora acentos e maiúsculas**
  (ex.: `nome=marchetti` ou `nome=Márchetti` encontram a Dra. Helena).
- O filtro por especialidade aceita o **id** (`nutricao`) ou o **nome**
  (`Nutrição`).
- Dados fictícios, para fins acadêmicos. Nenhuma pessoa real é retratada.
