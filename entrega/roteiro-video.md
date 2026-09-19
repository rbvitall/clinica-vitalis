# Roteiro do vídeo de apresentação — Clínica Vitalis
**Duração máxima: 5 minutos.** Gravar a tela com narração em primeira pessoa.
Tenha aberto antes de começar: a página no GitHub Pages, o VS Code na pasta do
projeto e a aba do repositório no GitHub.

---

## 0:00 – 0:30 · Abertura e o que é o projeto

> "Oi, eu sou <SEU NOME>. Este é o Projeto 01: uma landing page para a Clínica
> Vitalis, uma clínica de saúde fictícia. É uma página estática, feita em HTML,
> CSS e JavaScript puro, sem nenhum framework, publicada no GitHub Pages.
> Além do site, escrevi dois scripts em Python que me ajudaram a construir e a
> testar a página localmente."

**Tela:** o site já aberto, no topo da página.

---

## 0:30 – 1:00 · A decisão de design

> "Antes de codar, defini uma direção de arte e escrevi ela num `clinicaLP.md`,
> para não cair no visual genérico de landing page. A direção é imersiva: a
> página tem vida já parada — essas esferas de luz ficam flutuando sozinhas — e
> ganha profundidade conforme você rola. A tipografia é Cormorant, uma serifada
> grande e leve, contra a Public Sans bem miúda, numa paleta de baixa saturação.
> São sete efeitos ao todo, e eu vou mostrando cada um."

**Tela:** rolar rapidamente o `clinicaLP.md` mostrando o bloco da direção de arte.

---

## 1:00 – 2:30 · Demonstração da página

Rolar a página devagar, narrando cada bloco:

- **Hero.** "As esferas ao fundo têm animação própria, cada uma com um tempo
  diferente, e ainda se deslocam em paralaxe quando eu rolo. O bloco de texto
  inclina em 3D conforme o mouse e vai sumindo ao sair da tela."
- **Marquee.** "Esta faixa de especialidades roda em loop infinito, só com CSS —
  a lista é duplicada para a emenda não aparecer. Ela pausa quando passo o mouse."
- **Serviços.** "Aqui está o efeito principal: a seção fica presa na tela e os
  quatro serviços avançam em profundidade, o da frente nítido e os outros
  recuados. O indicador embaixo mostra em qual eu estou. São quatro imagens com
  texto alternativo descritivo, que era o requisito, e cada uma tem sua descrição."
- **Números.** "Nesta seção escura os contadores sobem quando entram na tela, e
  o brilho do fundo se move em paralaxe."
- **Equipe.** "Três profissionais fictícios, cada um com retrato, cargo e um
  registro de conselho inventado. Os retratos são ilustrações SVG que eu mesmo
  montei — não usei foto de pessoa real."
- **Depoimentos e FAQ.** "Os depoimentos usam a serifada em itálico. O FAQ é um
  acordeão feito com `details` e `summary` nativos do HTML, então já funciona no
  teclado sem eu escrever JavaScript para isso."

**Tela:** rolagem contínua e calma. Abrir e fechar um item do FAQ.

---

## 2:30 – 3:10 · O formulário

> "Aqui está o formulário exigido: Nome, E-mail, Cidade e Estado, com as 27
> unidades federativas. Ele é totalmente estático — não envia nada para servidor
> nenhum."

Demonstrar, nesta ordem:
1. Clicar em **Enviar** com os campos vazios → aparecem as mensagens de erro.
2. Preencher corretamente e enviar → aparece a confirmação local.

> "A validação usa a API nativa do navegador, e o JavaScript só dá
> `preventDefault` e mostra a confirmação."

**Tela:** mostrar rapidamente o mobile (F12 → modo responsivo, 360 px): a
navegação vira um botão "Menu" e os painéis de serviço viram uma coluna só.

---

## 3:10 – 4:10 · O código e a organização do repositório

**Tela:** VS Code.

- `index.html` — "É o arquivo publicado, e ele é versionado. Funciona sozinho."
- `css/style.css` — "Uma folha única, comentada e dividida em dezenove seções
  numeradas. Todas as cores e tamanhos são tokens no `:root`, então a direção de
  arte fica num lugar só."
- `js/main.js` — "Comentado, dividido em blocos: tema, menu, reveal, contadores,
  formulário, e então a parte de movimento — paralaxe com inclinação 3D e a
  seção presa. Se o sistema pede movimento reduzido, o script para antes da
  parte de movimento e o CSS deixa tudo visível e estático."
- `dados/dados.json` + `templates/` + `scripts/build.py` — "Aqui está a parte de
  Python: em vez de escrever os serviços e a equipe na mão dentro do HTML, o
  conteúdo mora num JSON e o `build.py` monta o `index.html` a partir de um
  template. Rodo `python scripts/build.py` e ele avisa se sobrou algum marcador."

Rodar `python scripts/build.py` ao vivo e mostrar o resumo impresso no terminal.

---

## 4:10 – 4:40 · O site no ar

**Tela:** aba do GitHub → Settings → Pages, e depois o link publicado.

> "O repositório é público e o Pages está servindo a branch `main` a partir da
> raiz. Este é o endereço final, e é o mesmo que está no README."

---

## 4:40 – 5:00 · Fechamento

> "Resumindo: os seis requisitos estão cumpridos — título na aba, quatro imagens
> com alt, descrição de cada serviço, três membros de equipe com cargo,
> hierarquia de H1 a H3 e o formulário estático. E os sete efeitos da direção
> imersiva funcionam, sem nenhuma biblioteca externa: é tudo CSS e JavaScript
> puro. A página é responsiva, acessível pelo teclado e tem contraste AA."

---

### Checklist antes de gravar
- [ ] Fechar abas e notificações; usar tela limpa.
- [ ] Zoom do navegador em 100%.
- [ ] Testar o áudio (30 segundos de teste).
- [ ] Conferir que o link do Pages está no ar.
- [ ] Cronometrar: o corte obrigatório é em 5:00.
