# Clínica Vitalis — Landing Page

Página institucional estática de uma clínica de saúde **fictícia**, criada como
trabalho acadêmico (Projeto 01). Apresenta os serviços da clínica, a equipe,
depoimentos, perguntas frequentes e um formulário de contato **sem processamento
no servidor**.

> ⚠ Clínica, profissionais, registros (CRM/CRN) e depoimentos são inventados.
> Nenhuma pessoa real é retratada — todas as imagens são ilustrações SVG autorais.

**Site publicado:** <preencher com o link do GitHub Pages>

---

## Direção de arte

O projeto segue uma direção visual **imersiva**: a página tem vida já parada
(esferas de luz flutuando no hero) e ganha profundidade conforme se rola.
A direção está documentada em [`clinicaLP.md`](clinicaLP.md), com o brief em
[`BRIEF-IMERSIVO.md`](BRIEF-IMERSIVO.md) e a implementação de referência em
`referencia/vitalis-immersive-referencia.html`.

Tipografia: **Cormorant** (títulos, grandes e leves) + **Public Sans** (corpo).

| Token | Cor | Uso |
| --- | --- | --- |
| `--paper` | `#F6F5F0` | Fundo principal |
| `--stone` | `#EFEDE7` | Fundo alternado |
| `--ink` | `#20241D` | Texto e superfícies escuras |
| `--muted` | `#676B61` | Texto de apoio (4.6:1 mínimo) |
| `--sage` | `#7C8B6F` | Decoração (esferas, fios, ícones) |
| `--gold` | `#9C7734` | Estrelas de avaliação |
| `--olive` | `#54613F` | Texto de acento (contraste AA) |
| `--forest` | `#161C15` | Seção escura e rodapé |

No canto inferior direito ficam dois controles, ambos sem persistência em disco
(o projeto não usa `localStorage` — a escolha vale enquanto a página está aberta):

- **Modo acessível** — desliga esferas, paralaxe e o efeito 3D dos serviços, e
  reforça o contraste (tokens mais escuros, fios mais grossos, links
  sublinhados, foco de 3 px). O estado é exposto por `aria-pressed` e anunciado
  a leitores de tela. Funciona **além** de `prefers-reduced-motion`, que
  continua sendo respeitado sozinho, mesmo sem JavaScript.
- **Tema claro/escuro.**

### Seções da página

Hero → faixa de especialidades → manifesto → serviços (em profundidade) →
**Como é a sua primeira consulta** → números → equipe → **Por que existimos** →
depoimentos → perguntas frequentes → contato → chamada final.

As duas seções em negrito vêm do `dados.json` (`primeira_consulta` e `sobre`)
e existem para a página contar como é ser atendido ali, não só como ela é
bonita: três passos com ícone de linha (agendar, acolhimento de 40 minutos,
cuidado contínuo), a linha "o que trazer", e a história da clínica com três
valores.

### Agendar

Um botão flutuante de **WhatsApp** aparece no canto inferior esquerdo depois de
cerca de uma tela de rolagem — do lado oposto aos controles de exibição, para
nunca encostar neles. Enquanto está oculto usa `visibility: hidden`, então
também fica fora da ordem de tabulação: ninguém dá Tab e cai num botão que não
está na tela. O número é fictício (`wa.me/55619XXXXXXXX`) e o microtexto abaixo
avisa que é demonstração acadêmica. O telefone da seção de contato é um link
`tel:` de clique-para-ligar.

### Confiança na dobra

Logo abaixo dos botões do hero há uma linha de prova: a avaliação **4,9/5** em
estrelas desenhadas com preenchimento proporcional à nota (um gradiente que
corta em 98%), seguida de *8.400+ pacientes atendidos*, *12 anos de cuidado* e
*Equipe registrada no CRM/DF*. A nota também é escrita em texto e repetida para
leitores de tela.

### Os sete efeitos

1. **Esferas dinâmicas** no hero — três animações CSS próprias (22 s, 28 s e 19 s)
   flutuando e respirando, somadas à paralaxe de scroll e ao pulso do sol.
2. **Hero com inclinação 3D** — o bloco de texto inclina em `rotateX`/`rotateY`
   conforme o scroll e o movimento do mouse, com fade e escala ao sair.
3. **Serviços em profundidade** — seção presa (`sticky`) de 248 vh (62 vh por
   painel) onde os quatro serviços avançam em `translateZ`/`rotateX`, com
   indicador de progresso. O efeito 3D é o mesmo de antes, com menos rolagem.
4. **Contadores na seção escura** — os números sobem ao entrar na viewport,
   com o brilho de fundo em paralaxe.
5. **Reveals no scroll** — via `animation-timeline: view()`, com fallback em
   `IntersectionObserver` onde o navegador não suporta.
6. **`prefers-reduced-motion`** — desliga esferas, paralaxe, 3D e reveals;
   a seção presa vira uma lista normal e tudo fica visível e estático.
7. **Marquee de especialidades** — faixa em loop infinito por CSS, que pausa ao
   passar o mouse e some sob movimento reduzido.

## Tecnologias

- **HTML5** semântico (um único `<h1>`, `<details>` nativo no FAQ).
- **CSS3** puro — tokens em `:root`, sem framework. Só `transform` e `opacity`
  são animados, com `will-change` nos elementos que o JS toca a cada quadro.
