# BRIEF PROFISSIONAL — Elevar a LP Vitalis ao melhor nível

Aplique o método do manifesto "Clínica Viva": **imersão a serviço da calma, da confiança e
da acessibilidade**. O objetivo é uma landing page 100% profissional que mantenha TODOS os
requisitos do Projeto 01 e maximize os critérios de nota. Trabalhe sobre o que já existe
(templates/index.template.html, css/style.css, js/main.js) mantendo o pipeline do build.py.

## Princípios (do manifesto)
1. Movimento que respira — nada de rolagem sequestrada; efeito só onde importa.
2. Confiança na dobra — prova perto do primeiro CTA.
3. Quebre o azul — manter a paleta pedra/sálvia (já distinta); reforçar consistência.
4. Demonstre, não prometa — números reais e um passo do atendimento à mostra.
5. Acessibilidade como recurso — visível, não escondida.
6. Um momento de encanto, não dez — o resto rápido e quieto.

## Mudanças estruturais (aplicar todas)
1. **Confiança na dobra**: adicionar uma linha de prova NO HERO — avaliação "4,9/5" com estrelas
   (SVG, cor --gold/ocre), "8.400+ pacientes", "12 anos de cuidado" e um selo "Equipe registrada".
   Compacta, logo abaixo dos botões. (Referência: DrDoctor com Trustpilot no hero.)
2. **Encurtar a seção pinned dos serviços**: de ~420vh para ~250vh. Manter o efeito 3D de
   profundidade, porém mais ágil (menos scroll por painel). Os 4 serviços devem passar sem cansar.
3. **Performance (crítico para os 10 pontos de "sem erros")**:
   - Reduzir o orb gigante do hero (diminuir tamanho e/ou blur) para baixar o custo de composição.
   - REMOVER `mix-blend-mode: difference` da barra fixa; trocar por fundo translúcido sólido
     (ex.: rgba do --paper) com contraste garantido do texto/links em qualquer seção.
   - `will-change` só nos elementos realmente animados; parar de escrever transforms do hero
     quando ele sai da viewport; `contain: paint` nas seções animadas.
   - Meta: rolagem fluida (60fps) em máquina modesta e em scroll rápido.
4. **Acessibilidade como recurso**: além de respeitar `prefers-reduced-motion` automaticamente,
   adicionar um **botão visível "Modo acessível"** que (a) desliga orbs/paralaxe/3D e (b) aumenta
   contraste. Persistir a escolha na sessão (variável em memória; sem localStorage no preview).
   Foco de teclado visível em tudo; navegação por teclado no menu, acordeão e formulário; AA.

## Polimento profissional (checklist)
- **Copy**: textos curtos, humanos, sem jargão; UM CTA primário ("Agendar consulta") repetido nos
  pontos-chave; microcopy honesta no formulário ("demonstração — nada é enviado").
- **Tipografia/ritmo**: escala de tipo consistente; `text-wrap:balance` nos títulos; leitura ~65ch;
  espaçamento por escala (8/12/16/24/32/48/64), sem margens soltas.
- **Hierarquia**: um único H1; H2 nas seções; H3 em serviços/equipe. Nada de salto de nível.
- **Trust/conteúdo**: depoimentos com nome + cidade + estrelas; FAQ útil (planos, horários,
  primeira consulta, contato) em acordeão acessível.
- **Formulário**: labels associadas (for/id), validação no navegador, mensagens de erro úteis por
  campo, estado de foco, confirmação local. Campos: Nome, E-mail, Cidade, Estado (27 UFs).
- **SEO/meta**: `<title>` descritivo, `<meta name="description">`, `lang="pt-BR"`, Open Graph
  básico (og:title, og:description), favicon SVG.
- **Imagens**: todos os SVG com `alt` descritivo; otimizados; ≥2 imagens de serviços.
- **Performance**: animar só `transform`/`opacity`; sem bibliotecas externas (JS puro); se usar
  qualquer lib, só via CDN e com justificativa. Alvo Lighthouse ≥ 90 em Performance,
  Acessibilidade, Práticas recomendadas e SEO.
- **Responsivo**: testar 360 / 768 / 1280 px — sem overflow horizontal; menu hambúrguer, marquee
  e seção pinned funcionando no mobile.
- **Robustez**: caminhos relativos (funciona em subpasta do GitHub Pages) e abrindo index.html direto.

## Requisitos obrigatórios do Projeto 01 (NÃO perder nenhum)
`<title>` na aba · ≥2 imagens de serviços com alt · descrição de cada serviço ·
equipe fictícia 3x (avatar + cargo + registro fictício) · H1/H2/H3 ·
formulário estático Nome/E-mail/Cidade/Estado sem envio a servidor.

## Pipeline (manter)
Seções dinâmicas via dados/dados.json + build.py (marcadores {{...}}). Portar CSS para
css/style.css e JS para js/main.js (comentado). Rodar `python scripts/build.py` ao final e
garantir que não sobra nenhum {{...}}. Atualizar README se algo mudar na execução.

## Aceite (pronto quando)
- Prova de confiança visível no hero; pinned ~250vh e ágil; sem `mix-blend-mode` na barra.
- Botão "Modo acessível" funcionando + prefers-reduced-motion respeitado; foco visível; AA.
- Todos os requisitos obrigatórios presentes; build sem {{...}}; sem overflow em 360/768/1280.
- Rolagem fluida em scroll rápido; a página "sente viva" parada e ganha profundidade ao rolar,
  sem cara de template — e sem engasgar.
Ao final, liste o que mudou e rode um autoteste do checklist acima.
