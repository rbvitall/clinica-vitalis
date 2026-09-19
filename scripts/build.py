#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gerador estático da landing page da Clínica Vitalis.

Lê ``dados/dados.json`` e ``templates/index.template.html``, monta o HTML das
seções dinâmicas (marquee, serviços em profundidade, métricas, selos, equipe,
depoimentos, FAQ e UFs) e escreve ``index.html`` na raiz do projeto.

Usa apenas a biblioteca padrão — nada para instalar.

Uso:
    python scripts/build.py

O site publicado NÃO depende deste script: o ``index.html`` gerado é
versionado e funciona sozinho no GitHub Pages.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from html import escape
from pathlib import Path

# --------------------------------------------------------------------------
# Caminhos (sempre relativos à raiz do projeto, um nível acima de scripts/)
# --------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent
ARQUIVO_DADOS = RAIZ / "dados" / "dados.json"
ARQUIVO_TEMPLATE = RAIZ / "templates" / "index.template.html"
ARQUIVO_SAIDA = RAIZ / "index.html"

# Quantos viewports de rolagem cada painel de serviço ocupa na seção presa.
# 4 serviços x 62vh = 248vh. Era 105 (420vh): o efeito 3D continua igual,
# mas cada painel exige menos rolagem — a seção passa sem cansar.
VH_POR_PAINEL = 62

# Ícones SVG inline — sem biblioteca externa, sem emoji como marcador.
ICONE_SELO = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M3 8.5l3.2 3.2L13 5" fill="none" stroke="currentColor" '
    'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

ESTRELA = (
    '<svg viewBox="0 0 16 16"{extra} aria-hidden="true" focusable="false">'
    '<path d="M8 1l2 4.6 5 .5-3.8 3.3 1.1 4.9L8 11.7 3.7 14.3l1.1-4.9L1 6.1l5-.5z" '
    'fill="currentColor"/></svg>'
)


def estrelas_proporcionais(nota: float, id_gradiente: str) -> str:
    """Cinco estrelas com preenchimento proporcional à nota (ex.: 4,9 de 5).

    Desenha as estrelas duas vezes: a camada de baixo apagada e, por cima, a
    mesma forma pintada por um gradiente que corta exatamente na fração da
    nota. É assim que 4,9/5 aparece como quatro estrelas e quase uma.
    """
    passo, largura = 18, 90
    formas = "".join(
        f'<path transform="translate({i * passo},0)" '
        'd="M8 1l2 4.6 5 .5-3.8 3.3 1.1 4.9L8 11.7 3.7 14.3l1.1-4.9L1 6.1l5-.5z"/>'
        for i in range(5)
    )
    corte = max(0.0, min(nota / 5, 1.0)) * 100
    return (
        f'<svg class="prova__estrelas" viewBox="0 0 {largura} 16" '
        'role="img" aria-hidden="true" focusable="false">'
        "<defs>"
        f'<linearGradient id="{id_gradiente}" x1="0" x2="1" y1="0" y2="0">'
        f'<stop offset="{corte:.4g}%" stop-color="currentColor"/>'
        f'<stop offset="{corte:.4g}%" stop-color="transparent"/>'
        "</linearGradient>"
        "</defs>"
        f'<g class="prova__estrelas-vazias">{formas}</g>'
        f'<g fill="url(#{id_gradiente})">{formas}</g>'
        "</svg>"
    )


def montar_prova(prova: dict) -> str:
    """Linha de confiança do hero, logo abaixo dos botões.

    Traz a nota com estrelas e os três fatos que o visitante precisa ver
    antes de decidir: volume, tempo de casa e registro profissional.
    """
    itens = "".join(
        f'<li class="prova__item">{escape(item)}</li>' for item in prova["itens"]
    )
    rotulo = f'{prova["nota_texto"]} — {prova["nota_rotulo"]}'
    return (
        '<div class="prova">\n'
        f'  <p class="prova__nota">\n'
        f'    {estrelas_proporcionais(float(prova["nota"]), "nota-hero")}\n'
        f'    <strong>{escape(prova["nota_texto"])}</strong>\n'
        f'    <span class="prova__rotulo">{escape(prova["nota_rotulo"])}</span>\n'
        f'    <span class="sr-so">{escape(rotulo)}</span>\n'
        "  </p>\n"
        f'  <ul class="prova__lista">{itens}</ul>\n'
        "</div>"
    )


