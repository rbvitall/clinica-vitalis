# Projeto 03 — Sistema de Agendamento

Aplicação completa (**frontend + backend**) para marcação de consultas/exames
na Clínica Vitalis (fictícia), em **Python + Flask** com **armazenamento local
em JSON**.

Disciplina de Programação e Desenvolvimento Web — CEUB
Aluno: Roberto Vital de Araujo

## Funcionalidades

- Escolha da **especialidade** e do **profissional**
- Exibição das **datas e horários disponíveis** (próximos 21 dias)
- Formulário com **nome** e **CPF** (CPF validado pelos dígitos verificadores)
- **Consulta por CPF** e **cancelamento** de agendamento
- **Armazenamento local** em `agendamentos.json`

## Como executar

Na pasta `agendamento/`:

```bash
pip install -r requirements.txt
python app.py
```

Abra no navegador: `http://localhost:5002`

O frontend e a API são servidos pelo mesmo Flask, então basta abrir esse
endereço — não precisa de mais nada.

## Fonte de dados

- Profissionais e especialidades: `../dados/profissionais.json` (compartilhado
  com o Projeto 02).
- Agendamentos criados: `agendamentos.json` (gerado automaticamente).

## API (usada pelo frontend)

| Método | Rota | O que faz |
| --- | --- | --- |
| GET | `/api/especialidades` | Lista especialidades |
| GET | `/api/profissionais?especialidade=<id>` | Profissionais da especialidade |
| GET | `/api/disponibilidade?profissional=<id>` | Datas/horários livres |
| POST | `/api/agendamentos` | Cria um agendamento (nome, cpf, data, horário) |
| GET | `/api/agendamentos?cpf=<cpf>` | Consulta por CPF |
| POST | `/api/agendamentos/<id>/cancelar` | Cancela um agendamento |

## Observação sobre o CPF

O CPF é validado pelo algoritmo oficial dos dígitos verificadores. Para testar,
use um CPF válido de exemplo, como **526.018.159-06**. Todos os dados são
fictícios e ficam apenas no seu computador.
