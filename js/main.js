/* =====================================================================
   Clínica Vitalis — comportamento da página
   JavaScript puro, sem bibliotecas e sem localStorage.

   Blocos:
      1 estado (movimento / modo acessível) ·  2 tema
      3 modo acessível ·  4 menu ·  5 barra + WhatsApp ·  6 reveal (fallback)
      7 contadores ·  8 ano ·  9 formulário
     10 pausar fora da tela · 11 paralaxe + hero 3D · 12 serviços em profundidade

   O movimento tem DOIS interruptores: a preferência do sistema
   (prefers-reduced-motion) e o botão "Modo acessível". Os dois marcam
   data-mov="off" na raiz; o CSS reage a isso e o JS para de escrever
   transform. Conteúdo e interação (blocos 2 a 9) nunca dependem disso.
   ===================================================================== */
(function () {
  'use strict';

  var raiz = document.documentElement;

  /* ------------------------ 1. ESTADO ------------------------------ */
  var prefereParado = matchMedia('(prefers-reduced-motion: reduce)');

  // Memória apenas de sessão: uma variável. Sem localStorage, por regra
  // do projeto — a escolha vale enquanto a página estiver aberta.
  var modoAcessivel = false;
  var movimento = false;

  var camadas = [].slice.call(document.querySelectorAll('[data-speed]'));
  var plate = document.getElementById('plate');
  var wrap = document.querySelector('.pin-wrap');
  var panels = [].slice.call(document.querySelectorAll('.panel'));
  var dots = [].slice.call(document.querySelectorAll('.progress i'));
  var N = panels.length;
  var mx = 0, my = 0;

  /* ------------------------- 2. TEMA ------------------------------- */
  var botaoTema = document.getElementById('tg');
  if (botaoTema) {
    botaoTema.addEventListener('click', function () {
      var escuro = raiz.getAttribute('data-theme') === 'dark';
      raiz.setAttribute('data-theme', escuro ? 'light' : 'dark');
      botaoTema.setAttribute('aria-pressed', String(!escuro));
    });
  }

  /* -------------------- 3. MODO ACESSÍVEL -------------------------- */
  /* Desliga o movimento e reforça o contraste. Fica à vista, com rótulo
     escrito, porque acessibilidade aqui é recurso, não ajuste escondido. */
  var botaoA11y = document.getElementById('modo-acessivel');
  var aviso = document.getElementById('a11y-aviso');

  function aplicarMovimento() {
    movimento = !prefereParado.matches && !modoAcessivel;
    raiz.setAttribute('data-mov', movimento ? 'on' : 'off');

    if (movimento) {
      // volta a posicionar tudo de acordo com a rolagem atual
      quadro();
      pin();
    }
    // Quando desliga não é preciso limpar nada: as regras do bloco 19 do
    // CSS usam !important e vencem os estilos inline que o JS escreveu.
  }

  if (botaoA11y) {
    botaoA11y.addEventListener('click', function () {
      modoAcessivel = !modoAcessivel;
      raiz.setAttribute('data-a11y', modoAcessivel ? 'on' : 'off');
      botaoA11y.setAttribute('aria-pressed', String(modoAcessivel));
      aplicarMovimento();
      if (aviso) {
        aviso.textContent = modoAcessivel
          ? 'Modo acessível ligado: animações desligadas e contraste reforçado.'
          : 'Modo acessível desligado.';
      }
    });
  }

  // Se a pessoa mudar a preferência do sistema com a página aberta
  prefereParado.addEventListener('change', aplicarMovimento);

  /* -------------------------- 4. MENU ------------------------------ */
  var barra = document.querySelector('.bar');
  var botaoMenu = document.querySelector('.bar-menu');

  function fecharMenu() {
    if (!barra || !botaoMenu) return;
    barra.classList.remove('aberto');
    botaoMenu.setAttribute('aria-expanded', 'false');
    botaoMenu.textContent = 'Menu';
  }

  if (barra && botaoMenu) {
    botaoMenu.addEventListener('click', function () {
      var aberto = barra.classList.toggle('aberto');
      botaoMenu.setAttribute('aria-expanded', String(aberto));
      botaoMenu.textContent = aberto ? 'Fechar' : 'Menu';
    });

    barra.addEventListener('click', function (e) {
      if (e.target.closest('nav a')) fecharMenu();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && barra.classList.contains('aberto')) {
        fecharMenu();
        botaoMenu.focus();
      }
    });

    matchMedia('(min-width: 721px)').addEventListener('change', fecharMenu);
  }

  /* -------------------------- 5. BARRA ----------------------------- */
  /* Ganha um fio embaixo só depois que a página sai do topo. */
  function barraRolada() {
    if (barra) barra.classList.toggle('rolada', window.scrollY > 12);
  }

  /* ---------------------- 5b. BOTÃO WHATSAPP ----------------------- */
  /* Surge depois de cerca de uma tela de rolagem. Enquanto escondido o
     CSS usa visibility:hidden, então ele também fica fora do tab order —
     ninguém dá Tab e cai num botão que não está na tela. */
  var wa = document.querySelector('.wa');

  function whatsappVisivel() {
    if (wa) wa.classList.toggle('visivel', window.scrollY > innerHeight * 0.9);
  }

  /* ------------------- 6. REVEAL (fallback do CSS) ------------------ */
  /* Onde animation-timeline:view() existe, o CSS resolve sozinho. Onde
     não existe, o observer marca .seen — nada fica preso em opacity:0. */
  if (!window.CSS || !CSS.supports('animation-timeline', 'view()')) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add('seen');
          io.unobserve(e.target);
        });
      }, { rootMargin: '0px 0px -12% 0px' });
      document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
    } else {
      document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('seen'); });
    }
  }

  /* ------------------------ 7. CONTADORES -------------------------- */
  function formatar(valor, div, sufixo) {
    var texto = div > 1
      ? (valor / div).toFixed(1).replace('.', ',')
      : valor.toLocaleString('pt-BR');
    return texto + sufixo;
  }

  var numeros = [].slice.call(document.querySelectorAll('[data-count]'));

  function escreverFinal(el) {
    el.textContent = formatar(+el.dataset.count, +el.dataset.div || 1, el.dataset.suffix || '');
  }

  if (prefereParado.matches || !('IntersectionObserver' in window)) {
    // sem animação: o número final aparece de uma vez, nunca um "0" na tela
    numeros.forEach(escreverFinal);
  } else {
    var contados = new WeakSet();
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting || contados.has(e.target)) return;
        contados.add(e.target);

        var el = e.target;
        if (!movimento) { escreverFinal(el); return; }

        var fim = +el.dataset.count,
            div = +el.dataset.div || 1,
            sufixo = el.dataset.suffix || '',
            t0 = null;

        function passo(t) {
          if (!movimento) { escreverFinal(el); return; }
          if (!t0) t0 = t;
          var p = Math.min((t - t0) / 1100, 1);
          // o sufixo só entra no fim, para o número não "piscar" com ele
          el.textContent = formatar(Math.floor(p * fim), div, p === 1 ? sufixo : '');
          if (p < 1) requestAnimationFrame(passo);
        }
        requestAnimationFrame(passo);
      });
    }, { threshold: .6 });
    numeros.forEach(function (el) { cio.observe(el); });
  }

  /* ---------------------------- 8. ANO ----------------------------- */
  var ano = document.getElementById('ano');
  if (ano) ano.textContent = String(new Date().getFullYear());

  /* ------------------------ 9. FORMULÁRIO -------------------------- */
  /* Estático por exigência do projeto: valida no navegador, confirma
     localmente e nunca envia nada a servidor algum. */
  var form = document.getElementById('form-contato');
  var confirmacao = document.getElementById('form-confirmacao');

  if (form && confirmacao) {
    var campos = ['nome', 'email', 'cidade', 'estado'];

    function marcarErro(id, visivel) {
      var entrada = document.getElementById(id);
      var erro = form.querySelector('[data-erro="' + id + '"]');
      if (!entrada || !erro) return;
      erro.hidden = !visivel;
      entrada.closest('.campo').classList.toggle('campo--invalido', visivel);
      entrada.setAttribute('aria-invalid', String(visivel));
    }

    campos.forEach(function (id) {
      var entrada = document.getElementById(id);
      if (!entrada) return;
      entrada.addEventListener('input', function () {
        if (entrada.checkValidity()) marcarErro(id, false);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault(); // nada sai desta página

      var primeiroInvalido = null;

      campos.forEach(function (id) {
        var entrada = document.getElementById(id);
        if (!entrada) return;
        var valido = entrada.checkValidity();
        marcarErro(id, !valido);
        if (!valido && !primeiroInvalido) primeiroInvalido = entrada;
      });

      if (primeiroInvalido) {
        confirmacao.hidden = true;
        primeiroInvalido.focus();
        return;
      }

      var nome = document.getElementById('nome').value.trim().split(' ')[0];
      confirmacao.textContent = nome + ', recebemos seu pedido de contato. ' +
        'Retornamos em até um dia útil. (Demonstração acadêmica: nenhum dado foi enviado.)';
      confirmacao.hidden = false;
      form.reset();
      confirmacao.focus();
    });
  }

  /* ---------------- 10. PAUSAR ANIMAÇÕES FORA DA TELA -------------- */
  /* Uma animação CSS continua rodando com o elemento fora da viewport.
     Pausamos o que não está à vista: na tela o resultado é idêntico. */
  if ('IntersectionObserver' in window) {
    var pausar = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle('parado', !e.isIntersecting); });
    }, { rootMargin: '10% 0px' });

    ['.hero', '.marquee'].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (el) pausar.observe(el);
    });
  }

  /* -------------- 11. PARALAXE + INCLINAÇÃO 3D DO HERO ------------- */
  var brilho = document.querySelector('.glow');
  var heroAtivo = true;

  function quadro() {
    if (!movimento) return;

    var y = window.scrollY, vh = innerHeight;
    var noHero = y < vh * 1.5;

    // Os orbs são grandes: depois que o hero sai de cena não há o que
    // mostrar, então paramos de escrever transform nessas camadas.
    if (noHero || heroAtivo) {
      camadas.forEach(function (el) {
        if (!noHero && el !== brilho) return;
        el.style.transform = 'translate3d(0,' + (y * +el.dataset.speed) + 'px,0)';
      });
      heroAtivo = noHero;
    } else if (brilho) {
      brilho.style.transform = 'translate3d(0,' + (y * +brilho.dataset.speed) + 'px,0)';
    }

    // o bloco do hero inclina ao rolar e conforme o mouse, e some
    if (plate && y < vh * 1.2) {
      var hp = Math.min(y / vh, 1);
      plate.style.transform =
        'translateY(' + (y * 0.18) + 'px) ' +
        'rotateX(' + (hp * 8 + my * -5) + 'deg) ' +
        'rotateY(' + (mx * 7) + 'deg) ' +
        'scale(' + (1 - hp * 0.08) + ')';
      plate.style.opacity = String(1 - hp * 0.9);
      plate.style.pointerEvents = hp > 0.9 ? 'none' : '';
    }
  }

  /* ------------- 12. SERVIÇOS EM PROFUNDIDADE (pin) ---------------- */
  /* A seção tem 62vh de rolagem por painel (248vh no total). O .pin fica
     preso e os painéis avançam em Z: o da frente nítido, os outros
     recuados e apagados. */
  function pin() {
    if (!movimento || !wrap || !N) return;

    var r = wrap.getBoundingClientRect();
    var total = wrap.offsetHeight - innerHeight;
    if (total <= 0) return;

    var prog = Math.min(Math.max(-r.top / total, 0), 1); // 0..1 no trecho preso
    var pos = prog * (N - 1);                            // índice fracionário

    panels.forEach(function (p, i) {
      var d = i - pos;            // distância até o painel ativo
      var abs = Math.abs(d);
      var op = abs > 1.15 ? 0 : 1 - abs * 0.5;

      p.style.transform = 'translate3d(0,' + (d * 90) + 'px,' + (-abs * 260) + 'px) ' +
                          'rotateX(' + (d * -16) + 'deg)';
      p.style.opacity = String(Math.max(op, 0));
      p.style.zIndex = String(100 - Math.round(abs * 10));
      // painel apagado não recebe clique nem foco de mouse
      p.style.pointerEvents = op <= 0 ? 'none' : '';
    });

    var ativo = Math.round(pos);
    dots.forEach(function (d, i) { d.classList.toggle('on', i === ativo); });
  }

  /* --------------------- LAÇO ÚNICO DE ROLAGEM --------------------- */
  /* Um só listener de scroll para tudo, com um rAF por quadro. */
  var pendente = false;

  addEventListener('scroll', function () {
    if (pendente) return;
    pendente = true;
    requestAnimationFrame(function () {
      barraRolada();
      whatsappVisivel();
      quadro();
      pin();
      pendente = false;
    });
  }, { passive: true });

  addEventListener('pointermove', function (e) {
    if (!movimento || window.scrollY >= innerHeight) return;
    mx = (e.clientX / innerWidth - .5);
    my = (e.clientY / innerHeight - .5);
    quadro();
  }, { passive: true });

  addEventListener('resize', function () { quadro(); pin(); });

  // estado inicial
  aplicarMovimento();
  barraRolada();
  whatsappVisivel();
})();

/* ---- Parallax sutil da faixa full-bleed (respeita movimento reduzido) ---- */
(function(){
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var media = document.querySelector('.photo-band__media');
  if (!media) return;
  var sec = media.closest('.photo-band'), ticking = false;
  function upd(){
    var root = document.documentElement.getAttribute('data-mov');
    if (root === 'off') { media.style.transform = ''; ticking = false; return; }
    var r = sec.getBoundingClientRect(), vh = window.innerHeight;
    var prog = (r.top + r.height/2 - vh/2) / (vh/2 + r.height/2);
    prog = Math.max(-1, Math.min(1, prog));
    media.style.transform = 'translateY(' + (prog * 42) + 'px)';
    ticking = false;
  }
  function onScroll(){ if(!ticking){ ticking = true; requestAnimationFrame(upd); } }
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', onScroll);
  upd();
})();
