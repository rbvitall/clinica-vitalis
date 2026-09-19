# BRIEF IMERSIVO — Clínica Vitalis (para o Claude Code integrar)

Este documento é a direção de arte a ser aplicada na landing page real do projeto.
Existe um arquivo de referência PRONTO e funcional em `referencia/vitalis-immersive-referencia.html`
(single-file, testado). Sua tarefa é **portar as técnicas dele para o projeto real**
(templates/index.template.html + css/style.css + js/main.js), mantendo o pipeline do
build.py (marcadores {{...}} → dados.json) e TODOS os requisitos obrigatórios do Projeto 01.

## Regra de ouro
Não recriar do zero nem "interpretar": abra o arquivo de referência, entenda cada efeito e
reproduza-o no projeto real com o MESMO comportamento. Se algo divergir, o de referência vence.

## Direção de arte (Imersiva / Wellness em movimento)
Paleta e tipografia estão no topo do arquivo de referência (:root). Cormorant (títulos) +
Public Sans (corpo). Paleta pedra/sálvia/oliva + seção escura #161C15. Manter exatamente.

## Efeitos a portar (todos já implementados na referência)
1. **Bolas (orbs) dinâmicas** no hero: cada uma com animação CSS própria (float1/float2/float3,
   22s/28s/19s), flutuando e "respirando" (scale) continuamente — NÃO estáticas. Somadas à
   paralaxe de scroll (data-speed) e ao pulso do sol (sunpulse).
2. **Hero com inclinação 3D**: o bloco de texto (#plate) inclina em rotateX/rotateY conforme
   scroll e movimento do mouse, com fade/scale ao sair (JS rAF).
3. **Serviços "pinned" em profundidade**: seção sticky de ~420vh onde os 4 serviços avançam em
   3D (translateZ/rotateX), o da frente nítido e os outros recuados/apagados, com indicador de
   progresso (JS pin()).
4. **Seção escura com contadores**: números sobem (data-count) ao entrar na viewport + brilho
   em paralaxe.
5. **Reveals no scroll**: elementos .reveal sobem com rotateX via animation-timeline:view(),
   com fallback IntersectionObserver quando não suportado (nunca deixar preso em opacity:0).
6. **Respeitar prefers-reduced-motion**: desliga orbs, paralaxe, 3D e reveals; mostra tudo
   estático e visível.

## Efeito NOVO a acrescentar (referência das LPs reais que estudei)
7. **Marquee de sintomas/serviços** (inspirado na One Medical): uma faixa fina que rola
   continuamente com termos como "check-up · nutrição · exames · vacinas · saúde da mulher ·
   acompanhamento · ...", em loop infinito por CSS (translateX), pausando no hover. Colocar
   logo após o hero, antes dos serviços. Duplicar a lista para loop sem emenda; aria-hidden na
   cópia. Desligar animação sob prefers-reduced-motion.

## Requisitos obrigatórios do Projeto 01 (NÃO perder nenhum ao redesenhar)
- <title> na aba.
- >= 2 imagens de serviços com alt (os SVGs contam; manter alt descritivo).
- Descrição de cada serviço.
- Equipe fictícia: 3 membros com avatar + cargo (+ registro CRM fictício).
- H1 (uma vez) + H2 + H3, hierarquia real.
- Formulário estático: Nome, E-mail, Cidade, Estado (select 27 UFs), SEM envio a servidor;
  JS previne o submit, valida no navegador e mostra confirmação local.
- FAQ em acordeão acessível (<details>/<summary>), depoimentos com estrelas, contato com
  clique-para-ligar (tel:), e-mail (mailto) e placeholder de mapa (sem iframe externo).

## Pipeline (manter)
- As seções dinâmicas (serviços, equipe, depoimentos, faq, métricas, dados da clínica) vêm do
  dados/dados.json via build.py, substituindo {{...}} em templates/index.template.html.
- Portar o CSS da referência para css/style.css e o JS para js/main.js (comentado).
- Rodar `python scripts/build.py` ao final; garantir que não sobra nenhum {{...}} e que o site
  funciona abrindo index.html direto e via GitHub Pages (caminhos relativos).

## Qualidade
Performance: só transform/opacity, will-change nos elementos animados. Foco de teclado visível.
Contraste AA. Sem libs externas. Testar em 360/768/1280px sem overflow horizontal.

## Aceite
Pronto quando: os 7 efeitos funcionam, todos os requisitos obrigatórios presentes, build sem
{{...}} restante, e a página "sente viva" já parada (orbs em movimento) e ganha profundidade ao
rolar — sem cara de template genérico.