# Mini-ícones de linha dos passos da primeira consulta. Traço fino, mesma
# malha de 24x24, sem emoji e sem biblioteca externa.
ICONES_PASSO = {
    "calendario": (
        '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/>'
        '<path d="M3.5 9.5h17M8 3v4M16 3v4"/>'
        '<path d="M8 14h3"/>'
    ),
    "escuta": (
        '<path d="M6 10a6 6 0 0 1 12 0v3a4 4 0 0 1-4 4h-1"/>'
        '<rect x="3.5" y="10" width="3.5" height="5.5" rx="1.75"/>'
        '<rect x="17" y="10" width="3.5" height="5.5" rx="1.75"/>'
        '<path d="M11 20.5h2"/>'
    ),
    "continuidade": (
        '<path d="M20.5 12a8.5 8.5 0 1 1-2.6-6.1"/>'
        '<path d="M20.5 3.5v5h-5"/>'
        '<path d="M8.5 12l2.5 2.5 4.5-5"/>'
    ),
}


def icone_passo(nome: str) -> str:
    """Devolve o SVG inline do ícone de um passo."""
    return (
        '<svg class="passo__icone" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true" focusable="false">'
        + ICONES_PASSO.get(nome, "")
        + "</svg>"
    )


def montar_primeira_consulta(passos: list[dict]) -> str:
    """Os três passos da primeira consulta, numerados.

    É uma lista ordenada de verdade (<ol>): a ordem dos passos é parte da
    informação, não só do desenho.
    """
    partes = []
    for indice, passo in enumerate(passos, start=1):
        partes.append(
            f'<li class="passo reveal" id="passo-{escape(passo["id"])}">\n'
            f'  {icone_passo(passo["icone"])}\n'
            f'  <p class="passo__numero">Passo {indice}</p>\n'
            f'  <h3 class="passo__titulo">{escape(passo["titulo"])}</h3>\n'
            f'  <p class="passo__texto">{escape(passo["texto"])}</p>\n'
            "</li>"
        )
    return "\n".join(partes)


def montar_sobre(sobre: dict) -> str:
    """Texto da história da clínica e os três valores."""
    paragrafos = "\n".join(
        f'  <p>{escape(texto)}</p>' for texto in sobre["paragrafos"]
    )
    valores = "\n".join(
        '  <div class="valor">\n'
        f'    <h3 class="valor__titulo">{escape(valor["titulo"])}</h3>\n'
        f'    <p class="valor__texto">{escape(valor["texto"])}</p>\n'
        "  </div>"
        for valor in sobre["valores"]
    )
    return (
        '<div class="sobre__texto reveal">\n'
        f"{paragrafos}\n"
        "</div>\n"
        '<div class="sobre__valores reveal">\n'
        f"{valores}\n"
        "</div>"
    )


def indentar(html: str, espacos: int) -> str:
    """Reindenta um bloco gerado para o HTML final continuar legível."""
    recuo = " " * espacos
    return ("\n" + recuo).join(html.strip().splitlines())


# --------------------------------------------------------------------------
# Construtores de seção
# --------------------------------------------------------------------------
def montar_marquee(termos: list[str]) -> str:
    """Itens da faixa em loop (EFEITO 7).

    O template insere este bloco duas vezes: a segunda cópia leva
    aria-hidden e existe só para o loop não ter emenda.
    """
    return "".join(
        f'<span class="marquee__item">{escape(termo)}</span>' for termo in termos
    )


def montar_servicos(servicos: list[dict]) -> str:
    """Painéis empilhados em profundidade (EFEITO 3).

    Cada painel traz a imagem real do serviço (com alt descritivo, exigência
    do Projeto 01), o número, o H3 e a descrição.
    """
    partes = []
    for indice, servico in enumerate(servicos):
        partes.append(
            f'<article class="panel" data-i="{indice}" id="servico-{escape(servico["id"])}">\n'
            '  <div class="card">\n'
            '    <div class="txt">\n'
            f'      <span class="num">{indice + 1:02d}</span>\n'
            f'      <h3>{escape(servico["titulo"])}</h3>\n'
            f'      <p>{escape(servico["descricao"])}</p>\n'
            "    </div>\n"
            '    <div class="art">\n'
            f'      <img src="{escape(servico["imagem"])}" alt="{escape(servico["alt"])}"'
            ' width="800" height="600" loading="lazy" decoding="async">\n'
            "    </div>\n"
            "  </div>\n"
            "</article>"
        )
    return "\n".join(partes)


def montar_progresso(servicos: list[dict]) -> str:
    """Indicador de progresso da seção presa — um traço por serviço."""
    return "".join(f'<i data-p="{i}"></i>' for i in range(len(servicos)))


