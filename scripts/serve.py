#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Servidor local de desenvolvimento da Clínica Vitalis.

Sobe um ``http.server`` servindo a raiz do projeto e abre o navegador.
Apenas biblioteca padrão. Serve para conferir o site como ele ficará no
GitHub Pages — o site em si não precisa de servidor nenhum.

Uso:
    python scripts/serve.py            # porta 8000
    python scripts/serve.py 8080       # outra porta

Para encerrar: Ctrl+C.
"""

from __future__ import annotations

import sys
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PORTA_PADRAO = 8000


def ler_porta() -> int:
    """Lê a porta do primeiro argumento da linha de comando, se houver."""
    if len(sys.argv) < 2:
        return PORTA_PADRAO
    try:
        return int(sys.argv[1])
    except ValueError:
        print(f"Porta inválida: {sys.argv[1]!r}. Usando {PORTA_PADRAO}.")
        return PORTA_PADRAO


def servir() -> int:
    porta = ler_porta()

    if not (RAIZ / "index.html").exists():
        print("Aviso: index.html ainda não existe. Rode antes:")
        print("    python scripts/build.py\n")

    manipulador = partial(SimpleHTTPRequestHandler, directory=str(RAIZ))

    try:
        servidor = ThreadingHTTPServer(("127.0.0.1", porta), manipulador)
    except OSError as erro:
        print(f"Não foi possível abrir a porta {porta}: {erro}")
        print("Tente outra porta, por exemplo:  python scripts/serve.py 8080")
        return 1

    endereco = f"http://localhost:{porta}/"
    print("Clínica Vitalis — servidor local")
    print(f"  Pasta servida .... {RAIZ}")
    print(f"  Endereço ......... {endereco}")
    print("  Encerrar ......... Ctrl+C\n")

    webbrowser.open(endereco)

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(servir())
