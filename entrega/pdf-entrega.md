# Conteúdo do PDF de entrega

> Copie para o Word/Google Docs e exporte como PDF, ou converta este arquivo
> direto. Preencha todos os campos marcados com `<...>`.

---

# Projeto 01 — Landing Page
## Clínica Vitalis

**Disciplina:** `<nome da disciplina>`
**Professor(a):** `<nome do professor>`
**Aluno:** `<seu nome completo>`
**Matrícula:** `<sua matrícula>`
**Semestre:** `<ex.: 2026/2>`
**Data de entrega:** `<dd/mm/aaaa>`

---

### Links da entrega

| Item | Endereço |
| --- | --- |
| Repositório no GitHub | `<https://github.com/SEU-USUARIO/NOME-DO-REPO>` |
| Site publicado (GitHub Pages) | `<https://SEU-USUARIO.github.io/NOME-DO-REPO/>` |
| Vídeo de apresentação | `<link do YouTube / Drive — deixar como "não listado" ou público>` |

---

### Descrição

Landing page institucional de uma clínica de saúde **fictícia**, a Clínica
Vitalis. A página apresenta os serviços oferecidos, a equipe de profissionais,
depoimentos de pacientes, perguntas frequentes e um formulário de contato
estático, sem processamento no servidor.

Clínica, profissionais, registros profissionais e depoimentos são inventados
para fins acadêmicos. Nenhuma pessoa real é retratada: todas as imagens são
ilustrações SVG produzidas para este projeto.

---

### Tecnologias utilizadas

- **HTML5** semântico — um único `<h1>`, acordeão nativo com `<details>`.
- **CSS3** puro — tokens de design em `:root`, layout mobile-first, sem framework.
- **JavaScript** puro — sem bibliotecas externas e sem `localStorage`.
- **Python 3** (biblioteca padrão) — `build.py` gera o HTML a partir de um JSON;
  `serve.py` sobe um servidor local. O site publicado não depende de Python.
- **Google Fonts** — Cormorant e Public Sans (único recurso externo).

---

### Direção de arte

O projeto segue uma direção visual **imersiva**, definida antes da implementação:
contraste entre uma serifada grande e leve (Cormorant) e uma sans miúda
(Public Sans), paleta de baixa saturação (`#F6F5F0`, `#20241D`, `#7C8B6F`,
`#54613F`, `#161C15`) e, sobretudo, movimento — a página tem vida já parada e
ganha profundidade ao rolar. As regras estão em `CLAUDE.md` e no
`BRIEF-IMERSIVO.md`, com uma implementação de referência em `referencia/`.

Sete efeitos, todos em CSS e JavaScript puro, sem nenhuma biblioteca:

1. Esferas de luz animadas no hero, somadas a paralaxe de scroll.
2. Bloco do hero com inclinação 3D por scroll e mouse.
3. Seção de serviços presa na tela, com os painéis avançando em profundidade.
4. Contadores que sobem ao entrar na viewport, com brilho em paralaxe.
5. Reveals no scroll via `animation-timeline`, com fallback.
6. `prefers-reduced-motion` desligando todo o movimento.
7. Marquee de especialidades em loop infinito, pausando no hover.

---

### Requisitos atendidos

| # | Requisito | Situação |
| --- | --- | --- |
| 1 | Título na aba do navegador (`<title>`) | Atendido |
| 2 | Pelo menos 2 imagens de serviços, com texto alternativo | Atendido — 4 imagens de serviços; 7 `<img>` no total, todas com `alt` |
| 3 | Descrição de cada serviço | Atendido — 4 serviços descritos |
| 4 | Equipe fictícia com ao menos 3 membros (foto + cargo) | Atendido — 3 profissionais com retrato, cargo e registro |
| 5 | Ao menos 2 níveis de cabeçalho (H1, H2, H3) | Atendido — 1 `<h1>`, 10 `<h2>`, 7 `<h3>` |
| 6 | Formulário com Nome, E-mail, Cidade e Estado, sem envio ao servidor | Atendido — validação no navegador e confirmação local |

---

### Itens adicionais de qualidade

- Responsiva de 360 px a 1440 px ou mais, sem rolagem horizontal.
- Acessibilidade: link de pular para o conteúdo, foco de teclado visível,
  `aria-expanded` no menu, rótulos associados a todos os campos, contraste WCAG AA.
- `prefers-reduced-motion` respeitado em todas as animações.
- A página continua legível com o JavaScript desativado.
- Animações pausam ao sair da viewport, para não consumir GPU à toa.
- Publicada no GitHub Pages (item extra do enunciado).

---

### Como executar localmente

1. Clonar o repositório e entrar na pasta.
2. Abrir `index.html` diretamente no navegador, **ou**
3. Executar `python scripts/serve.py` e acessar `http://localhost:8000`.
4. Para regerar a página após editar `dados/dados.json`:
   `python scripts/build.py`.