def montar_metricas(metricas: list[dict]) -> str:
    """Contadores da seção escura (EFEITO 4).

    ``data-count`` é o alvo, ``data-div`` divide para gerar decimais e
    ``data-suffix`` entra só ao terminar a contagem. O valor final também
    fica escrito no HTML, para a página fazer sentido sem JavaScript.
    """
    partes = []
    for metrica in metricas:
        atributos = f' data-count="{int(metrica["count"])}"'
        if metrica.get("div"):
            atributos += f' data-div="{int(metrica["div"])}"'
        if metrica.get("suffix"):
            atributos += f' data-suffix="{escape(metrica["suffix"])}"'

        partes.append(
            '<div class="stat reveal">\n'
            # <dt> antes de <dd> para o <dl> ser válido; o CSS inverte a
            # ordem visual (.stat usa flex-direction: column-reverse).
            f'  <dt class="l">{escape(metrica["rotulo"])}</dt>\n'
            f'  <dd class="n"{atributos}>{escape(metrica["valor"])}</dd>\n'
            "</div>"
        )
    return "\n".join(partes)


def montar_selos(selos: list[str]) -> str:
    """Compromissos da clínica, cada um com ícone SVG inline."""
    return "\n".join(f"<li>{ICONE_SELO}{escape(selo)}</li>" for selo in selos)


def montar_equipe(equipe: list[dict]) -> str:
    """Cartões da equipe: avatar, nome (H3), cargo, registro e uma linha."""
    partes = []
    for membro in equipe:
        partes.append(
            '<article class="tcard reveal">\n'
            '  <div class="av">\n'
            f'    <img src="{escape(membro["imagem"])}" alt="{escape(membro["alt"])}"'
            ' width="400" height="500" loading="lazy" decoding="async">\n'
            "  </div>\n"
            f'  <h3>{escape(membro["nome"])}</h3>\n'
            f'  <p class="role">{escape(membro["cargo"])}</p>\n'
            f'  <p class="crm">{escape(membro["registro"])}</p>\n'
            f'  <p class="bio">{escape(membro["descricao"])}</p>\n'
            "</article>"
        )
    return "\n".join(partes)


def montar_depoimentos(depoimentos: list[dict]) -> str:
    """Citações com estrelas desenhadas em SVG."""
    partes = []
    for depoimento in depoimentos:
        nota = int(depoimento["nota"])
        estrelas = "".join(
            ESTRELA.format(extra="" if posicao <= nota else ' class="vazia"')
            for posicao in range(1, 6)
        )
        rotulo = f"Avaliação: {nota} de 5 estrelas"
        partes.append(
            '<figure class="depo reveal">\n'
            f'  <div class="estrelas" role="img" aria-label="{escape(rotulo)}">{estrelas}</div>\n'
            f'  <blockquote>{escape(depoimento["texto"])}</blockquote>\n'
            f'  <figcaption>{escape(depoimento["nome"])} · {escape(depoimento["cidade"])}</figcaption>\n'
            "</figure>"
        )
    return "\n".join(partes)


def montar_faq(faq: list[dict]) -> str:
    """Acordeão acessível nativo com <details>/<summary>."""
    partes = []
    for item in faq:
        partes.append(
            '<details class="faq-item">\n'
            f'  <summary>{escape(item["pergunta"])}</summary>\n'
            f'  <p>{escape(item["resposta"])}</p>\n'
            "</details>"
        )
    return "\n".join(partes)


def montar_estados(estados: list[list[str]]) -> str:
    """As 27 unidades federativas do select do formulário."""
    return "\n".join(
        f'<option value="{escape(sigla)}">{escape(nome)}</option>'
        for sigla, nome in estados
    )


