# Clínica Vitalis — instruções do repositório

Repositório da disciplina de Programação e Desenvolvimento Web (CEUB).
Três projetos numa clínica **fictícia**. Visão geral em [README.md](README.md).

## A regra que mais importa

`index.html` na raiz é **gerado**. Nunca edite esse arquivo direto — a próxima
build sobrescreve. Para mudar a landing page:

1. edite `templates/index.template.html` (estrutura) ou `dados/dados.json` (conteúdo);
2. rode `python scripts/build.py`;
3. confira que não sobrou nenhum marcador `{{...}}` — o build falha se sobrar.

O mesmo vale para o `<head>`: versionar o CSS (`style.css?v=N`) se faz no template.

## Os três projetos

| Onde | O quê | Como rodar |
| --- | --- | --- |
| raiz | Projeto 01 — landing page estática | abrir `index.html` ou `python scripts/serve.py` (8000) |
| `api/` | Projeto 02 — API de profissionais | `cd api && python app.py` (5001) |
| `agendamento/` | Projeto 03 — agendamento + frontend | `cd agendamento && python app.py` (5002) |

`dados/profissionais.json` é compartilhado pelos Projetos 02 e 03: mexer nele
afeta os dois. `dados/dados.json` é só da landing page.

## Restrições que valem para tudo

- **Sem bibliotecas externas.** HTML, CSS e JavaScript puro no front; Flask e
  biblioteca padrão no back. Único recurso externo: Google Fonts.
- **Sem `localStorage`/`sessionStorage`.** Preferências (tema, Modo acessível)
  vivem em variável de sessão e se perdem no reload — é intencional.
- **Caminhos relativos**, para o site funcionar em subpasta do GitHub Pages e
  abrindo o `index.html` direto.
- **Flask:** `debug=False` e `host="127.0.0.1"` nos dois apps. Não reverter:
  `debug=True` expõe o depurador do Werkzeug (execução remota de código).
- `agendamento/agendamentos.json` fica versionado **vazio** (`[]`). Se testes
  gravarem dados nele, limpe antes de commitar.

## Acessibilidade — não regredir

- Contraste WCAG AA em todo texto, nos três modos (normal, Modo acessível e
  tema escuro). O pior caso hoje mede 4,66:1.
- `prefers-reduced-motion` desliga todo movimento **sem JavaScript**, e o botão
  "Modo acessível" faz o mesmo em tempo real marcando `data-mov="off"`.
- Um único `<h1>`; toda `<img>` com `alt` descritivo; foco de teclado visível;
  formulário com `label` associada por `for`/`id`.
- O formulário de contato é estático: `preventDefault()`, valida no navegador e
  confirma localmente. Nunca enviar a servidor.

## Direção de arte

Paleta, tipografia e os sete efeitos de scroll estão em
[clinicaLP.md](clinicaLP.md). Só `transform` e `opacity` animam, com
`will-change` apenas onde de fato anima.