- **JavaScript** puro (ES5+), sem bibliotecas e sem `localStorage`.
- **Python 3** (biblioteca padrão) apenas como apoio de desenvolvimento.
- **Google Fonts** (Cormorant + Public Sans) — único recurso externo.

O site publicado **não depende de Python**: o `index.html` é versionado e
funciona sozinho.

---

## Como executar

### 1. Jeito mais simples
Abra o arquivo `index.html` com duplo clique. Tudo funciona, inclusive o
formulário — os caminhos são relativos.

### 2. Com servidor local (recomendado)
```bash
python scripts/serve.py
# abre http://localhost:8000 no navegador
# outra porta: python scripts/serve.py 8080
# encerrar: Ctrl+C
```

### 3. Regerar o `index.html`
Depois de editar `dados/dados.json` ou `templates/index.template.html`:
```bash
python scripts/build.py
```
O script imprime um resumo e falha se sobrar algum marcador `{{...}}`.

---

## Publicando no GitHub Pages

1. Crie um repositório **público** no GitHub (sem README, sem .gitignore).
2. Rode a sequência de comandos git da seção abaixo.
3. No repositório: **Settings → Pages**.
4. Em *Build and deployment* → *Source*, escolha **Deploy from a branch**.
5. Selecione a branch **`main`** e a pasta **`/ (root)`**. Clique em **Save**.
6. Aguarde cerca de 1 minuto. O link aparece no topo da mesma página, no formato
   `https://<SEU-USUARIO>.github.io/<NOME-DO-REPO>/`.
7. Cole esse link no topo deste README e no PDF de entrega.

---

## Estrutura de pastas

```
clinica-vitalis/
├── index.html                    # página publicada (gerada, versionada)
├── clinicaLP.md                     # direção de arte e regras do projeto
├── README.md
├── .gitignore
├── css/
│   └── style.css                 # folha única, comentada por seções
├── js/
│   └── main.js                   # tema, menu, reveal, contadores,
│                                 # paralaxe 3D, seção presa, formulário
├── assets/img/                   # 7 ilustrações SVG + favicon
│   ├── servico-*.svg             # 4 imagens de serviços
│   └── equipe-*.svg              # 3 retratos humanos ilustrados (240x240,
│                                 # já recortados em círculo)
├── BRIEF-IMERSIVO.md             # brief da direção imersiva
├── referencia/                   # implementação de referência (consulta)
├── dados/
│   └── dados.json                # todo o conteúdo do site
├── templates/
│   └── index.template.html       # template com marcadores {{...}}
└── scripts/
    ├── build.py                  # dados.json + template -> index.html
    └── serve.py                  # servidor local (http.server)
```

---

## Checklist dos requisitos

| # | Requisito | Onde está |
| --- | --- | --- |
| 1 | `<title>` na aba | `<head>` — "Clínica Vitalis — Cuidar é presença" |
| 2 | ≥ 2 imagens de serviços com `alt` | 4 imagens nos painéis de **Serviços** (7 `<img>` no total, todas com `alt`) |
| 3 | Descrição de cada serviço | Seção **Serviços**, um parágrafo por item |
| 4 | Equipe ≥ 3 membros com foto e cargo | Seção **Equipe** — 3 profissionais com retrato circular de 140 px, cargo e registro |
| 5 | H1 + H2 + H3 | 1 `<h1>`, 10 `<h2>`, 7 `<h3>` |
| 6 | Formulário Nome / E-mail / Cidade / Estado, sem envio | Seção **Contato** — validação no navegador, `preventDefault()` |

### Qualidade adicional

- Acessibilidade: link "pular para o conteúdo", foco de teclado visível,
  `aria-expanded` no menu, acordeão nativo, contraste WCAG AA.
- Responsivo de 360 px a 1440 px+, sem rolagem horizontal; no mobile a
  navegação vira um painel com `aria-expanded` e os painéis viram uma coluna.
- `prefers-reduced-motion` respeitado em todas as animações.
- Página legível mesmo com JavaScript desativado (`<noscript>`).
- Sem bibliotecas externas, sem `iframe`, sem `localStorage`.
- Contraste conferido em três modos (normal, modo acessível e tema escuro):
  nenhum texto abaixo de 4,5:1; o pior caso mede 4,66:1.
- SEO: `<title>` descritivo, `meta description`, Open Graph e favicon SVG.

### Decisões de performance

A barra fixa usava `mix-blend-mode: difference`, que obriga o navegador a
recompor tudo o que passa por baixo dela a cada quadro. Foi trocada por uma
faixa translúcida sólida com `backdrop-filter` — o contraste do texto passou a
ser o mesmo em toda a página e a rolagem ficou barata. Além disso:

- As esferas do hero encolheram (52 vw → 38 vw) e o desfoque caiu de 8 px para
  4 px, porque o gradiente agora morre em transparente na borda e dispensa o
  resto do blur.
- `will-change` só nos elementos que realmente animam (saiu do `.tcard`, que
  não animava) e `contain: paint` nas quatro seções animadas.
- Um único listener de `scroll` para a página inteira, com um `requestAnimationFrame`
  por quadro; o hero para de receber `transform` assim que sai da viewport, e as
  animações CSS pausam quando a seção não está à vista.

---

## Licença e créditos

Trabalho acadêmico, sem fins comerciais. Ilustrações SVG criadas para este
projeto. Fontes Cormorant e Public Sans sob SIL Open Font License.