def montar_manifesto(clinica: dict) -> str:
    """Frase do manifesto, com uma palavra em ênfase itálica."""
    return (
        f'{escape(clinica["manifesto_linha1"])}<br>'
        f'{escape(clinica["manifesto_linha2"])} '
        f'<em>{escape(clinica["manifesto_enfase"])}</em><br>'
        f'{escape(clinica["manifesto_linha3"])}'
    )


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------
def construir() -> int:
    """Monta o index.html. Devolve o código de saída do processo."""
    for arquivo in (ARQUIVO_DADOS, ARQUIVO_TEMPLATE):
        if not arquivo.exists():
            print(f"ERRO: arquivo não encontrado -> {arquivo}")
            return 1

    dados = json.loads(ARQUIVO_DADOS.read_text(encoding="utf-8"))
    template = ARQUIVO_TEMPLATE.read_text(encoding="utf-8")

    clinica = dados["clinica"]
    servicos = dados["servicos"]

    substituicoes = {
        "{{NOME}}": escape(clinica["nome"]),
        "{{SLOGAN}}": escape(clinica["slogan"]),
        "{{DESCRICAO}}": escape(clinica["descricao"]),
        "{{SEO_TITULO}}": escape(clinica["seo_titulo"]),
        "{{SEO_DESCRICAO}}": escape(clinica["seo_descricao"]),
        "{{PROVA}}": indentar(montar_prova(clinica["prova"]), 8),
        "{{WHATSAPP_LINK}}": "https://wa.me/" + escape(clinica["whatsapp"]["numero"]),
        "{{WHATSAPP_ARIA}}": escape(clinica["whatsapp"]["aria"]),
        "{{WHATSAPP_ROTULO}}": escape(clinica["whatsapp"]["rotulo"]),
        "{{PRIMEIRA_CONSULTA}}": indentar(
            montar_primeira_consulta(dados["primeira_consulta"]), 10),
        "{{TRAZER}}": escape(dados["primeira_consulta_trazer"]),
        "{{SOBRE_OLHO}}": escape(dados["sobre"]["olho"]),
        "{{SOBRE_TITULO}}": escape(dados["sobre"]["titulo"]),
        "{{SOBRE}}": indentar(montar_sobre(dados["sobre"]), 8),
        "{{HERO_L1}}": escape(clinica["hero_linha1"]),
        "{{HERO_L2}}": escape(clinica["hero_linha2"]),
        "{{HERO_SUB}}": escape(clinica["hero_sub"]),
        "{{MANIFESTO}}": montar_manifesto(clinica),
        "{{LEAD_ESCURO}}": escape(clinica["lead_escuro"]),
        "{{TELEFONE}}": escape(clinica["telefone"]),
        "{{TELEFONE_LINK}}": escape(clinica["telefone_link"]),
        "{{EMAIL}}": escape(clinica["email"]),
        "{{ENDERECO}}": escape(clinica["endereco"]),
        "{{HORARIO}}": escape(clinica["horario"]),
        "{{ANO}}": str(date.today().year),
        "{{PIN_ALTURA}}": f"{len(servicos) * VH_POR_PAINEL}vh",
        "{{MARQUEE}}": montar_marquee(dados["marquee"]),
        "{{SERVICOS}}": indentar(montar_servicos(servicos), 8),
        "{{PROGRESSO}}": montar_progresso(servicos),
        "{{METRICAS}}": indentar(montar_metricas(clinica["metricas"]), 10),
        "{{SELOS}}": indentar(montar_selos(dados["selos"]), 10),
        "{{EQUIPE}}": indentar(montar_equipe(dados["equipe"]), 8),
        "{{DEPOIMENTOS}}": indentar(montar_depoimentos(dados["depoimentos"]), 10),
        "{{FAQ}}": indentar(montar_faq(dados["faq"]), 10),
        "{{ESTADOS}}": indentar(montar_estados(dados["estados"]), 16),
    }

    html = template
    for marcador, valor in substituicoes.items():
        html = html.replace(marcador, valor)

    # Nenhum marcador pode sobrar no arquivo publicado.
    restantes = re.findall(r"\{\{[^}]+\}\}", html)
    if restantes:
        print("ERRO: sobraram marcadores no HTML -> " + ", ".join(sorted(set(restantes))))
        return 1

    ARQUIVO_SAIDA.write_text(html, encoding="utf-8")

    # ---------------------------- resumo ----------------------------------
    print("Build concluído — index.html gerado.")
    print(f"  Arquivo .............. {ARQUIVO_SAIDA.relative_to(RAIZ)}")
    print(f"  Tamanho .............. {ARQUIVO_SAIDA.stat().st_size / 1024:.1f} KB")
    print(f"  Serviços (painéis) ... {len(servicos)}")
    print(f"  Altura da seção presa  {len(servicos) * VH_POR_PAINEL}vh "
          f"({VH_POR_PAINEL}vh por painel)")
    print(f"  Prova no hero ........ {clinica['prova']['nota_texto']} + "
          f"{len(clinica['prova']['itens'])} fatos")
    print(f"  Primeira consulta .... {len(dados['primeira_consulta'])} passos")
    print(f"  Nossa história ....... {len(dados['sobre']['paragrafos'])} parágrafos + "
          f"{len(dados['sobre']['valores'])} valores")
    print(f"  Termos no marquee .... {len(dados['marquee'])} (x2 para o loop)")
    print(f"  Métricas (contadores)  {len(clinica['metricas'])}")
    print(f"  Selos ................ {len(dados['selos'])}")
    print(f"  Equipe ............... {len(dados['equipe'])}")
    print(f"  Depoimentos .......... {len(dados['depoimentos'])}")
    print(f"  Perguntas (FAQ) ...... {len(dados['faq'])}")
    print(f"  Estados (UF) ......... {len(dados['estados'])}")
    print(f"  Imagens <img> ........ {html.count('<img ')}")
    print("  Marcadores {{...}} restantes: nenhum.")
    return 0


if __name__ == "__main__":
    sys.exit(construir())
