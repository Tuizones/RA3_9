# Integrantes:
#   Arthur Hoffmann Tuyzones
#   Emanuel Henrique Ricetto
#   Frederico Frutuoso
# Grupo Canvas: RA3 9
# Instituição: Pontifícia Universidade Católica do Paraná
# Disciplina: Linguagens Formais e Compiladores
# Professor: Frank Coelho de Alcantara

"""CLI da Fase 3 — primeira iteração.

Esta versão só executa lex + parse e prepara a saída para a fase semântica
que será integrada no próximo commit. O ponto de extensão está marcado com
`# TODO(arthur): integrar semantica`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.lexer_fsm import lex
from src.parser_ll1 import construir_arvore
from src.pipeline import (
    prepararEntradaSemantica,
    salvar_tokens,
    salvar_arvore,
    salvar_derivacao,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "output"

EXIT_OK = 0
EXIT_ERRO_LEX_SINT = 2


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analisador semântico — Fase 3 (versão inicial)",
    )
    parser.add_argument("arquivo", type=Path, help="caminho do arquivo-fonte")
    parser.add_argument(
        "--saida",
        type=Path,
        default=OUTPUT_DIR,
        help="diretório onde gravar os artefatos",
    )
    return parser.parse_args()


def _imprimir_secao(titulo: str) -> None:
    print()
    print("=" * 72)
    print(titulo)
    print("=" * 72)


def main() -> int:
    args = _parse_args()
    fonte = args.arquivo.read_text(encoding="utf-8")
    args.saida.mkdir(parents=True, exist_ok=True)

    _imprimir_secao("LÉXICO + SINTÁTICO")
    try:
        entrada = prepararEntradaSemantica(fonte)
    except Exception as exc:  # pragma: no cover - placeholder
        print(f"[ERRO LEX/SINT] {exc}", file=sys.stderr)
        return EXIT_ERRO_LEX_SINT

    salvar_tokens(entrada["tokens"], args.saida / "tokens_ultima_execucao.txt")
    salvar_arvore(entrada["arvore"], args.saida / "arvore_ultima_execucao.md")
    salvar_derivacao(entrada["derivacao"], args.saida / "derivacao_ultima_execucao.md")

    # TODO(arthur): integrar semantica (próximo commit)
    print("Lex/Parse concluídos. Fase semântica ainda não integrada.")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
