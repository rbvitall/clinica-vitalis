# Projeto: Landing Page — Clínica Vitalis (trabalho acadêmico)

## Objetivo
Página estática (Projeto 01) que apresenta uma clínica de saúde FICTÍCIA
("Clínica Vitalis"), seus serviços e sua equipe, com formulário de contato SEM
processamento no servidor. Deve rodar no GitHub Pages e valer nota máxima.

## Stack (obrigatória)
- Site: HTML5 + CSS3 + JavaScript puro (sem framework, sem build no deploy).
- Python 3 de apoio (o site funciona sem ele):
  - scripts/serve.py  -> servidor local (http.server).
  - scripts/build.py   -> gera index.html a partir de dados/dados.json + templates/.
- index.html versionado, funciona sozinho no GitHub Pages.

## Requisitos obrigatórios (checar TODOS)
1. <title> na aba.
2. >= 2 imagens de serviços (usaremos 4), todas com alt descritivo.
3. Descrição de cada serviço.
4. Equipe fictícia: >= 3 membros, cada um com foto/avatar + cargo.
5. H1 + H2 + H3 (2+ níveis de cabeçalho, hierarquia real).
6. Formulário estático: Nome, E-mail, Cidade, Estado — sem enviar a servidor.

## Critérios de nota (otimizar)
Funcionamento sem erros (10) · GitHub (5) · Instruções (2) · Apresentação (8) ·
Extra: GitHub Pages (+5).

## Direção de arte: IMERSIVA (Wellness em movimento)
Fonte da verdade: `BRIEF-IMERSIVO.md` + `referencia/vitalis-immersive-referencia.html`.
Se algo divergir, a referência vence.
Conceito: bem-estar premium COM profundidade e movimento. A página "sente viva" já
parada (orbs flutuando) e ganha camadas de profundidade ao rolar.
Paleta (CSS :root):
  --stone:#EFEDE7; --paper:#F6F5F0; --hi:#FBFAF6; --ink:#20241D; --muted:#6E7268;
  --sage:#7C8B6F; --olive:#54613F; --forest:#161C15; --gold:#B18A4E; --line:#DAD7CC;
  (+ variante `:root[data-theme="dark"]` para o alternador de tema)
Tipografia (Google Fonts):
  - Títulos: "Cormorant", peso 500, TAMANHO GRANDE e leve.
  - Corpo/UI: "Public Sans", pesos 400-600.
Acessibilidade da paleta: texto miúdo de acento usa --olive (6:1), nunca --sage (3.3:1).

Os 7 efeitos obrigatórios:
  1. Orbs animados no hero (float1/float2/float3, 22s/28s/19s) + paralaxe data-speed + sunpulse.
  2. Hero com inclinação 3D (#plate) por scroll e mouse, com fade/scale ao sair.
  3. Serviços "pinned": seção sticky de 105vh por painel, avanço em translateZ/rotateX
     com indicador de progresso.
  4. Seção escura com contadores data-count + brilho em paralaxe.
  5. Reveals via animation-timeline:view(), com fallback IntersectionObserver.
  6. prefers-reduced-motion desliga orbs, paralaxe, 3D e reveals — tudo visível e estático.
  7. Marquee de sintomas/serviços em loop infinito por CSS, pausando no hover.

PROIBIDO aqui: cores saturadas fora da paleta; fontes Inter ou Space Grotesk; emoji como
marcador de seção; animar propriedades que não sejam transform/opacity; bibliotecas externas.

## Nota sobre a regra anterior
A direção Wellness Luxe estática (sem hero de 100vh, sem sombras) foi SUBSTITUÍDA por esta.
O hero de 100svh e as sombras dos painéis agora são intencionais e vêm da referência.

## Qualidade
HTML semântico (um único H1); CSS organizado, comentado, por seções, tokens em :root;
JS comentado; foco de teclado visível; validação de formulário no navegador;
imagens leves com alt; nada de foto de pessoa real (avatar/ilustração fictícia ou
imagem de licença livre); caminhos relativos; sem libs externas; sem localStorage.
Mobile-first; contraste WCAG AA; respeitar prefers-reduced-motion.
