# BRIEF-ALMA — Dar alma à landing page da Vitalis

Quatro adições para a página deixar de ser "bonita e abstrata" e virar "clínica de verdade".
Aplicar mantendo TUDO que já existe (imersão, modo acessível, confiança no hero), os requisitos
do Projeto 01 e o pipeline do build.py (marcadores {{...}} + dados.json). Integrar com bom gosto:
a página tinha muito espaço vazio — estas seções preenchem com propósito, sem poluir.

## 1. Equipe humana (rostos)
Os avatares em `assets/img/equipe-helena.svg`, `equipe-ivo.svg` e `equipe-clara.svg` JÁ FORAM
ATUALIZADOS para ilustrações humanas (rosto, cabelo, tom de pele, jaleco). NÃO voltar aos
círculos abstratos. Garanta que a seção Equipe os exibe bem: recorte circular, tamanho generoso
(~120–160px), com nome (H3), cargo em destaque, registro (CRM) e 1 linha de descrição.

## 2. Ação de agendar (conversão)
- **Botão flutuante de WhatsApp**, fixo no canto inferior ESQUERDO (para NÃO colidir com os botões
  "Modo acessível"/tema, que ficam à direita). Link `https://wa.me/55619XXXXXXXX` (número
  placeholder, é fictício), `aria-label="Agendar pela WhatsApp"`, ícone + rótulo curto "Agendar".
  Surge com leve fade depois de rolar ~1 tela. Entra no fluxo de teclado (focável).
- **Telefone com clique-para-ligar** (`tel:`) já em destaque na seção de contato.
- Deixar claro (microtexto) que é demonstração acadêmica.

## 3. Seção "Sua primeira consulta" (o que esperar)
Nova seção com H2 "Como é a sua primeira consulta". Três passos, cada um com um mini-ícone SVG
inline e texto curto e tranquilizador:
1. **Agende** — escolha o dia e o horário que cabem na sua rotina.
2. **Acolhimento** — recepção, escuta e avaliação sem pressa (cerca de 40 minutos).
3. **Cuidado contínuo** — um plano claro e acompanhamento próximo.
Incluir uma linha "O que trazer: um documento com foto e exames anteriores, se tiver."
Conteúdo vindo do `dados.json` (novo array `primeira_consulta`).

## 4. Seção "Nossa história" (alma)
Nova seção com H2 "Por que existimos" (ou "Nossa história"). Texto curto, humano, em primeira
pessoa do plural: por que a Vitalis nasceu e os valores — cuidar no tempo de cada paciente,
escutar antes de indicar, proximidade. 2–3 frases + 3 valores em destaque. Conteúdo do
`dados.json` (novo objeto `sobre`). Pode usar a linguagem visual existente (orbes/serifada);
nada de foto real.

## Ordem sugerida das seções
Hero → faixa de confiança → serviços → **Sua primeira consulta** → Equipe →
**Nossa história** → Depoimentos → FAQ → Contato → CTA final.

## Pipeline
Adicionar `{{PRIMEIRA_CONSULTA}}` e `{{SOBRE}}` ao template e ao build.py; incluir os dados no
`dados/dados.json`. Rodar `python scripts/build.py` ao final; garantir zero `{{...}}` restante.

## Guardrails (não perder)
Requisitos do Projeto 01 intactos; acessibilidade (foco visível, aria nos novos botões/seções,
contraste AA, prefers-reduced-motion; os botões flutuantes no fluxo de teclado); performance
(só transform/opacity; sem libs externas); responsivo 360/768/1280 sem overflow; o botão de
WhatsApp NÃO pode sobrepor o "Modo acessível".

## Aceite
As 4 adições presentes e bem integradas; avatares humanos na equipe; WhatsApp flutuante funcional
sem colisão; primeira-consulta e história vindos do JSON; build sem `{{...}}`; tudo acessível e
responsivo. Ao final, liste o que mudou.
